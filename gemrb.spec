#
# Conditional build:
%bcond_with	gles	# build GLES backend (broken)

Summary:	Emulator of BioWare's Infinity game engine
Summary(pl.UTF-8):	Emulator silnika gier Infinity firmy BioWare
Name:		gemrb
Version:	0.9.4
Release:	4
License:	GPL v2+
Group:		Applications/Emulators
Source0:	https://downloads.sourceforge.net/gemrb/%{name}-sources-%{version}.tar.gz
# Source0-md5:	289dcda433c012e4a15b5c0d80a4e70e
Patch0:		%{name}-config_file.patch
Patch1:		flags.patch
URL:		http://gemrb.sourceforge.net/
BuildRequires:	OpenAL-devel
%{!?with_gles:BuildRequires:	OpenGL-devel}
%{?with_gles:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	SDL2-devel
BuildRequires:	SDL2_mixer-devel
BuildRequires:	cmake >= 3.25
BuildRequires:	freetype-devel
%{!?with_gles:BuildRequires:	glew-devel}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	vlc-devel
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
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
%patch -P 0 -p1
%patch -P 1 -p1

%{__sed} -i -e '1s,/usr/bin/python$,%{__python3},' admin/extend2da.py

%build
install -d build
cd build
%cmake .. \
	-DBIN_DIR="%{_bindir}" \
	-DSYSCONF_DIR="%{_sysconfdir}/gemrb" \
	-DLIB_DIR="%{_libdir}" \
	-DPLUGIN_DIR="%{_libdir}/gemrb/plugins" \
	-DDATA_DIR="%{_datadir}/gemrb" \
	-DMAN_DIR="%{_mandir}/man6" \
	-DICON_DIR="%{_pixmapsdir}" \
	-DSVG_DIR="%{_iconsdir}/hicolor/scalable/apps" \
	-DMENU_DIR="%{_desktopdir}" \
	-DOPENGL_BACKEND=%{!?with_gles:OpenGL}%{?with_gles:GLES} \
	-DSDL_BACKEND=SDL2
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -C build \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/gemrb/GemRB.cfg{.noinstall,}.sample
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/gemrb/{GemRB.cfg,gemrb.cfg}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md NEWS README.md %{name}/{docs/en/*.txt,GemRB.cfg*.sample}
%dir %{_sysconfdir}/gemrb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gemrb/gemrb.cfg
%attr(755,root,root) %{_bindir}/gemrb
%attr(755,root,root) %{_libdir}/libgemrb_core.so.*.*.*
%dir %{_libdir}/gemrb
%dir %{_libdir}/gemrb/plugins
%attr(755,root,root) %{_libdir}/gemrb/plugins/*.so
%{_datadir}/gemrb
%{_mandir}/man6/gemrb.6*
%{_desktopdir}/gemrb.desktop
%{_iconsdir}/hicolor/scalable/apps/gemrb.svg
%{_pixmapsdir}/gemrb.png
%{_datadir}/metainfo/org.gemrb.gemrb.metainfo.xml
