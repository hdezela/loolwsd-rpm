%global            debug_package %{nil}
%global apiversion 0.4

Name:		libwps
Version:	0.4.3
Release:           1000.HDZ
Summary:	A library for import of Microsoft Works documents
License:	LGPLv2+ or MPLv2.0
URL:		http://libwps.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
BuildRequires:	doxygen
BuildRequires:	help2man
BuildRequires:	pkgconfig(librevenge-0.0)
%description
%{summary}.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package tools
Summary:	Tools to transform Microsoft Works documents into other formats
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description tools
%{summary}.

%package doc
Summary:	Documentation of %{name} API
BuildArch:	noarch
%description doc
%{summary}.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror --with-sharedptr=c++11
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR="%{buildroot}" 
rm -f %{buildroot}%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}%{_defaultdocdir}/%{name}

export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in wks2csv wks2raw wks2text wps2html wps2raw wps2text; do
    help2man -S %{name} -N -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 wks2*.1 wps2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc CREDITS NEWS README
%license COPYING.LGPL COPYING.MPL
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc HACKING
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files tools
%{_bindir}/wks2csv
%{_bindir}/wks2raw
%{_bindir}/wks2text
%{_bindir}/wps2html
%{_bindir}/wps2raw
%{_bindir}/wps2text
%{_mandir}/man1/wks2csv.1*
%{_mandir}/man1/wks2raw.1*
%{_mandir}/man1/wks2text.1*
%{_mandir}/man1/wps2html.1*
%{_mandir}/man1/wps2raw.1*
%{_mandir}/man1/wps2text.1*

%files doc
%license COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html

%changelog
* Mon Aug 08 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 0.4.3
- Based on libwps-0.4.3-1.fc24.src
