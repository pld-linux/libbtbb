#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Bluetooth baseband decoding library
Summary(pl.UTF-8):	Biblioteka dekodowania warstwy baseband Bluetooth
Name:		libbtbb
%define	tag_ver	2020-12-R1
Version:	%(echo %{tag_ver} | tr - _)
Release:	
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/greatscottgadgets/libbtbb/releases
Source0:	https://github.com/greatscottgadgets/libbtbb/archive/%{tag_ver}/%{name}-%{tag_ver}.tar.gz
# Source0-md5:	d1c01829b1f32926065e72095641a6be
Patch0:		%{name}-python.patch
URL:		https://github.com/greatscottgadgets/libbtbb
BuildRequires:	cmake >= 2.8
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the Bluetooth baseband decoding library, forked from the
GR-Bluetooth project. It can be used to extract Bluetooth packet and
piconet information from Ubertooth devices as well as
GR-Bluetooth/USRP.

%description -l pl.UTF-8
Biblioteka dekodująca warstwę baseband Bluetooth, odgałęziona z
projektu GR-Bluetooth. Może być używana do wydobywania pakietów
Bluetooth i informacji piconet z urządzeń Ubertooth oraz
GR-Bluetooth/USRP.

%package devel
Summary:	Header files for libbtbb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbtbb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libbtbb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbtbb.

%package static
Summary:	Static libbtbb library
Summary(pl.UTF-8):	Statyczna biblioteka libbtbb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbtbb library.

%description static -l pl.UTF-8
Statyczna biblioteka libbtbb.

%package python
Summary:	Python tools for working with pcap files produced via libbtbb
Summary(pl.UTF-8):	Narzędzia pythonowe do pracy z plikami pcap tworzonymi przy pomocy libbtbb
Group:		Development/Tools
BuildArch:	noarch

%description python
Supplemental tools for working with pcap files produced via libbtbb.

%description python -l pl.UTF-8
Dodatkowe narzędzia do pracy z plikami pcap tworzonymi przy pomocy
libbtbb.

%prep
%setup -q -n %{name}-%{tag_ver}
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	python/pcaptools/btaptap

%{__sed} -i -e 's, --root, --install-purelib=%{py3_sitescriptdir} &,' \
	python/pcaptools/CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	%{?with_static_libs:-DBUILD_STATIC_LIB=ON} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libbtbb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtbb.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtbb.so
%{_includedir}/btbb.h
%{_pkgconfigdir}/libbtbb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbtbb.a
%endif

%files python
%defattr(644,root,root,755)
%doc python/pcaptools/README
%attr(755,root,root) %{_bindir}/btaptap
%{py3_sitescriptdir}/pcapdump
%{py3_sitescriptdir}/pcapdump-*.egg-info
