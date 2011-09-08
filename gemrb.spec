# TODO:
# - make it build on x86_64
#
# Conditional build:
%bcond_without	png	# build without png

Summary:	Emulator of BioWare's Infinity game engine
Summary(pl.UTF-8):	Emulator silnika gier Infinity firmy BioWare
Name:		gemrb
Version:	0.6.5
Release:	0.1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://downloads.sourceforge.net/gemrb/%{name}-%{version}.tar.gz
# Source0-md5:	16b42bc0c11520743e2f84df659285b3
Patch0:		%{name}-config_file.patch
Patch1:		%{name}-useless_files.patch
URL:		http://gemrb.sourceforge.net/
BuildRequires:	OpenAL-devel
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_png:BuildRequires:	libpng-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3.0
BuildRequires:	python-modules
BuildRequires:	zlib-devel
Suggests:	synce-unshield
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Game Engine is a port of the original Infinity Engine (the one of
Baldur's Gate, Planescape: Torment, Icewind Dale) to Linux/Unix, MacOs
X and Windows with some Enhancements.

%description -l pl.UTF-8
Silnik ten jest portem oryginalnego silnika Infinity Engine (używanego
przez Baldur's Gate, Planescape: Torment, Icewind Dale) dla systemów
Linux/Unix, MacOS i Windows. Silnik posiada kilka ulepszeń.

%prep
%setup -q
%patch0 -p1
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_datadir}/gemrb/Cache}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install gemrb/GemRB.cfg.sample.in $RPM_BUILD_ROOT%{_sysconfdir}/gemrb.cfg
%{__rm} $RPM_BUILD_ROOT%{_libdir}{,/gemrb/plugins}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO %{name}{/docs/en/*.txt,/GemRB.cfg*.sample}
%attr(755,root,root) %{_bindir}/gemrb
%dir %{_libdir}/gemrb
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/gemrb/plugins
%attr(755,root,root) %{_libdir}/gemrb/plugins/*.so*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gemrb.cfg
%{_datadir}/gemrb
%{_mandir}/man6/gemrb.6*
