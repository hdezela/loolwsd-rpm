%global            debug_package %{nil}
%global apiversion 0.0

Name: libpagemaker
Version: 0.0.3
Release:           1000.HDZ
Summary: A library for import of Adobe PageMaker documents
License: MPLv2.0
URL: http://wiki.documentfoundation.org/DLP/Libraries/libpagemaker
Source0: http://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz
BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: help2man
BuildRequires: pkgconfig(librevenge-0.0)
%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch
%description doc
%{summary}.

%package tools
Summary: Tools to transform Adobe PageMaker documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tools
%{summary}.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in pmd2raw pmd2svg; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 pmd2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS
%license COPYING
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING
%doc docs/doxygen/html

%files tools
%{_bindir}/pmd2raw
%{_bindir}/pmd2svg
%{_mandir}/man1/pmd2raw.1*
%{_mandir}/man1/pmd2svg.1*

%changelog
* Mon Aug 08 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 0.0.3
- Based on libpagemaker-0.0.3-1.fc25.src
