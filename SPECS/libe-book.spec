%global            debug_package %{nil}
%global            apiversion 0.1
Name:              libe-book
Version:           0.1.2
Release:           1000.HDZ
Summary:           A library for import of reflowable e-book formats
License:           MPLv2.0
URL:               https://sourceforge.net/projects/libebook/
Source0:           http://downloads.sourceforge.net/libebook/%{name}-%{version}.tar.xz
BuildRequires:     boost-devel
BuildRequires:     doxygen
BuildRequires:     gperf
BuildRequires:     help2man
BuildRequires:     pkgconfig(cppunit)
BuildRequires:     pkgconfig(icu-i18n)
BuildRequires:     pkgconfig(librevenge-0.0)
BuildRequires:     pkgconfig(libxml-2.0)
BuildRequires:     pkgconfig(zlib)
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
Summary: Tools to transform e-books into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tools
%{summary}.

%prep
%autosetup -p1

%build
export CPPFLAGS=-DBOOST_ERROR_CODE_HEADER_ONLY
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

export LD_LIBRARY_PATH=$(pwd)/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'convert e-book into HTML' -o ebook2html.1 ./src/conv/html/.libs/ebook2html
help2man -N -n 'convert e-book into plain text' -o ebook2text.1 ./src/conv/text/.libs/ebook2text
help2man -N -n 'debug the conversion library' -o ebook2raw.1 ./src/conv/raw/.libs/ebook2raw

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# TODO: drop on next update
rm -f %{buildroot}%{_datadir}/%{name}/*.css

mkdir -p %{buildroot}/%{_mandir}/man1
install -m 0644 ebook2*.1 %{buildroot}/%{_mandir}/man1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS NEWS README
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
%{_bindir}/ebook2raw
%{_bindir}/ebook2text
%{_bindir}/ebook2html
%{_mandir}/man1/ebook2html.1*
%{_mandir}/man1/ebook2raw.1*
%{_mandir}/man1/ebook2text.1*

%changelog
* Mon Aug 08 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 0.1.2
- Based on libe-book-0.1.2-12.fc25.src
