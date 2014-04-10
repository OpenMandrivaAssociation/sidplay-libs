%define spmajor 1
%define libname    %mklibname sidplay 2 %{spmajor}
%define sumajor 0
%define libnamesu %mklibname sidutils %{sumajor}
%define develnamesu %mklibname -d sidutils

Summary:	A Commodore 64 music player and SID chip emulator library
Name:		sidplay-libs
Version:	2.1.2
Release:	0.svn1452.2
License:	GPLv2+
Group:		System/Libraries
URL:		http://sidplay2.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/sidplay2/%{name}-%{version}.tar.xz
#gw from xsidplay 2.0.3
Patch1:		sidplay-libs-2.1.2-cia.patch
Patch3:         sidplay-libs-2.1.1-pkgconfig.patch
Patch4:		sidplay-libs-2.1.2-autofoo-fixes.patch
Patch5:		sidplay-libs-2.1.2-fix-broken-exceptions.check.patch

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
%define	oldname	%mklibname sidplay 2
%rename		%{oldname}

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
Requires:	%{libname} = %{EVRD}
Provides:	sidplay2-devel = %{EVRD}
%define	oldname	%mklibname sidplay 2
%rename		%{oldname}-devel

%description -n %{libname}-devel
This package includes the header and library files necessary
for developing applications to use %{libname}.

%package -n %{libnamesu}
Summary:	General utility library for use in sidplayers
Requires:	%{libname} = %{EVRD}
Group:		System/Libraries

%description -n %{libnamesu}
This library provides general utilities that are not considered core
to the C64 emulation.  Utilities include decoding and obtaining tune
lengths from the songlength database, INI file format parser and SID
filter files (types 1 and 2).

%package -n %{develnamesu}
Summary:	Development headers and libraries for libsidutils
Group:		Development/C++
Requires:	%{libnamesu} = %{EVRD}
Requires:	%{libname}-devel = %{EVRD}
Provides:	sidutils-devel = %{EVRD}

%description -n %{develnamesu}
This package includes the header and library files necessary
for developing applications to use %{libnamesu}.

%prep
%setup -q
%apply_patches
for dir in libsidplay libsidutils; do
	pushd $dir
	#ugly libtool hack..
	echo '/usr/bin/libtool --tag=CXX $@' > libtool
	chmod +x libtool
	./bootstrap
	popd
done

%build
pushd libsidplay
%configure2_5x	--enable-shared
%make
popd
pushd libsidutils
%configure2_5x	--enable-shared \
		--with-sidplay2-dir=../libsidplay \
		--with-sidplay2-includes=../libsidplay/include \
		--with-sidplay2-library=../libsidplay/src
%make LIBVERSION="%{spmajor}:0:1"
popd

%install
%makeinstall_std -C libsidplay
%makeinstall_std -C libsidutils

%files -n %{libname}
%doc libsidplay/AUTHORS libsidplay/ChangeLog libsidplay/README libsidplay/TODO
%{_libdir}/libsidplay2.so.%{spmajor}*

%files -n %{libname}-devel
%dir %{_includedir}/sidplay/
%{_includedir}/sidplay/*.h
%{_libdir}/libsidplay2.so
%{_libdir}/pkgconfig/libsidplay2.pc

%files -n %{libnamesu}
%doc libsidutils/AUTHORS libsidutils/ChangeLog libsidutils/README libsidutils/TODO
%{_libdir}/libsidutils.so.%{sumajor}*

%files -n %{develnamesu}
%dir %{_includedir}/sidplay/imp
%{_includedir}/sidplay/imp/*.h
%dir %{_includedir}/sidplay/utils/
%{_includedir}/sidplay/utils/*.h
%{_libdir}/libsidutils.so
%{_libdir}/pkgconfig/libsidutils*pc

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

