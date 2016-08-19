Name:              poco
Version:           1.7.4
Release:           1000.HDZ
Summary:           C++ class libraries for network-centric applications
Group:             Development/Libraries
License:           Boost
URL:               http://pocoproject.org
Source0:           https://github.com/pocoproject/%{name}/archive/%{name}-%{name}-%{version}.tar.gz
Patch3:            disable-tests.patch
Patch4:            sqlite-no-busy-snapshot.patch
Patch5:            ppc64le.patch
BuildRequires:     openssl-devel
BuildRequires:     libiodbc-devel
BuildRequires:     mysql-devel
BuildRequires:     zlib-devel
BuildRequires:     pcre-devel
BuildRequires:     sqlite-devel
BuildRequires:     expat-devel
BuildRequires:     libtool-ltdl-devel
BuildRequires:     mongodb-devel
Provides:          bundled(pcre) = 8.35
%description
%{summary}.

%package           foundation
Summary:           The Foundation POCO component
Group:             System Environment/Libraries
%description       foundation
%{summary}.

%package           xml
Summary:           The XML POCO component
Group:             System Environment/Libraries
%description       xml
%{summary}.

%package           util
Summary:           The Util POCO component
Group:             System Environment/Libraries
%description       util
%{summary}.

%package           net
Summary:           The Net POCO component
Group:             System Environment/Libraries
%description       net
%{summary}.

%package           crypto
Summary:           The Crypto POCO component
Group:             System Environment/Libraries
%description       crypto
%{summary}.

%package           netssl
Summary:           The NetSSL POCO component
Group:             System Environment/Libraries
%description       netssl
%{summary}.

%package           data
Summary:           The Data POCO component
Group:             System Environment/Libraries
%description       data
%{summary}.

%package           sqlite
Summary:           The Data/SQLite POCO component
Group:             System Environment/Libraries
%description       sqlite
%{summary}.

%package           odbc
Summary:           The Data/ODBC POCO component
Group:             System Environment/Libraries
%description       odbc
%{summary}.

%package           mysql
Summary:           The Data/MySQL POCO component
Group:             System Environment/Libraries
%description       mysql
%{summary}.

%package           zip
Summary:           The Zip POCO component
Group:             System Environment/Libraries
%description       zip
%{summary}.

%package           json
Summary:           The JSON POCO component
Group:             System Environment/Libraries
%description       json
%{summary}.

%package           mongodb
Summary:           The MongoDB POCO component
Group:             System Environment/Libraries
%description       mongodb
%{summary}.

%package           pagecompiler
Summary:           The PageCompiler POCO component
Group:             System Environment/Libraries
%description       pagecompiler
%{summary}.

%package           debug
Summary:           Debug builds of the POCO libraries
Group:             Development/Libraries
%description       debug
%{summary}.

%package           devel
Summary:           Headers for developing programs that will use POCO
Group:             Development/Libraries
Requires:          poco-debug%{?_isa} = %{version}-%{release}
Requires:          poco-foundation%{?_isa} = %{version}-%{release}
Requires:          poco-xml%{?_isa} = %{version}-%{release}
Requires:          poco-util%{?_isa} = %{version}-%{release}
Requires:          poco-net%{?_isa} = %{version}-%{release}
Requires:          poco-crypto%{?_isa} = %{version}-%{release}
Requires:          poco-netssl%{?_isa} = %{version}-%{release}
Requires:          poco-data%{?_isa} = %{version}-%{release}
Requires:          poco-sqlite%{?_isa} = %{version}-%{release}
Requires:          poco-odbc%{?_isa} = %{version}-%{release}
Requires:          poco-mysql%{?_isa} = %{version}-%{release}
Requires:          poco-zip%{?_isa} = %{version}-%{release}
Requires:          poco-json%{?_isa} = %{version}-%{release}
Requires:          poco-mongodb%{?_isa} = %{version}-%{release}
Requires:          poco-pagecompiler%{?_isa} = %{version}-%{release}
Requires:          zlib-devel
Requires:          expat-devel
%description       devel
%{summary}.

%package           doc
Summary:           The POCO API reference documentation
Group:             Documentation
%description       doc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch3 -p1
%patch4 -p1
%patch5 -p1

/bin/sed -i.orig -e 's|$(INSTALLDIR)/lib\b|$(INSTALLDIR)/%{_lib}|g' Makefile
/bin/sed -i.orig -e 's|ODBCLIBDIR = /usr/lib\b|ODBCLIBDIR = %{_libdir}|g' Data/ODBC/Makefile Data/ODBC/testsuite/Makefile
/bin/sed -i.orig -e 's|flags=""|flags="%{optflags}"|g' configure
/bin/sed -i.orig -e 's|SHAREDOPT_LINK  = -Wl,-rpath,$(LIBPATH)|SHAREDOPT_LINK  =|g' build/config/Linux
/bin/sed -i.orig -e 's|#endif|#define POCO_UNBUNDLED 1\n\n#endif|g' Foundation/include/Poco/Config.h
/bin/sed -i.orig -e 's|"Poco/zlib.h"|<zlib.h>|g' Zip/src/ZipStream.cpp
/bin/sed -i.orig -e 's|PDF|Data/SQLite PDF|' travis/runtests.sh

rm -f Foundation/src/MSG00001.bin
rm -f Foundation/include/Poco/zconf.h
rm -f Foundation/include/Poco/zlib.h
rm -f Foundation/src/adler32.c
rm -f Foundation/src/compress.c
rm -f Foundation/src/crc32.c
rm -f Foundation/src/crc32.h
rm -f Foundation/src/deflate.c
rm -f Foundation/src/deflate.h
rm -f Foundation/src/gzguts.h
rm -f Foundation/src/gzio.c
rm -f Foundation/src/infback.c
rm -f Foundation/src/inffast.c
rm -f Foundation/src/inffast.h
rm -f Foundation/src/inffixed.h
rm -f Foundation/src/inflate.c
rm -f Foundation/src/inflate.h
rm -f Foundation/src/inftrees.c
rm -f Foundation/src/inftrees.h
rm -f Foundation/src/trees.c
rm -f Foundation/src/trees.h
rm -f Foundation/src/zconf.h
rm -f Foundation/src/zlib.h
rm -f Foundation/src/zutil.c
rm -f Foundation/src/zutil.h
rm -f Foundation/src/pcre_byte_order.c
rm -f Foundation/src/pcre_chartables.c
rm -f Foundation/src/pcre_compile.c
rm -f Foundation/src/pcre_config.c
rm -f Foundation/src/pcre_dfa_exec.c
rm -f Foundation/src/pcre_exec.c
rm -f Foundation/src/pcre_fullinfo.c
rm -f Foundation/src/pcre_get.c
rm -f Foundation/src/pcre_globals.c
rm -f Foundation/src/pcre_jit_compile.c
rm -f Foundation/src/pcre_maketables.c
rm -f Foundation/src/pcre_newline.c
rm -f Foundation/src/pcre_ord2utf8.c
rm -f Foundation/src/pcre_refcount.c
rm -f Foundation/src/pcre_string_utils.c
rm -f Foundation/src/pcre_study.c
rm -f Foundation/src/pcre_try_flipped.c
rm -f Foundation/src/pcre_valid_utf8.c
rm -f Foundation/src/pcre_version.c
rm -f Foundation/src/pcre_xclass.c
rm -f Data/SQLite/src/sqlite3.h
rm -f Data/SQLite/src/sqlite3.c
rm -f XML/include/Poco/XML/expat.h
rm -f XML/include/Poco/XML/expat_external.h
rm -f XML/src/ascii.h
rm -f XML/src/asciitab.h
rm -f XML/src/expat_config.h
rm -f XML/src/iasciitab.h
rm -f XML/src/internal.h
rm -f XML/src/latin1tab.h
rm -f XML/src/nametab.h
rm -f XML/src/utf8tab.h
rm -f XML/src/xmlparse.cpp
rm -f XML/src/xmlrole.c
rm -f XML/src/xmlrole.h
rm -f XML/src/xmltok.c
rm -f XML/src/xmltok.h
rm -f XML/src/xmltok_impl.c
rm -f XML/src/xmltok_impl.h
rm -f XML/src/xmltok_ns.c

%build
./configure \
  --prefix=%{_prefix} \
  --everything \
  --omit=PDF,CppParser \
  --unbundled \
  --no-samples \
  --include-path=%{_includedir}/libiodbc \
  --library-path=%{_libdir}/mysql

make -s %{?_smp_mflags} STRIP=/bin/true

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_prefix}/include/Poco/Config.h.orig

%check
LIBPATH="$(pwd)/lib/Linux/$(uname -m)"
export LD_LIBRARY_PATH=$LIBPATH
POCO_BASE="$(pwd)"
$POCO_BASE/travis/runtests.sh

%post foundation -p /sbin/ldconfig
%postun foundation -p /sbin/ldconfig

%post xml -p /sbin/ldconfig
%postun xml -p /sbin/ldconfig

%post util -p /sbin/ldconfig
%postun util -p /sbin/ldconfig

%post net -p /sbin/ldconfig
%postun net -p /sbin/ldconfig

%post crypto -p /sbin/ldconfig
%postun crypto -p /sbin/ldconfig

%post netssl -p /sbin/ldconfig
%postun netssl -p /sbin/ldconfig

%post data -p /sbin/ldconfig
%postun data -p /sbin/ldconfig

%post sqlite -p /sbin/ldconfig
%postun sqlite -p /sbin/ldconfig

%post odbc -p /sbin/ldconfig
%postun odbc -p /sbin/ldconfig

%post mysql -p /sbin/ldconfig
%postun mysql -p /sbin/ldconfig

%post zip -p /sbin/ldconfig
%postun zip -p /sbin/ldconfig

%post json -p /sbin/ldconfig
%postun json -p /sbin/ldconfig

%post mongodb -p /sbin/ldconfig
%postun mongodb -p /sbin/ldconfig

%post debug -p /sbin/ldconfig
%postun debug -p /sbin/ldconfig

%files foundation
%{_libdir}/libPocoFoundation.so.*

%files xml
%{_libdir}/libPocoXML.so.*

%files util
%{_libdir}/libPocoUtil.so.*

%files net
%{_libdir}/libPocoNet.so.*

%files crypto
%{_libdir}/libPocoCrypto.so.*

%files netssl
%{_libdir}/libPocoNetSSL.so.*

%files data
%{_libdir}/libPocoData.so.*

%files sqlite
%{_libdir}/libPocoDataSQLite.so.*

%files odbc
%{_libdir}/libPocoDataODBC.so.*

%files mysql
%{_libdir}/libPocoDataMySQL.so.*

%files zip
%{_libdir}/libPocoZip.so.*

%files json
%{_libdir}/libPocoJSON.so.*

%files mongodb
%{_libdir}/libPocoMongoDB.so.*

%files pagecompiler
%{_bindir}/cpspc
%{_bindir}/f2cpsp

%files debug
%{_libdir}/libPocoFoundationd.so.*
%{_libdir}/libPocoXMLd.so.*
%{_libdir}/libPocoUtild.so.*
%{_libdir}/libPocoNetd.so.*
%{_libdir}/libPocoCryptod.so.*
%{_libdir}/libPocoNetSSLd.so.*
%{_libdir}/libPocoDatad.so.*
%{_libdir}/libPocoDataSQLited.so.*
%{_libdir}/libPocoDataODBCd.so.*
%{_libdir}/libPocoDataMySQLd.so.*
%{_libdir}/libPocoZipd.so.*
%{_libdir}/libPocoJSONd.so.*
%{_libdir}/libPocoMongoDBd.so.*
%{_bindir}/cpspcd
%{_bindir}/f2cpspd

%files devel
%{_includedir}/Poco
%{_libdir}/libPocoFoundation.so
%{_libdir}/libPocoFoundationd.so
%{_libdir}/libPocoXML.so
%{_libdir}/libPocoXMLd.so
%{_libdir}/libPocoUtil.so
%{_libdir}/libPocoUtild.so
%{_libdir}/libPocoNet.so
%{_libdir}/libPocoNetd.so
%{_libdir}/libPocoCrypto.so
%{_libdir}/libPocoCryptod.so
%{_libdir}/libPocoNetSSL.so
%{_libdir}/libPocoNetSSLd.so
%{_libdir}/libPocoData.so
%{_libdir}/libPocoDatad.so
%{_libdir}/libPocoDataSQLite.so
%{_libdir}/libPocoDataSQLited.so
%{_libdir}/libPocoDataODBC.so
%{_libdir}/libPocoDataODBCd.so
%{_libdir}/libPocoDataMySQL.so
%{_libdir}/libPocoDataMySQLd.so
%{_libdir}/libPocoZip.so
%{_libdir}/libPocoZipd.so
%{_libdir}/libPocoJSON.so
%{_libdir}/libPocoJSONd.so
%{_libdir}/libPocoMongoDB.so
%{_libdir}/libPocoMongoDBd.so

%files doc
%doc README NEWS LICENSE CONTRIBUTORS CHANGELOG doc/*

%changelog
* Wed Aug 10 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 1.7.4
- Based on poco-1.6.1-2.el7.src
