Summary:	IDE for R
Summary(pl.UTF-8):	IDE dla R
Name:		rstudio
Version:	1.1.143
Release:	1
License:	AGPLv3
Group:		Applications
Source0:	https://github.com/rstudio/rstudio/archive/v%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	ae531eed17e70a6d4f2d8560696b466e
Source1:	https://s3.amazonaws.com/rstudio-dictionaries/core-dictionaries.zip
# Source1-md5:	0e03798b8e53096c4a906bde05e32378
Source2:	https://s3.amazonaws.com/rstudio-buildtools/gwt-2.7.0.zip
# Source2-md5:	a8f3704a597b392910ea060284f21a03
Source3:	https://s3.amazonaws.com/rstudio-buildtools/gin-1.5.zip
# Source3-md5:	2409168cc18bf5f341e107e6887fe359
Source4:	https://s3.amazonaws.com/rstudio-buildtools/mathjax-26.zip
# Source4-md5:	94fcab0aead8f730cd21e26dcb5a330d
Source5:	https://s3.amazonaws.com/rstudio-buildtools/pandoc-1.12.4.2.zip
# Source5-md5:	d0f7e3d23b42cb9d26d2783d659040cf
Source6:	https://s3.amazonaws.com/rstudio-buildtools/libclang-3.5.zip
# Source6-md5:	cf1a43d2d6203a765ef16d7b12382c8a
Source7:	https://s3.amazonaws.com/rstudio-buildtools/libclang-builtin-headers.zip
# Source7-md5:	e6790a3ee6c371968eba865fc0a84daf
Source8:	packrat_0.4.1.24_bbdab984134678db91b8f372e2550e59f266de37.tar.xz
# Source8-md5:	7607927c4adf507d67d2ba18d38c7bb0
Source9:	rmarkdown_1.4.0.9001_b7434dcc5abe87cb27f01cbffb9ca94e1539d322.tar.xz
# Source9-md5:	3555af924d08fa900789c61eaa837087
Source10:	shinyapps_0.3.61_d3ab9e1cdd02f0067d69fe6fc816a61c8a5f2218.tar.xz
# Source10-md5:	3f5ce12f86b00a2e77067d7769fffe08
Source11:	rsconnect_0.7.0-2_fa486121f8f75701e2044f33d2901e610160322f.tar.xz
# Source11-md5:	938ca5efbed1ead619de42488ed30760
Patch0:		%{name}-includes.patch
Patch1:		%{name}-openssl.patch
Patch2:		%{name}-boost.patch
URL:		http://rstudio.org/
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5XmlPatterns-devel
BuildRequires:	R >= 2.11.1
BuildRequires:	boost-devel >= 1.50
BuildRequires:	clang-devel >= 3.5.0
BuildRequires:	cmake >= 2.8.0
BuildRequires:	java-junit
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pandoc
BuildRequires:	pango-devel
Requires:	R >= 2.11.1
Requires:	pandoc
Requires:	clang >= 3.5.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RStudio(tm) is a free and open source integrated development
environment (IDE) for R. You can run it on your desktop (Windows, Mac,
or Linux) or even over the web using RStudio Server.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
mkdir -p dependencies/common/dictionaries
unzip -qq %{SOURCE1} -d dependencies/common/dictionaries
mkdir -p src/gwt/lib/gwt
mkdir -p src/gwt/lib/gin/1.5
unzip -qq %{SOURCE2} -d src/gwt/lib/gwt
unzip -qq %{SOURCE3} -d src/gwt/lib/gin/1.5
%{__mv} src/gwt/lib/gwt/gwt-2.7.0 src/gwt/lib/gwt/2.7.0
unzip -qq %{SOURCE4} -d dependencies/common

xz -dc %{SOURCE8} | tar xf - -C dependencies/common/
xz -dc %{SOURCE9} | tar xf - -C dependencies/common/
xz -dc %{SOURCE10} | tar xf - -C dependencies/common/
xz -dc %{SOURCE11} | tar xf - -C dependencies/common/

# rstudio wants 1.12.4.2, let it think that
mkdir -p dependencies/common/pandoc/1.12.4.2
ln -s %{_bindir}/pandoc dependencies/common/pandoc/1.12.4.2/pandoc
ln -s %{_bindir}/pandoc dependencies/common/pandoc/1.12.4.2/pandoc-static

mkdir -p dependencies/common/libclang/3.5/include/
ln -s /usr/include/clang-c dependencies/common/libclang/3.5/include/
mkdir -p dependencies/common/libclang/builtin-headers
ln -s /usr/lib64/clang/3.5.0/include dependencies/common/libclang/builtin-headers/3.5
#dependencies/common/libclang/builtin-headers/libc++/3.5
%ifarch %{ix86}
mkdir -p dependencies/common/libclang/3.5/linux/x86
ln -s %{_libdir}/libclang.so dependencies/common/libclang/3.5/linux/x86/libclang.so
%endif
%ifarch %{x8664}
mkdir -p dependencies/common/libclang/3.5/linux/x86_64
ln -s %{_libdir}/libclang.so dependencies/common/libclang/3.5/linux/x86_64/libclang.so
%endif

%build
install -d build
cd build
%cmake \
	-DQT_QMAKE_EXECUTABLE=/usr/bin/qt5-qmake \
	-DCMAKE_CXX_FLAGS_RELEASE="${CXXFLAGS:-%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG}" \
	-DCMAKE_C_FLAGS_RELEASE="${CFLAGS:-%{rpmcflags} -DNDEBUG -DQT_NO_DEBUG}" \
	-DRSTUDIO_TARGET=Desktop \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{_libdir}/%{name}/bin/rstudio $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NOTICE README.md
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/R
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/diagnostics
%attr(755,root,root) %{_libdir}/%{name}/bin/r*
%dir %{_libdir}/%{name}/bin/postback
%attr(755,root,root) %{_libdir}/%{name}/bin/postback/*
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/www
%{_libdir}/%{name}/www-symbolmaps
%{_libdir}/%{name}/rstudio.png
%{_desktopdir}/rstudio.desktop
%{_iconsdir}/hicolor/*x*/apps/*
%{_iconsdir}/hicolor/*x*/mimetypes/*
%{_datadir}/mime/packages/*.xml
%{_pixmapsdir}/rstudio.png
