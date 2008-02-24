Summary:	Collects system information in RRD files
Name:		collectd
Version:	4.3.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Monitoring
Url:		http://collectd.org/
Source0:	http://collectd.org/files/collectd-%{version}.tar.gz
Source1:	%{name}-initscript
Source2:	%{name}.logrotate
Patch0:		collectd-path_fixes.diff
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	flex
BuildRequires:	iptables-devel
BuildRequires:	libhal-devel
BuildRequires:	libstatgrab-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	nut-devel
BuildRequires:	oping-devel
BuildRequires:	pcap-devel
BuildRequires:	perl-devel
BuildRequires:	rrdtool-devel
BuildRequires:	xmms-devel
BuildConflicts:	git
Requires(pre):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The collectd daemon collects information about the system it is running on and
writes this information into special database files. These database files can
then be used to generate graphs of the collected data.

%prep

%setup -q
%patch0 -p1

%{_bindir}/find . -name Makefile.am -o -name Makefile.in | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\-Werror//g'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in

%build
%serverbuild
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --foreign --add-missing --copy

%configure2_5x \
    --enable-apache --with-libcurl=%{_prefix} \
    --enable-apcups \
    --disable-apple_sensors \
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
    --disable-ipvs \
    --enable-irq \
    --disable-libvirt \
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
    --enable-nut --with-libupsclient=%{_prefix} \
    --enable-perl --with-libperl=%{_prefix} --with-perl-bindings="INSTALLDIRS=vendor" \
    --enable-ping --with-liboping=%{_prefix} \
    --enable-processes \
    --enable-rrdtool --with-rrdtool=%{_prefix} \
    --enable-sensors--with-lm-sensors=%{_prefix} \
    --enable-serial \
    --enable-snmp --with-libnetsnmp \
    --enable-swap \
    --enable-syslog \
    --disable-tape \
    --enable-tcpconns \
    --enable-unixsock \
    --enable-users \
    --enable-uuid \
    --enable-vserver \
    --enable-wireless \
    --enable-xmms --with-libxmms=%{_prefix} \
    --with-libpthread=%{_prefix} \
    --with-libstatgrab=%{_prefix} \
    
make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_localstatedir}/%{name}
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
%attr(0755,root,root) %{_libdir}/collectd/battery.so
%attr(0755,root,root) %{_libdir}/collectd/cpufreq.so
%attr(0755,root,root) %{_libdir}/collectd/cpu.so
%attr(0755,root,root) %{_libdir}/collectd/csv.so
%attr(0755,root,root) %{_libdir}/collectd/df.so
%attr(0755,root,root) %{_libdir}/collectd/disk.so
%attr(0755,root,root) %{_libdir}/collectd/dns.so
%attr(0755,root,root) %{_libdir}/collectd/email.so
%attr(0755,root,root) %{_libdir}/collectd/entropy.so
%attr(0755,root,root) %{_libdir}/collectd/exec.so
%attr(0755,root,root) %{_libdir}/collectd/hddtemp.so
%attr(0755,root,root) %{_libdir}/collectd/interface.so
%attr(0755,root,root) %{_libdir}/collectd/iptables.so
%attr(0755,root,root) %{_libdir}/collectd/irq.so
%attr(0755,root,root) %{_libdir}/collectd/load.so
%attr(0755,root,root) %{_libdir}/collectd/logfile.so
%attr(0755,root,root) %{_libdir}/collectd/mbmon.so
%attr(0755,root,root) %{_libdir}/collectd/memcached.so
%attr(0755,root,root) %{_libdir}/collectd/memory.so
%attr(0755,root,root) %{_libdir}/collectd/multimeter.so
%attr(0755,root,root) %{_libdir}/collectd/mysql.so
%attr(0755,root,root) %{_libdir}/collectd/network.so
%attr(0755,root,root) %{_libdir}/collectd/nfs.so
%attr(0755,root,root) %{_libdir}/collectd/nginx.so
%attr(0755,root,root) %{_libdir}/collectd/ntpd.so
%attr(0755,root,root) %{_libdir}/collectd/nut.so
%attr(0755,root,root) %{_libdir}/collectd/perl.so
%attr(0755,root,root) %{_libdir}/collectd/ping.so
%attr(0755,root,root) %{_libdir}/collectd/processes.so
%attr(0755,root,root) %{_libdir}/collectd/rrdtool.so
%attr(0755,root,root) %{_libdir}/collectd/sensors.so
%attr(0755,root,root) %{_libdir}/collectd/serial.so
%attr(0755,root,root) %{_libdir}/collectd/snmp.so
%attr(0755,root,root) %{_libdir}/collectd/swap.so
%attr(0755,root,root) %{_libdir}/collectd/syslog.so
%attr(0755,root,root) %{_libdir}/collectd/tcpconns.so
%attr(0755,root,root) %{_libdir}/collectd/unixsock.so
%attr(0755,root,root) %{_libdir}/collectd/users.so
%attr(0755,root,root) %{_libdir}/collectd/uuid.so
%attr(0755,root,root) %{_libdir}/collectd/wireless.so
%attr(0755,root,root) %{_libdir}/collectd/vserver.so
%attr(0755,root,root) %{_libdir}/collectd/xmms.so
%attr(0644,root,root) %{_libdir}/collectd/types.db
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd.pm
%attr(0644,root,root) %{_prefix}/lib/perl5/vendor_perl/*/Collectd/Unixsock.pm
%dir %{_localstatedir}/%{name}
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
%{_mandir}/man5/collectd-perl.5*
%{_mandir}/man5/collectd-snmp.5*
%{_mandir}/man5/collectd-unixsock.5*
%{_mandir}/man5/types.db.5*
