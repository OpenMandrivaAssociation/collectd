%define major 0
%define libname %mklibname collectdclient %{major}
%define develname %mklibname -d collectdclient

Summary:	Collects system information in RRD files
Name:		collectd
Version:	4.9.1
Release:	%mkrel 1
License:	GPLv2+
Group:		Monitoring
URL:		http://collectd.org/
Source0:	http://collectd.org/files/collectd-%{version}.tar.bz2
Source1:	%{name}-initscript
Source2:	%{name}.logrotate
Patch0:		collectd-path_fixes.diff
Patch1:		collectd-nut-2.2.x_fix.diff
Patch2:		collectd-libstatgrab_fix.diff
Patch3:		collectd-4.5.1-perl_fix.diff
BuildConflicts:	git
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	flex
BuildRequires:	iptables-devel
BuildRequires:	libdbi-devel
BuildRequires:	libesmtp-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libgnutls-devel
BuildRequires:	libhal-devel
BuildRequires:	libltdl-devel
BuildRequires:	libnotify-devel
BuildRequires:	libstatgrab-devel
BuildRequires:	libtool
BuildRequires:	libvirt-devel
BuildRequires:	libxml2-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	nut-devel
BuildRequires:	openipmi-devel
BuildRequires:	oping-devel
BuildRequires:	pcap-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	postgresql-devel
BuildRequires:	rrdtool-devel
Requires(pre):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The collectd daemon collects information about the system it is running on and
writes this information into special database files. These database files can
then be used to generate graphs of the collected data.

%package -n %{libname}
Summary:	Collects system information in RRD files
Group:		System/Libraries

%description -n %{libname}
The collectd daemon collects information about the system it is running on.
This package contains the shared libraries used by %{name}

%package -n %{develname}
Summary:        Collects system information in RRD files
Group:          Development/C 
Requires:       %{libname} = %{version}


%description -n %{develname}
The collectd daemon collects information about the system it is running on.
This package contains the development headers.

%prep

%setup -q
%patch0 -p1
%patch2 -p0
%patch3 -p0

%{_bindir}/find . -name Makefile.am -o -name Makefile.in | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\-Werror//g'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
%serverbuild
rm -f configure
libtoolize --copy --force --ltdl; aclocal; autoconf; automake --foreign --add-missing --copy; autoheader

# hack...
export PKG_CONFIG_PATH="./pkg-config"
mkdir -p pkg-config
cat > pkg-config/pthread.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: pthread
Description: Pthread
Version: 0.0.0
Libs: -L\${libdir} -lpthread
Cflags: -I\${includedir}
EOF

CFLAGS="%{optflags} -fPIC" ./configure \
    --host=%{_host} --build=%{_build} \
    --target=%{_target_platform} \
    --program-prefix=%{?_program_prefix} \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var/lib \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-apache --with-libcurl=%{_prefix} \
    --enable-apcups \
    --disable-apple_sensors \
    --enable-ascent \
    --enable-battery \
    --enable-cpu \
    --enable-cpufreq \
    --enable-csv \
    --enable-df \
    --enable-disk \
    --enable-dns --with-libpcap=%{_prefix} \
    --enable-email \
    --enable-entropy \
    --enable-exec \
    --enable-hddtemp \
    --enable-interface \
    --enable-iptables --with-libiptc=%{_prefix} \
    --enable-ipmi \
    --disable-ipvs \
    --enable-irq \
    --enable-libvirt \
    --enable-load \
    --enable-logfile \
    --enable-mbmon \
    --enable-memcached \
    --enable-memory \
    --enable-multimeter \
    --enable-mysql --with-libmysql=%{_prefix} \
    --disable-netlink \
    --enable-network \
    --enable-nfs \
    --enable-nginx --with-libcurl=%{_prefix} \
    --enable-ntpd \
    --enable-nut \
    --enable-perl --with-libperl=%{_prefix} --with-perl-bindings="INSTALLDIRS=vendor" \
    --enable-ping --with-liboping=%{_prefix} \
    --enable-postgresql \
    --enable-powerdns \
    --enable-processes \
    --enable-rrdtool --with-rrdtool=%{_prefix} \
    --enable-sensors--with-lm-sensors=%{_prefix} \
    --enable-serial \
    --enable-snmp --with-libnetsnmp \
    --enable-swap \
    --enable-syslog \
    --enable-tail \
    --disable-tape \
    --enable-tcpconns \
    --enable-teamspeak2 \
    --enable-unixsock \
    --enable-users \
    --enable-uuid \
    --enable-vmem \
    --enable-vserver \
    --enable-wireless \
    --disable-xmms \
    --with-libpthread=%{_prefix} \
    --with-libstatgrab=%{_prefix} \
    --disable-static \

 %make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/lib/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}/var/log/%{name}

%makeinstall_std

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

touch %{buildroot}/var/log/%{name}/%{name}.log

# cleanup
rm %{buildroot}%{_libdir}/collectd/*.la

%post
%create_ghostfile /var/log/%{name}/%{name}.log root root 644
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README ChangeLog TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/collectd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) %{_bindir}/collectd-nagios
%attr(0755,root,root) %{_sbindir}/collectd
%attr(0755,root,root) %{_sbindir}/collectdmon
%dir %{_libdir}/collectd
%attr(0755,root,root) %{_libdir}/collectd/apache.so
%attr(0755,root,root) %{_libdir}/collectd/apcups.so
%attr(0755,root,root) %{_libdir}/collectd/ascent.so
%attr(0755,root,root) %{_libdir}/collectd/battery.so
%attr(0755,root,root) %{_libdir}/collectd/bind.so
%attr(0755,root,root) %{_libdir}/collectd/conntrack.so
%attr(0755,root,root) %{_libdir}/collectd/contextswitch.so
%attr(0755,root,root) %{_libdir}/collectd/cpufreq.so
%attr(0755,root,root) %{_libdir}/collectd/cpu.so
%attr(0755,root,root) %{_libdir}/collectd/csv.so
%attr(0755,root,root) %{_libdir}/collectd/curl.so
%attr(0755,root,root) %{_libdir}/collectd/dbi.so
%attr(0755,root,root) %{_libdir}/collectd/df.so
%attr(0755,root,root) %{_libdir}/collectd/disk.so
%attr(0755,root,root) %{_libdir}/collectd/dns.so
%attr(0755,root,root) %{_libdir}/collectd/email.so
%attr(0755,root,root) %{_libdir}/collectd/entropy.so
%attr(0755,root,root) %{_libdir}/collectd/exec.so
%attr(0755,root,root) %{_libdir}/collectd/filecount.so
%attr(0755,root,root) %{_libdir}/collectd/fscache.so
%attr(0755,root,root) %{_libdir}/collectd/hddtemp.so
%attr(0755,root,root) %{_libdir}/collectd/interface.so
%attr(0755,root,root) %{_libdir}/collectd/ipmi.so
%attr(0755,root,root) %{_libdir}/collectd/iptables.so
%attr(0755,root,root) %{_libdir}/collectd/irq.so
%attr(0755,root,root) %{_libdir}/collectd/libvirt.so
%attr(0755,root,root) %{_libdir}/collectd/load.so
%attr(0755,root,root) %{_libdir}/collectd/logfile.so
%attr(0755,root,root) %{_libdir}/collectd/madwifi.so
%attr(0755,root,root) %{_libdir}/collectd/match_empty_counter.so
%attr(0755,root,root) %{_libdir}/collectd/match_hashed.so
%attr(0755,root,root) %{_libdir}/collectd/match_regex.so
%attr(0755,root,root) %{_libdir}/collectd/match_timediff.so
%attr(0755,root,root) %{_libdir}/collectd/match_value.so
%attr(0755,root,root) %{_libdir}/collectd/mbmon.so
%attr(0755,root,root) %{_libdir}/collectd/memcached.so
%attr(0755,root,root) %{_libdir}/collectd/memory.so
%attr(0755,root,root) %{_libdir}/collectd/multimeter.so
%attr(0755,root,root) %{_libdir}/collectd/mysql.so
%attr(0755,root,root) %{_libdir}/collectd/network.so
%attr(0755,root,root) %{_libdir}/collectd/nfs.so
%attr(0755,root,root) %{_libdir}/collectd/nginx.so
%attr(0755,root,root) %{_libdir}/collectd/notify_desktop.so
%attr(0755,root,root) %{_libdir}/collectd/notify_email.so
%attr(0755,root,root) %{_libdir}/collectd/ntpd.so
%attr(0755,root,root) %{_libdir}/collectd/nut.so
%attr(0755,root,root) %{_libdir}/collectd/olsrd.so
%attr(0755,root,root) %{_libdir}/collectd/openvpn.so
%attr(0755,root,root) %{_libdir}/collectd/perl.so
%attr(0755,root,root) %{_libdir}/collectd/ping.so
%attr(0755,root,root) %{_libdir}/collectd/postgresql.so
%attr(0755,root,root) %{_libdir}/collectd/powerdns.so
%attr(0755,root,root) %{_libdir}/collectd/processes.so
%attr(0755,root,root) %{_libdir}/collectd/protocols.so
%attr(0755,root,root) %{_libdir}/collectd/python.so
%attr(0755,root,root) %{_libdir}/collectd/rrdcached.so
%attr(0755,root,root) %{_libdir}/collectd/rrdtool.so
%attr(0755,root,root) %{_libdir}/collectd/sensors.so
%attr(0755,root,root) %{_libdir}/collectd/serial.so
%attr(0755,root,root) %{_libdir}/collectd/snmp.so
%attr(0755,root,root) %{_libdir}/collectd/swap.so
%attr(0755,root,root) %{_libdir}/collectd/syslog.so
%attr(0755,root,root) %{_libdir}/collectd/table.so
%attr(0755,root,root) %{_libdir}/collectd/tail.so
%attr(0755,root,root) %{_libdir}/collectd/target_notification.so
%attr(0755,root,root) %{_libdir}/collectd/target_replace.so
%attr(0755,root,root) %{_libdir}/collectd/target_scale.so
%attr(0755,root,root) %{_libdir}/collectd/target_set.so
%attr(0755,root,root) %{_libdir}/collectd/tcpconns.so
%attr(0755,root,root) %{_libdir}/collectd/teamspeak2.so
%attr(0755,root,root) %{_libdir}/collectd/ted.so
%attr(0755,root,root) %{_libdir}/collectd/thermal.so
%attr(0755,root,root) %{_libdir}/collectd/unixsock.so
%attr(0755,root,root) %{_libdir}/collectd/uptime.so
%attr(0755,root,root) %{_libdir}/collectd/users.so
%attr(0755,root,root) %{_libdir}/collectd/uuid.so
%attr(0755,root,root) %{_libdir}/collectd/wireless.so
%attr(0755,root,root) %{_libdir}/collectd/vmem.so
%attr(0755,root,root) %{_libdir}/collectd/vserver.so
%attr(0755,root,root) %{_libdir}/collectd/write_http.so
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd.pm
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd/Plugins/Monitorus.pm
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd/Plugins/OpenVZ.pm
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd/Unixsock.pm
%dir %{_datadir}/collectd
%attr(0644,root,root) %{_datadir}/collectd/postgresql_default.conf
%attr(0644,root,root) %{_datadir}/collectd/types.db
%dir /var/lib/%{name}
%dir /var/run/%{name}
%dir /var/log/%{name}
%attr(0644,root,root) %ghost /var/log/%{name}/%{name}.log
%{_mandir}/man1/collectd.*
%{_mandir}/man5/collectd.conf.*
%{_mandir}/man1/collectdmon.1*
%{_mandir}/man1/collectd-nagios.1*
%{_mandir}/man3/Collectd::Unixsock.3pm*
%{_mandir}/man5/collectd-email.5*
%{_mandir}/man5/collectd-exec.5*
%{_mandir}/man5/collectd-java.5*
%{_mandir}/man5/collectd-perl.5*
%{_mandir}/man5/collectd-python.5*
%{_mandir}/man5/collectd-snmp.5*
%{_mandir}/man5/collectd-unixsock.5*
%{_mandir}/man5/types.db.5*

%files -n %{libname}
%{_libdir}/libcollectdclient.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
%{_libdir}/libcollectdclient.so
%{_includedir}/collectd/client.h
%{_includedir}/collectd/lcc_features.h
%{_libdir}/pkgconfig/libcollectdclient.pc
%{_libdir}/libcollectdclient.la

