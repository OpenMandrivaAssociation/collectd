%define major 0
%define libname %mklibname collectdclient %{major}
%define develname %mklibname -d collectdclient

Summary:	Collects system information in RRD files
Name:		collectd
Version:	5.0.0
Release:	%mkrel 2
License:	GPLv2+
Group:		Monitoring
URL:		http://collectd.org/
Source0:	http://collectd.org/files/collectd-%{version}.tar.bz2
Source1:	%{name}-initscript
Source2:	%{name}.logrotate
Patch3:		collectd-4.5.1-perl_fix.diff
Patch101:	collectd-4.10.3-werror.patch
Patch102:	collectd-4.10.3-lt.patch
Patch103:	collectd-4.10.1-noowniptc.patch
Patch104:	collectd-4.10.2-libnotify-0.7.patch
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
BuildRequires:	libmemcached-devel
BuildRequires:	iptables-iptc-devel
BuildRequires:	iptables-ip6tc-devel
BuildRequires:	iptables-ip4tc-devel
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
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p0
%patch3 -p0

%build
autoreconf -fi
%serverbuild
pushd libltdl
%before_configure
popd
%configure2_5x \
    --with-libperl=%{_prefix} --with-perl-bindings="INSTALLDIRS=vendor" \
    --localstatedir=/var/lib \
    --without-included-ltdl \
    --with-ltdl-include=%{_includedir} \
    --with-ltdl-lib=%{_libdir} \
    --disable-xmms \
    --disable-static

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/lib/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}/var/log/%{name}

%makeinstall_std LIBLTDL=%{_libdir}/libltdl.la

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
%config(noreplace) %{_sysconfdir}/collectd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_initrddir}/%{name}
%{_bindir}/collectd-nagios
%{_bindir}/collectdctl
%{_sbindir}/collectd
%{_sbindir}/collectdmon
%dir %{_libdir}/collectd
%{_libdir}/collectd/apache.so
%{_libdir}/collectd/apcups.so
%{_libdir}/collectd/ascent.so
%{_libdir}/collectd/battery.so
%{_libdir}/collectd/bind.so
%{_libdir}/collectd/conntrack.so
%{_libdir}/collectd/contextswitch.so
%{_libdir}/collectd/cpufreq.so
%{_libdir}/collectd/cpu.so
%{_libdir}/collectd/csv.so
%{_libdir}/collectd/curl.so
%{_libdir}/collectd/dbi.so
%{_libdir}/collectd/df.so
%{_libdir}/collectd/disk.so
%{_libdir}/collectd/dns.so
%{_libdir}/collectd/email.so
%{_libdir}/collectd/entropy.so
%{_libdir}/collectd/exec.so
%{_libdir}/collectd/filecount.so
%{_libdir}/collectd/fscache.so
%{_libdir}/collectd/hddtemp.so
%{_libdir}/collectd/interface.so
%{_libdir}/collectd/ipmi.so
%{_libdir}/collectd/iptables.so
%{_libdir}/collectd/irq.so
%{_libdir}/collectd/libvirt.so
%{_libdir}/collectd/load.so
%{_libdir}/collectd/logfile.so
%{_libdir}/collectd/madwifi.so
%{_libdir}/collectd/match_empty_counter.so
%{_libdir}/collectd/match_hashed.so
%{_libdir}/collectd/match_regex.so
%{_libdir}/collectd/match_timediff.so
%{_libdir}/collectd/match_value.so
%{_libdir}/collectd/mbmon.so
%{_libdir}/collectd/memcachec.so
%{_libdir}/collectd/memcached.so
%{_libdir}/collectd/memory.so
%{_libdir}/collectd/multimeter.so
%{_libdir}/collectd/mysql.so
%{_libdir}/collectd/network.so
%{_libdir}/collectd/nfs.so
%{_libdir}/collectd/nginx.so
%{_libdir}/collectd/notify_desktop.so
%{_libdir}/collectd/notify_email.so
%{_libdir}/collectd/ntpd.so
%{_libdir}/collectd/olsrd.so
%{_libdir}/collectd/openvpn.so
%{_libdir}/collectd/perl.so
%{_libdir}/collectd/ping.so
%{_libdir}/collectd/postgresql.so
%{_libdir}/collectd/powerdns.so
%{_libdir}/collectd/processes.so
%{_libdir}/collectd/protocols.so
%{_libdir}/collectd/python.so
%{_libdir}/collectd/rrdcached.so
%{_libdir}/collectd/rrdtool.so
%{_libdir}/collectd/sensors.so
%{_libdir}/collectd/serial.so
%{_libdir}/collectd/snmp.so
%{_libdir}/collectd/swap.so
%{_libdir}/collectd/syslog.so
%{_libdir}/collectd/table.so
%{_libdir}/collectd/tail.so
%{_libdir}/collectd/target_notification.so
%{_libdir}/collectd/target_replace.so
%{_libdir}/collectd/target_scale.so
%{_libdir}/collectd/target_set.so
%{_libdir}/collectd/tcpconns.so
%{_libdir}/collectd/teamspeak2.so
%{_libdir}/collectd/ted.so
%{_libdir}/collectd/thermal.so
%{_libdir}/collectd/unixsock.so
%{_libdir}/collectd/uptime.so
%{_libdir}/collectd/users.so
%{_libdir}/collectd/uuid.so
%{_libdir}/collectd/wireless.so
%{_libdir}/collectd/vmem.so
%{_libdir}/collectd/vserver.so
%{_libdir}/collectd/write_http.so
%{_libdir}/collectd/curl_xml.so
%{_libdir}/collectd/target_v5upgrade.so
%{_libdir}/collectd/threshold.so
%perl_vendorlib/*
%dir %{_datadir}/collectd
%{_datadir}/collectd/postgresql_default.conf
%{_datadir}/collectd/types.db
%dir /var/lib/%{name}
%dir /var/run/%{name}
%dir /var/log/%{name}
%ghost /var/log/%{name}/%{name}.log
%{_mandir}/man1/collectd.*
%{_mandir}/man5/collectd.conf.*
%{_mandir}/man1/collectdmon.1*
%{_mandir}/man1/collectd-nagios.1*
%{_mandir}/man1/collectdctl.1*
%{_mandir}/man3/Collectd::Unixsock.3pm*
%{_mandir}/man5/collectd-threshold.5*
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

