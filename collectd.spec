Summary:	Collects system information in RRD files
Name:		collectd
Version:	4.2.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Monitoring
Url:		http://collectd.org/
Source0:	http://collectd.org/files/collectd-%{version}.tar.bz2
Source1:	%{name}-initscript
BuildRequires:	libpcap-devel
BuildRequires:	libcurl4-devel
BuildRequires:	mysql-devel
BuildRequires:	libstatgrab-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	rrdtool-devel
BuildRequires:	chrpath
Requires(pre):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The collectd daemon collects information about the system 
it is running on and writes this information into special 
database files. These database files can then be used to 
generate graphs of the collected data.

%prep
%setup -q
%{_bindir}/find . -name Makefile.am -o -name Makefile.in | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\-Werror//g'

%build
%{configure2_5x} \
	--with-rrdtool \
	--with-libpthread \
	--with-libcurl \
	--with-libstatgrab \
	--with-lm-sensors \
	--with-libmysql \
	--with-libpcap \
	--disable-perl
(cd bindings/perl && %{__perl} Makefile.PL INSTALLDIRS=vendor)
%{make}

%install
rm -rf %{buildroot}
%{makeinstall_std}

mkdir -p %{buildroot}%{_initrddir}
install %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_var}/lib/%{name}

rm %{buildroot}%{_libdir}/collectd/*.la

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/collectd/*.so %{buildroot}%{_sbindir}/collectd

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README ChangeLog TODO
%attr(755,root,root) %{_sbindir}/collectd
%attr(755,root,root) %{_initrddir}/%{name}
%attr(755,root,root) %{_libdir}/collectd/*.so
%dir %{_var}/lib/%{name}
%{_mandir}/man1/collectd.*
%{_mandir}/man5/collectd.conf.*
%config(noreplace) %{_sysconfdir}/collectd.conf
%attr(755,root,root) %{_bindir}/collectd-nagios
%{_libdir}/collectd/types.db
%{_prefix}/lib/perl5/vendor_perl/*/Collectd.pm
%{_prefix}/lib/perl5/vendor_perl/*/Collectd/Unixsock.pm
%{_mandir}/man3/Collectd::Unixsock.3pm*
%{_mandir}/man1/collectd-nagios.1*
%{_mandir}/man5/collectd-email.5*
%{_mandir}/man5/collectd-exec.5*
%{_mandir}/man5/collectd-perl.5*
%{_mandir}/man5/collectd-snmp.5*
%{_mandir}/man5/collectd-unixsock.5*
