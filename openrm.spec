%define name openrm
%define version 1.5.2
%define release %mkrel 5

%define rmver rm152

%define major 1
%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} %major -d


Summary: OpenRM development environment 
Name: %name
Version: %version
Release: %release
Source0: openrm-devel-%{version}-3.tar.bz2
Source1: openrm-demo-%{version}.tar.bz2
Source2: openrm-cave-demo-%{version}.tar.bz2
URL: https://openrm.sourceforge.net/
License: LGPL
Group: System/Libraries
Buildrequires: X11-devel mesaglu-devel
BuildRoot: %{_tmppath}/%name-buildroot
Requires: libGL.so.1, libGLU.so.1, libjpeg.so.62

%description
OpenRM Scene Graph is set of tools and utilities that implement a
high performance, flexible and extendible scene graph API. Underneath
OpenRM, OpenGL(tm) is used as the graphics platform for rendering,
so OpenRM is highly portable and can deliver blazing rendering speeds.
OpenRM can be used on any platform that has OpenGL

%package -n %libname
License: LGPL
Group: System/Libraries
Summary: Development environment to build high performance graphics

%description -n %libname
OpenRM Scene Graph is set of tools and utilities that implement a
high performance, flexible and extendible scene graph API. Underneath
OpenRM, OpenGL(tm) is used as the graphics platform for rendering,
so OpenRM is highly portable and can deliver blazing rendering speeds.
OpenRM can be used on any platform that has OpenGL

%package -n %libnamedev
License: LGPL
Group: System/Libraries
Summary: Development environment to build high performance graphics
Requires: %libname = %version
Provides: libopenrm-devel

%description -n %libnamedev
OpenRM Scene Graph is set of tools and utilities that implement a
high performance, flexible and extendible scene graph API. Underneath
OpenRM, OpenGL(tm) is used as the graphics platform for rendering,
so OpenRM is highly portable and can deliver blazing rendering speeds.
OpenRM can be used on any platform that has OpenGL


%prep
%setup -T -c
%setup -q -T -a 0 -D -c
%setup -q -T -a 1 -D -c
%setup -q -T -a 2 -D -c

perl -pi -e 's/"CFLAGS = .*"/"CFLAGS = %optflags -c -D_BSD_SOURCE -finline-functions -fomit-frame-pointer -DRM_X -fPIC"/' %{rmver}/make.cfg
# (tv) fix typos breaking build in build system:
perl -pi -e 's/"\\/" \\/' %{rmver}/make.cfg
%ifarch ppc64 x86_64 sparc64 alpha
perl -pi -e 's/"ARCHFLAGS.*"/"ARCHFLAGS = 64"/' %{rmver}/make.cfg
%endif

%build
export CFLAGS='%optflags'

pushd %{rmver}
make linux
make docs
popd

pushd rmdemo
./configure -opengl=%_prefix -rm=%_prefix -x11=%_prefix/X11R6 -opt='%optflags' -jpeg=%_prefix
popd

pushd openRMCaveDemos
./configure -opengl=%_prefix -rm=%_prefix -x11=%_prefix/X11R6 -opt='%optflags'
popd

%install
mkdir -p ${RPM_BUILD_ROOT}/usr
cp -arf %{rmver}/include ${RPM_BUILD_ROOT}/usr
cp -far %{rmver}/lib ${RPM_BUILD_ROOT}/usr


%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root)
%doc %{rmver}/FUTUREPLANS %{rmver}/LICENSE.html %{rmver}/README %{rmver}/RELEASENOTES %{rmver}/VERSION %{rmver}/doc/HTML rmdemo openRMCaveDemos
%_libdir/*.so.*

%files -n %libnamedev
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%_libdir/*.a

