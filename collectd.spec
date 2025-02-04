%define major 1
%define libname %mklibname collectdclient %{major}
%define devname %mklibname -d collectdclient

Summary:	Collects system information in RRD files
Name:		collectd
Version:	5.5.0
Release:	1
License:	GPLv2+
Group:		Monitoring
Url:		https://collectd.org/
Source0:	http://collectd.org/files/collectd-%{version}.tar.bz2
Source1:	%{name}.service
Patch101:	collectd-5.5.0-werror.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libdbi-devel
BuildRequires:	libesmtp-devel
BuildRequires:	libtool-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	mysql-devel
BuildRequires:	net-snmp-devel
BuildRequires:	oping-devel
BuildRequires:	pcap-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	pkgconfig(libip4tc)
BuildRequires:	pkgconfig(libip6tc)
BuildRequires:	pkgconfig(libmemcached)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(librrd)
BuildRequires:	pkgconfig(libstatgrab)
BuildRequires:	pkgconfig(libupsclient)
BuildRequires:	pkgconfig(libvirt)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(OpenIPMI)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(xtables)
Requires(pre):	rpm-helper

%description
The collectd daemon collects information about the system it is running on and
writes this information into special database files. These database files can
then be used to generate graphs of the collected data.

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README ChangeLog TODO
%config(noreplace) %{_sysconfdir}/collectd.conf
%{_unitdir}/%{name}.service
%{_bindir}/collectd-nagios
%{_bindir}/collectdctl
%{_bindir}/collectd-tg
%{_sbindir}/collectd
%{_sbindir}/collectdmon
%dir %{_libdir}/collectd
%{_libdir}/collectd/*.so
%{perl_vendorlib}/*
%dir %{_datadir}/collectd
%{_datadir}/collectd/postgresql_default.conf
%{_datadir}/collectd/types.db
%dir /var/lib/%{name}
%dir /var/run/%{name}
%dir /var/log/%{name}
%ghost /var/log/%{name}/%{name}.log
%{_mandir}/man1/collectd.*
%{_mandir}/man1/collectd-tg.*
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

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Collects system information in RRD files
Group:		System/Libraries

%description -n %{libname}
The collectd daemon collects information about the system it is running on.
This package contains the shared libraries used by %{name}

%files -n %{libname}
%{_libdir}/libcollectdclient.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Collects system information in RRD files
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
The collectd daemon collects information about the system it is running on.
This package contains the development headers.

%files -n %{devname}
%defattr(644,root,root,755)
%{_libdir}/libcollectdclient.so
%{_includedir}/collectd/client.h
%{_includedir}/collectd/lcc_features.h
%{_includedir}/collectd/network.h
%{_includedir}/collectd/network_buffer.h
%{_libdir}/pkgconfig/libcollectdclient.pc

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
autoreconf -fi
%serverbuild
pushd libltdl
%before_configure
popd
%configure2_5x \
    --with-libperl=%{_prefix} \
    --with-perl-bindings="INSTALLDIRS=vendor" \
    --localstatedir=/var/lib \
    --without-included-ltdl \
    --with-ltdl-include=%{_includedir} \
    --with-ltdl-lib=%{_libdir} \
    --disable-xmms \
    --disable-static

%make

%install
install -d %{buildroot}/var/lib/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}/var/log/%{name}

%makeinstall_std LIBLTDL=%{_libdir}/libltdl.la

install -Dm755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

touch %{buildroot}/var/log/%{name}/%{name}.log

# cleanup
rm %{buildroot}%{_libdir}/collectd/*.la

%post
%create_ghostfile /var/log/%{name}/%{name}.log root root 644
%_post_service %{name}

%preun
%_preun_service %{name}

