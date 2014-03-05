%define spmajor 2
%define libname    %mklibname sidplay %{spmajor}
%define sumajor 0
%define libnamesu %mklibname sidutils %{sumajor}
%define develnamesu %mklibname -d sidutils
%define staticdevelnamesu %mklibname -s -d sidutils
%define builders %{_libdir}/sidplay/builders

Summary:	A Commodore 64 music player and SID chip emulator library
Name:		sidplay-libs
Version:	2.1.1
Release:	19
License:	GPLv2+
Group:		System/Libraries
URL:		http://sidplay2.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/sidplay2/%{name}-%version.tar.bz2
Patch0:		sidplay-libs-2.1.1-gcc4.3.patch
#gw from xsidplay 2.0.3
Patch1:		cia1.patch
BuildRequires:	automake
BuildRequires:	chrpath

%description
This is a cycle-based version of a C64 music playing library
developed by Simon White. This library provides no internal
SID emulation. Instead a means to drive any external SID hardware or
emulation has been provided using the SID Builder Classes.

A ReSID Builder Class using a modified version of ReSID 0.13
is included in this package. Alternative/updated classes can be
obtained from the SIDPlay2 homepage.

%package -n %{libname}
Summary:	A Commodore 64 music player and SID chip emulator library
Group:		System/Libraries

%description -n %{libname}
This is a cycle-based version of a C64 music playing library
developed by Simon White. This library provides no internal
SID emulation. Instead a means to drive any external SID hardware or
emulation has been provided using the SID Builder Classes.

A ReSID Builder Class using a modified version of ReSID 0.13
is included in this package. Alternative/updated classes can be
obtained from the SIDPlay2 homepage.

%package -n %{libname}-devel
Summary:	Development headers and libraries for %{libname}
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	sidplay2-devel = %{version}-%{release}

%description -n %{libname}-devel
This package includes the header and library files necessary
for developing applications to use %{libname}.

%package -n %{libnamesu}
Summary:	General utility library for use in sidplayers
Requires:	%{libname} = %{version}-%{release}
Group:		System/Libraries

%description -n %{libnamesu}
This library provides general utilities that are not considered core
to the C64 emulation.  Utilities include decoding and obtaining tune
lengths from the songlength database, INI file format parser and SID
filter files (types 1 and 2).

%package -n %{develnamesu}
Summary:	Development headers and libraries for libsidutils
Group:		Development/C++
Requires:	%{libnamesu} = %{version}-%{release}
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	libsidutils-devel = %{version}-%{release}

%description -n %{develnamesu}
This package includes the header and library files necessary
for developing applications to use %{libnamesu}.

%package -n %{staticdevelnamesu}
Summary:	Static library for %{libnamesu}
Group:		Development/C++
Requires:	%{develnamesu} = %{version}
Provides:	libsidutils-static-devel = %{version}-%{release}

%description -n %{staticdevelnamesu}
This package includes the static library file necessary
for developing applications to use %{libnamesu}.


%prep
%setup -q
%patch0 -p1 -b .gcc
%patch1 -p1
for i in . * */*; do
	[ -d "$i" ] || continue
	[ -e "$i/configure.in" -o -e "$i/configure.ac" ] || continue
	pushd $i
	aclocal -I unix
	libtoolize --copy --force
	automake -a
	autoconf
	popd
done

%build
export CFLAGS="%optflags -fPIC"
export CXXFLAGS="%optflags -fPIC"
%configure2_5x
%make

%install
#hack to prevent relinking
sed s/relink_command.*// < libsidutils/src/libsidutils.la > tmp.la
mv tmp.la libsidutils/src/libsidutils.la
%makeinstall_std
chrpath -d %{buildroot}%{_libdir}/libsidutils.so

rm -f %{buildroot}%{builders}/libsid*
rm -rf %{buildroot}%{builders}/pkgconfig

%multiarch_includes %{buildroot}%{_includedir}/sidplay/sidconfig.h

sed -i -e 's,${libdir}/libsidplay2.la,-lsidplay2,g' %{buildroot}%{_libdir}/pkgconfig/*.pc

%files -n %libname
%doc libsidplay/AUTHORS libsidplay/ChangeLog libsidplay/README libsidplay/TODO
%{_libdir}/libsidplay*.so.*

%files -n %libname-devel
%dir %{_libdir}/sidplay/
%dir %{_libdir}/sidplay/builders
%dir %{_includedir}/sidplay/builders/
%{_includedir}/sidplay/*.h
%{_includedir}/sidplay/builders/*.h
%{multiarch_includedir}/sidplay/

%{_libdir}/libsidplay*.so
%{_libdir}/libsidplay*.a
%{_libdir}/pkgconfig/libsidplay*.pc
%{builders}/*.a

%files -n %{libnamesu}
%doc libsidutils/AUTHORS libsidutils/ChangeLog libsidutils/README libsidutils/TODO
%{_libdir}/libsidutils*.so.*

%files -n %{develnamesu}
%dir %{_includedir}/sidplay/utils/
%{_includedir}/sidplay/utils/*
%{_libdir}/libsidutils*.so
%{_libdir}/pkgconfig/libsidutils*pc

%files -n %{staticdevelnamesu}
%{_libdir}/libsidutils*.a


%changelog
* Fri Jun 29 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.1.1-11
+ Revision: 807480
- Get rid of bogus .la files
- Don't BuildRequire prehistoric auto* tools
- Clean up spec file

* Wed Jul 13 2011 Götz Waschk <waschk@mandriva.org> 2.1.1-10
+ Revision: 689842
- work around rpm macro bug
- rebuild

* Fri May 22 2009 Götz Waschk <waschk@mandriva.org> 2.1.1-9mdv2011.0
+ Revision: 378682
- rebuild

* Wed May 06 2009 Götz Waschk <waschk@mandriva.org> 2.1.1-8mdv2010.0
+ Revision: 372560
- add cia1 timer support for xsidplay

* Mon Jul 07 2008 Götz Waschk <waschk@mandriva.org> 2.1.1-7mdv2009.0
+ Revision: 232324
- update the patch for gcc 4.3
- update license
- fix devel name for the sidutils package

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jul 06 2007 Götz Waschk <waschk@mandriva.org> 2.1.1-6mdv2008.0
+ Revision: 48919
- bump release
- Import sidplay-libs

