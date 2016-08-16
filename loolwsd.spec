%global            debug_package %{nil}
%global            libreoffice_version 5.2
Name:              loolwsd
Version:           1.9.0
Release:           1000.HDZ
Vendor:            Collabora
Summary:           LibreOffice On-Line WebSocket Daemon
License:           MPL
Url:               https://github.com/LibreOffice/online
# Sources manually packed
Source0:           online-master.tar.gz
# Shadow warnings as errors breaks the build
Patch0:            disable-shadow-errors.patch
BuildRequires:     libcap-devel
BuildRequires:     libpng-devel
BuildRequires:     poco-devel >= 1.7.1
BuildRequires:     libpcap
BuildRequires:     nodejs >= 4.4.7
BuildRequires:     nodejs-packaging
BuildRequires:     libreoffice%{libreoffice_version}
BuildRequires:     libreoffice%{libreoffice_version}-ure
BuildRequires:     libobasis%{libreoffice_version}-core
BuildRequires:     libreoffice%{libreoffice_version}-writer
BuildRequires:     libreoffice%{libreoffice_version}-impress
BuildRequires:     libobasis%{libreoffice_version}-graphicfilter
BuildRequires:     libreoffice%{libreoffice_version}-calc
BuildRequires:     libobasis%{libreoffice_version}-ooofonts
BuildRequires:     libobasis%{libreoffice_version}-images
BuildRequires:     libobasis%{libreoffice_version}-filter-data
BuildRequires:     libreoffice%{libreoffice_version}-draw
BuildRequires:     libreoffice%{libreoffice_version}-base
# Tied to LibreOffice version
Requires:          libreoffice%{libreoffice_version}
Requires:          libreoffice%{libreoffice_version}-ure
Requires:          libobasis%{libreoffice_version}-core
Requires:          libreoffice%{libreoffice_version}-writer
Requires:          libreoffice%{libreoffice_version}-impress
Requires:          libobasis%{libreoffice_version}-graphicfilter
Requires:          libreoffice%{libreoffice_version}-calc
Requires:          libobasis%{libreoffice_version}-ooofonts
Requires:          libobasis%{libreoffice_version}-images
Requires:          libobasis%{libreoffice_version}-filter-data
Requires:          libreoffice%{libreoffice_version}-draw
Requires:          libreoffice%{libreoffice_version}-base
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
Requires(post):    coreutils
Requires(post):    grep
Requires(post):    sed
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
  --with-lo-path=%{_libdir}/libreoffice \
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

%install
cd loolwsd
env BUILDING_FROM_RPMBUILD=yes make install DESTDIR=%{buildroot}
sed -i "s|ExecStart=/usr/bin/loolwsd --version --o:sys_template_path=/opt/lool/systemplate --o:lo_template_path=/opt/libreoffice%{libreoffice_version} --o:child_root_path=/opt/lool/child-roots --o:file_server_root_path=/usr/share/loolwsd|ExecStart=/usr/bin/loolwsd --version --o:sys_template_path=/opt/lool/systemplate --o:lo_template_path=/opt/libreoffice%{libreoffice_version} --o:child_root_path=/opt/lool/child-roots --o:file_server_root_path=/usr/share/loolwsd --o:admin_console.username=admin --o:admin_console.password=admin|" loolwsd.service

%__install -D -m 444 loolwsd.service %{buildroot}%{_unitdir}/loolwsd.service
install -d -m 755 %{buildroot}/var/adm/fillup-templates
install -D -m 644 sysconfig.loolwsd %{buildroot}/etc/sysconfig/loolwsd
mkdir -p %{buildroot}/etc/cron.d
echo "#Remove old tiles once every 10 days at midnight" > %{buildroot}/etc/cron.d/loolwsd.cron
echo "0 0 */1 * * root find /var/cache/loolwsd -name \"*.png\" -a -atime +10 -exec rm {} \;" >> %{buildroot}/etc/cron.d/loolwsd.cron

# Mangling paths for LibreOffice
%{__sed} -i 's/\/opt\/collaboraoffice5.1/\/opt\/libreoffice%{libreoffice_version}/g' %{buildroot}/etc/loolwsd/loolwsd.xml
%{__sed} -i 's/\/usr\/local\/lib \/opt\/poco\/lib/\/usr\/local\/lib \/usr\/lib64/g' %{buildroot}/usr/bin/loolwsd-systemplate-setup
%{__sed} -i 's/\/opt\/collaboraoffice5.1/\/opt\/libreoffice%{libreoffice_version}/g' %{buildroot}/usr/lib/systemd/system/loolwsd.service

# Removing rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolwsd
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolmap
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolforkit
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolmount
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/loolstress
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/looltool

cd ../loleaflet
mkdir -p %{buildroot}/usr/share/loolwsd/loleaflet
tar cf - . | (cd %{buildroot}/usr/share/loolwsd/loleaflet && tar xf -)

%check
cd loolwsd
# Play around with paths for tests
%{__sed} -i 's/--o:storage\.filesystem\[@allow\]=true \\/--o:storage\.filesystem\[@allow\]=true --o:ssl\.cert_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/cert.pem" --o:ssl\.key_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/key.pem" --o:ssl\.ca_file_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/etc\/loolwsd\/ca-chain.cert.pem" --o:tile_cache_path="\/home\/%(echo $USER)\/rpmbuild\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}\/test\/cache" \\/g' test/run_unit.sh
%{__mkdir_p} $RPM_BUILD_ROOT/test/cache
env BUILDING_FROM_RPMBUILD=yes make check

%pre
getent group lool >/dev/null || groupadd -r lool
getent passwd lool >/dev/null || useradd -g lool -r lool

%post
setcap cap_fowner,cap_mknod,cap_sys_chroot=ep /usr/bin/loolforkit
setcap cap_sys_admin=ep /usr/bin/loolmount

mkdir -p /var/cache/loolwsd && chown lool:lool /var/cache/loolwsd
rm -rf /var/cache/loolwsd/*

loroot=`rpm -ql libreoffice%{libreoffice_version} | grep '/soffice$' | sed -e 's-/program/soffice--'`
loolparent=`cd ${loroot} && cd .. && /bin/pwd`

rm -rf ${loolparent}/lool
mkdir -p ${loolparent}/lool/child-roots
chown lool:lool ${loolparent}/lool
chown lool:lool ${loolparent}/lool/child-roots

su lool -c "loolwsd-systemplate-setup ${loolparent}/lool/systemplate ${loroot} >/dev/null 2>&1"

%systemd_post loolwsd.service

%preun
%systemd_preun loolwsd.service

%postun
%systemd_postun loolwsd.service

%files
%{_bindir}/loolwsd
%{_bindir}/loolwsd-systemplate-setup
%{_bindir}/loolmap
%{_bindir}/loolforkit
%{_bindir}/loolmount
%{_bindir}/loolstress
%{_bindir}/looltool
%{_datadir}/%{name}/discovery.xml
%{_datadir}/%{name}/robots.txt
%{_datadir}/%{name}/loleaflet
%{_unitdir}/loolwsd.service
%config(noreplace) %{_sysconfdir}/sysconfig/loolwsd
%config(noreplace) %{_sysconfdir}/cron.d/loolwsd.cron
%config(noreplace) %{_sysconfdir}/%{name}/loolwsd.xml
%config(noreplace) %attr(400, lool, lool) %{_sysconfdir}/%{name}/key.pem
%config(noreplace) %{_sysconfdir}/%{name}/cert.pem
%config(noreplace) %{_sysconfdir}/%{name}/ca-chain.cert.pem
%doc README

%changelog
* Wed Aug 10 2016 Hugo De Zela <hugodz@winet.com.pe>
- Version 1.9.0
- Based on https://github.com/LibreOffice/online/blob/master/loolwsd/loolwsd.spec.in
