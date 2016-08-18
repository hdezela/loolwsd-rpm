%global            debug_package %{nil}
%global apiversion 0.5

Name: libcmis
Version: 0.5.1
Release:           1000.HDZ
Summary: A C++ client library for CM interfaces
License: GPLv2+ or LGPLv2+ or MPLv1.1
URL: https://github.com/tdf/libcmis
Source0: https://github.com/tdf/libcmis/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires: boost-devel
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: xmlto
Patch0: 0001-Add-new-Google-Drive-OAuth-2.0-login-procedure.patch
Patch1: 0002-Add-new-mokup-login-pages.patch
Patch2: 0003-Fix-test-in-test-factory.patch
Patch3: 0004-Fix-test-in-test-gdrive.patch
Patch4: 0005-Fix-test-in-test-onedrive.patch
%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package tools
Summary: Command line tool to access CMIS
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tools
%{summary}.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror \
    DOCBOOK2MAN='xmlto man'
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS NEWS
%license COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-c-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_includedir}/%{name}-c-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/%{name}-c-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_libdir}/pkgconfig/%{name}-c-%{apiversion}.pc

%files tools
%{_bindir}/cmis-client
%{_mandir}/man1/cmis-client.1*

%changelog
* Mon Aug 08 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 0.5.1
- Based on libcmis-0.5.1-2.fc25.src
