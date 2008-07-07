%define name sidplay-libs
%define spmajor 2
%define libname    %mklibname sidplay %{spmajor}
%define sumajor 0
%define libnamesu %mklibname sidutils %{sumajor}
%define develnamesu %mklibname -d sidutils
%define staticdevelnamesu %mklibname -s -d sidutils
%define version 2.1.1
%define release %mkrel 7
%define builders %{_libdir}/sidplay/builders


Summary:        A Commodore 64 music player and SID chip emulator library
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source:         http://prdownloads.sourceforge.net/sidplay2/%{name}-%version.tar.bz2
Patch:		sidplay-libs-2.1.1-gcc4.3.patch
License:        GPLv2+
Group:          System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://sidplay2.sourceforge.net/
BuildRequires:	automake1.8
BuildRequires:  chrpath

%description
This is a cycle-based version of a C64 music playing library
developed by Simon White. This library provides no internal
SID emulation. Instead a means to drive any external SID hardware or
emulation has been provided using the SID Builder Classes.

A ReSID Builder Class using a modified version of ReSID 0.13
is included in this package. Alternative/updated classes can be
obtained from the SIDPlay2 homepage.

%package -n %libname
Summary:        A Commodore 64 music player and SID chip emulator library
Group:          System/Libraries

%description -n %libname
This is a cycle-based version of a C64 music playing library
developed by Simon White. This library provides no internal
SID emulation. Instead a means to drive any external SID hardware or
emulation has been provided using the SID Builder Classes.

A ReSID Builder Class using a modified version of ReSID 0.13
is included in this package. Alternative/updated classes can be
obtained from the SIDPlay2 homepage.

#gw don't use libsidplay-devel here, that's libsidplay1
%package -n %libname-devel
Summary:        Development headers and libraries for %{libname}
Group:          Development/C++
Requires:       %{libname} = %{version}
Provides:       libsidplay-devel = %{version}-%release
Provides:	sidplay2-devel = %version-%release
Requires:	pkgconfig

%description -n %libname-devel
This package includes the header and library files necessary
for developing applications to use %{libname}.

%package -n %libnamesu
Summary:        General utility library for use in sidplayers
Requires:	%libname = %version
Group:          System/Libraries
%description -n %libnamesu
This library provides general utilities that are not considered core
to the C64 emulation.  Utilities include decoding and obtaining tune
lengths from the songlength database, INI file format parser and SID
filter files (types 1 and 2).

%package -n %develnamesu
Summary:        Development headers and libraries for libsidutils
Group:          Development/C++
Requires:       %libnamesu = %{version}
Requires:	%libname-devel = %version
Provides:       libsidutils-devel = %{version}-%release
Obsoletes:	%mklibname -d sidutils 0

%description -n %develnamesu
This package includes the header and library files necessary
for developing applications to use %libnamesu.

%package -n %staticdevelnamesu
Summary:        Static library for %libnamesu
Group:          Development/C++
Requires:       %develnamesu = %{version}
Obsoletes:	%mklibname -s -d sidutils 0
Provides:	libsidutils-static-devel = %version-%release

%description -n %staticdevelnamesu
This package includes the static library file necessary
for developing applications to use %libnamesu.


%prep
%setup -q 
%patch -p1 -b .gcc
aclocal-1.8 -I unix
automake-1.8
autoconf
cd resid
aclocal-1.8
libtoolize --copy --force
automake-1.8
autoconf
cd ..

%build
export CFLAGS="%optflags -fPIC"
export CXXFLAGS="%optflags -fPIC"
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT 
#hack to prevent relinking
sed s/relink_command.*// < libsidutils/src/libsidutils.la > tmp.la
mv tmp.la libsidutils/src/libsidutils.la
%makeinstall_std
chrpath -d %buildroot%_libdir/libsidutils.so

rm -f %buildroot%builders/libsid*
rm -rf %buildroot%builders/pkgconfig

%if %mdkversion >= 1020
%multiarch_includes %buildroot%_includedir/sidplay/sidconfig.h
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%post -n %libnamesu -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libnamesu -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%doc libsidplay/AUTHORS libsidplay/ChangeLog libsidplay/README libsidplay/TODO
%{_libdir}/libsidplay*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%dir %{_libdir}/sidplay/
%dir %{_libdir}/sidplay/builders
%dir %{_includedir}/sidplay/builders/
%{_includedir}/sidplay/*.h
%{_includedir}/sidplay/builders/*.h
%if %mdkversion >= 1020
%multiarch %multiarch_includedir/sidplay/
%endif
%{_libdir}/libsidplay*.so
%{_libdir}/libsidplay*.a
%{_libdir}/libsidplay*.la
%{_libdir}/pkgconfig/libsidplay*.pc
%{builders}/*.la
%{builders}/*.a

%files -n %libnamesu
%defattr(-,root,root)
%doc libsidutils/AUTHORS libsidutils/ChangeLog libsidutils/README libsidutils/TODO
%{_libdir}/libsidutils*.so.*

%files -n %develnamesu
%defattr(-,root,root)
%dir %{_includedir}/sidplay/utils/
%{_includedir}/sidplay/utils/*
%{_libdir}/libsidutils*.la
%{_libdir}/libsidutils*.so
%_libdir/pkgconfig/libsidutils*pc

%files -n %staticdevelnamesu
%defattr(-,root,root)
%{_libdir}/libsidutils*.a
