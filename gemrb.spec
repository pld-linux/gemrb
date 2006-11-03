#
# Conditional build:
%bcond_without	png	# build without png
#
Summary:	Emulator of BioWare's Infinity game engine
Summary(pl):	Emulator silnika BioWare Infinity
Name:		gemrb
Version:	0.2.7
Release:	0.1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/gemrb/%{name}-%{version}.tar.gz
# Source0-md5:	5ccc073a21464a33ca0e712c5dba34b0
Patch0:		%{name}-Makefile_am.patch
Patch1:		%{name}-config_file.patch
URL:		http://gemrb.sourceforge.net/
BuildRequires:	OpenAL-devel
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libtool
BuildRequires:	python-devel >= 1:2.3.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Game Engine is a port of the original Infinity Engine (the one of
Baldur's Gate, Planescape: Torment, Icewind Dale) to Linux/Unix, MacOs
X and Windows with some Enhancements.

%description -l pl
Silnik ten jest portem oryginalnego silnika Infinity Engine (u¿ywanego
przez Baldur's Gate, Planescape: Torment, Icewind Dale) dla systemów
Linux/Unix, MacOs i Windowsa. Silnik posiada kilka ulepszeñ.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO %{name}/docs/en/*.txt
%attr(755,root,root) %{_bindir}/gemrb
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/*.so*
%{_libdir}/gemrb/*.la
%attr(755,root,root) %{_libdir}/gemrb/*.so*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/GemRB.cfg
%{_datadir}/gemrb
%{_mandir}/man1/gemrb.1*
