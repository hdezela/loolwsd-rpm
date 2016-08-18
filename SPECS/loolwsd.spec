# This package is highly experimental
# I've had to hack around various things to get it to build
# All tests don't seem to work inside the rpmbuild environment
# Maybe someone with mock experience can lend a hand
# https://github.com/hdezela/loolwsd-rpm

%global            debug_package %{nil}
# Office information (depending on what/where it is installed)
%global            office_pkgname libreoffice
%global            office_version 5.2
%global            office_fulname %{office_pkgname}%{office_version}
%global            office_instdir %{_libdir}/%{office_pkgname}
Name:              loolwsd
Version:           1.9.0
Release:           1000.HDZ
Vendor:            Collabora
Summary:           LibreOffice On-Line WebSocket Daemon
License:           MPL
Url:               https://github.com/LibreOffice/online
# Sources manually packed
Source0:           online-master.tar.gz
# Files missing from the loleaflet dist that are nonetheless required
Source1:           loleaflet-missing.tar.xz
# Shadow warnings as errors breaks the build
Patch0:            disable-shadow-errors.patch
# There's a lot of extraneous stuff that triggers incorrect autoreq/autoprov
AutoReqProv:       no
# Npm requires tested manually since most aren't installed through RPM/YUM/DNF
BuildRequires:     libcap-devel
BuildRequires:     libpng-devel
BuildRequires:     poco-devel >= 1.7.1
BuildRequires:     libpcap
BuildRequires:     nodejs >= 4.4.7
BuildRequires:     nodejs-packaging
BuildRequires:     python
BuildRequires:     python-polib
# It needs to be able to find libreoffice for compiling
BuildRequires:     %{office_fulname}
BuildRequires:     %{office_fulname}-ure
BuildRequires:     %{office_pkgname}-core
BuildRequires:     %{office_fulname}-writer
BuildRequires:     %{office_fulname}-impress
BuildRequires:     %{office_pkgname}-graphicfilter
BuildRequires:     %{office_fulname}-calc
BuildRequires:     %{office_fulname}-draw
BuildRequires:     %{office_fulname}-base
# Tied to LibreOffice version
Requires:          %{office_fulname}
Requires:          %{office_fulname}-ure
Requires:          %{office_pkgname}-core
Requires:          %{office_fulname}-writer
Requires:          %{office_fulname}-impress
Requires:          %{office_pkgname}-graphicfilter
Requires:          %{office_fulname}-calc
Requires:          %{office_fulname}-draw
Requires:          %{office_fulname}-base
Requires:          systemd
Requires:          expat keyutils-libs
Requires:          krb5-libs
Requires:          libattr
Requires:          libcap
Requires:          libcom_err
Requires:          libgcc
Requires:          libpng
Requires:          libselinux
Requires:          openssl-libs
Requires:          pcre
Requires:          xz-libs
Requires:          zlib
Requires:          poco-crypto >= 1.7.1
Requires:          poco-foundation >= 1.7.1
Requires:          poco-json >= 1.7.1
Requires:          poco-net >= 1.7.1
Requires:          poco-netssl >= 1.7.1
Requires:          poco-util >= 1.7.1
Requires:          poco-xml >= 1.7.1
Requires:          %{_sbindir}/groupadd
Requires:          %{_sbindir}/useradd
Requires:          coreutils
Requires:          grep
Requires:          sed
Requires:          libcap
Provides:          loolwsd
Provides:          loleaflet
%description
%{summary}.

%prep
# Test for npm and dependencies in case they're not from RPMs (There has to be a better way than this...)
echo "Test for required npm dependencies"
# Test if npm is installed
if test -f /usr/bin/npm
then
	echo "Found npm, continuing"
else
	echo "npm is required for build"
	exit -1
fi
# Test if jake is installed
if test -d /usr/lib/node_modules/jake
then
	echo "Found npm(jake), continuing"
else
	if test -d /usr/lib64/node_modules/jake
	then
		echo "Found npm(jake), continuing"
	else
		echo "npm(jake) is required for build"
		exit -1
	fi
fi
# Test if browserify is installed
if test -d /usr/lib/node_modules/browserify
then
	echo "Found npm(browserify), continuing"
else
	if test -d /usr/lib64/node_modules/browserify
	then
		echo "Found npm(browserify), continuing"
	else
		echo "npm(browserify) is required for build"
		exit -1
	fi
fi
# Test if shrinkpack is installed
if test -d /usr/lib/node_modules/shrinkpack
then
	echo "Found npm(shrinkpack), continuing"
else
	if test -d /usr/lib64/node_modules/shrinkpack
	then
		echo "Found npm(shrinkpack), continuing"
	else
		echo "npm(shrinkpack) is required for build"
		exit -1
	fi
fi
# Test if shrinkwrap is installed
if test -d /usr/lib/node_modules/shrinkwrap
then
	echo "Found npm(shrinkwrap), continuing"
else
	if test -d /usr/lib64/node_modules/shrinkwrap
	then
		echo "Found npm(shrinkwrap), continuing"
	else
		echo "npm(shrinkwrap) is required for build"
		exit -1
	fi
fi

# Due to the way npm behaves inside rpmbuild, we need connectivity (Or maybe I just can't get it to work the way it should)
echo "Test for connectivity"
wget -q --tries=3 --timeout=20 --spider http://google.com > /dev/null
if [[ $? -eq 0 ]]; then
	echo "Online, continuing"
else
	echo "Connectivity is required for build"
	exit -1
fi

# Now we can really begin
%setup -q -n online-master
%patch0 -p1 -b .shadow

cd loolwsd
%{__libtoolize}
%{__aclocal} -I m4
autoreconf -vif
%{__automake} --add-missing
autoheader

%build
cd loolwsd
%configure \
  --with-lokit-path=bundled/include \
  --with-lo-path=%{office_instdir} \
  --enable-debug \
  --with-poco-libs=%{_libdir} \
  --with-poco-includes=%{_includedir} \
  --with-libpng-libs=%{_libdir} \
  --with-libpng-includes=%{_includedir}

# Build loolwsd
env BUILDING_FROM_RPMBUILD=yes make %{?_smp_mflags}

# Build loleaflet
cd ../loleaflet
npm update
npm shrinkwrap --dev
shrinkpack
make debug
util/po2json.py --quiet po/*.po
mv po/*.json dist/l10n
util/po2json.py --quiet po/styles/*.po
mkdir -p dist/l10n/styles/
mv po/styles/*.json dist/l10n/styles/

%install
cd loolwsd
env BUILDING_FROM_RPMBUILD=yes make install DESTDIR=%{buildroot}

%__install -D -m 444 loolwsd.service %{buildroot}%{_unitdir}/loolwsd.service
install -D -m 644 sysconfig.loolwsd %{buildroot}/etc/sysconfig/loolwsd
%{__mkdir_p} %{buildroot}/etc/cron.d
echo "#Remove old tiles once every 10 days at midnight" > %{buildroot}/etc/cron.d/loolwsd.cron
echo "0 0 */1 * * find /var/cache/loolwsd -name \"*.png\" -a -atime +10 -exec rm {} \;" >> %{buildroot}/etc/cron.d/loolwsd.cron

# Removing rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolwsd
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolmap
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolforkit
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolmount
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolstress
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/looltool

# Installing loleaflet
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/file_root/loleaflet
%{__mv} %{buildroot}/%{_datadir}/%{name}/discovery.xml %{buildroot}%{_datadir}/%{name}/file_root/discovery.xml
%{__mv} %{buildroot}/%{_datadir}/%{name}/robots.txt %{buildroot}%{_datadir}/%{name}/file_root/robots.txt
%{__mv} %{_builddir}/online-master/loleaflet/dist %{buildroot}%{_datadir}/%{name}/file_root/loleaflet

# Repairing loleaflet (files missing from dist that are required)
tar -xf %{SOURCE1} -C %{buildroot}%{_datadir}/%{name}/file_root/loleaflet/dist

# Setting up directories
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/jails
%{__mkdir_p} %{buildroot}/%{_localstatedir}/cache/%{name}

# Backing up original loolwsd.xml
cp %{buildroot}/etc/%{name}/loolwsd.xml %{buildroot}/etc/%{name}/loolwsd.xml.dist

# Mangling paths for LibreOffice and CentOS/Fedora
%{__sed} -i 's|relative="true"|relative="false"|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</tile_cache_path>|/var/cache/loolwsd</tile_cache_path>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</sys_template_path>|%{_datadir}/%{name}/systemplate</sys_template_path>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</lo_template_path>|%{office_instdir}</lo_template_path>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</child_root_path>|%{_datadir}/%{name}/jails</child_root_path>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</file_server_root_path>|%{_datadir}/%{name}/file_root</file_server_root_path>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</username>|admin</username>|g' %{buildroot}/etc/%{name}/loolwsd.xml
%{__sed} -i 's|</password>|admin</password>|g' %{buildroot}/etc/%{name}/loolwsd.xml

%{__sed} -i 's|/usr/local/lib /opt/poco/lib|/usr/lib64|g' %{buildroot}/usr/bin/loolwsd-systemplate-setup

%{__sed} -i 's|ExecStart=/usr/bin/loolwsd --version --o:sys_template_path=/opt/lool/systemplate --o:lo_template_path=/opt/collaboraoffice5.1 --o:child_root_path=/opt/lool/child-roots --o:file_server_root_path=/usr/share/loolwsd|ExecStart=/usr/bin/loolwsd|g' %{buildroot}/usr/lib/systemd/system/loolwsd.service

%check
# ---  Tests disabled, don't work within rpmbuild ---
#cd loolwsd
# Play around with paths for tests
#%{__sed} -i 's/--o:storage\.filesystem\[@allow\]=true \\/--o:storage\.filesystem\[@allow\]=true --o:ssl\.cert_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/cert.pem" --o:ssl\.key_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/key.pem" --o:ssl\.ca_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/ca-chain.cert.pem" --o:tile_cache_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/test\/cache" \\/g' test/run_unit.sh
#%{__mkdir_p} $RPM_BUILD_ROOT/test/cache
#env BUILDING_FROM_RPMBUILD=yes make check

%pre
getent group lool >/dev/null || groupadd -r lool
getent passwd lool >/dev/null || useradd -g lool -r lool

%post
setcap cap_fowner,cap_mknod,cap_sys_chroot=ep /usr/bin/loolforkit
setcap cap_sys_admin=ep /usr/bin/loolmount

systemplatepath=%{_datadir}/%{name}/systemplate
officedir=%{office_instdir}

su lool -c "/usr/bin/loolwsd-systemplate-setup ${systemplatepath} ${officedir} >/dev/null 2>&1"
rm -rf %{_datadir}/%{name}/systemplate%{_libdir}/%{office_pkgname}

%systemd_post loolwsd.service

    cat <<BANNER
----------------------------------------------------------------------

SSL Key files locations:
     \etc\loolwsd\key.pem
	\etc\loolwsd\ca-chain.cert.pem
	\etc\loolwsd\cert.pem

Some paths have been changed, take a look at:
     \etc\loolwsd\loolwsd.xml

Default admin credentials:
     user admin
	pass admin

Debug level is set to trace, find "level" in:
	\etc\loolwsd\loolwsd.xml

----------------------------------------------------------------------
BANNER

%preun
%systemd_preun loolwsd.service

%postun
%systemd_postun loolwsd.service

rm -rf %{_datadir}/%{name}

%files
%{_bindir}/loolwsd
%{_bindir}/loolwsd-systemplate-setup
%{_bindir}/loolmap
%{_bindir}/loolforkit
%{_bindir}/loolmount
%{_bindir}/loolstress
%{_bindir}/looltool
%attr(-, lool, lool) %{_datadir}/%{name}
%attr(-, lool, lool) %{_localstatedir}/cache/%{name}
%{_unitdir}/loolwsd.service
%config(noreplace) %{_sysconfdir}/sysconfig/loolwsd
%config(noreplace) %{_sysconfdir}/cron.d/loolwsd.cron
%config(noreplace) %{_sysconfdir}/%{name}/loolwsd.xml
%{_sysconfdir}/%{name}/loolwsd.xml.dist
%config(noreplace) %attr(400, lool, lool) %{_sysconfdir}/%{name}/key.pem
%config(noreplace) %{_sysconfdir}/%{name}/cert.pem
%config(noreplace) %{_sysconfdir}/%{name}/ca-chain.cert.pem
%doc README

%changelog
* Wed Aug 10 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 1.9.0
- Based on https://github.com/LibreOffice/online/blob/master/loolwsd/loolwsd.spec.in
