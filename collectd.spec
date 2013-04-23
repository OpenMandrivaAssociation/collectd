%define major 0
%define libname %mklibname collectdclient %{major}
%define develname %mklibname -d collectdclient

Summary:	Collects system information in RRD files
Name:		collectd
Version:	5.1.0
Release:	1
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
#BuildConflicts:	git
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	flex
BuildRequires:	iptables-devel
BuildRequires:	libdbi-devel
BuildRequires:	libesmtp-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	libtool-devel
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
%{_libdir}/collectd/*.so
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
