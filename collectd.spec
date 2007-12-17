Summary:	Collects system information in RRD files
Name:		collectd
Version:	4.2.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Monitoring
Url:		http://collectd.org/
Source0:	http://collectd.org/files/%{name}-%{version}.tar.bz2
Source1:	%{name}-initscript
BuildRequires:	libpcap-devel
BuildRequires:	libcurl4-devel
BuildRequires:	libmysql-devel
BuildRequires:	libstatgrab-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	rrdtool-devel
BuildRequires:	chrpath
Requires(pre):	rpm-helper

%description
The collectd daemon collects information about the system 
it is running on and writes this information into special 
database files. These database files can then be used to 
generate graphs of the collected data.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-rrdtool \
	--with-libpthread \
	--with-libcurl \
	--with-libstatgrab \
	--with-lm-sensors \
	--with-libmysql \
	--with-libpcap

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}%{_var}/lib/%{name}
mv -f %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/%{name}
rm -f %{buildroot}%{_libdir}/%{name}/*.la
install %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}

chrpath -d %{buildroot}%{_libdir}/%{name}/apache.so

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README ChangeLog TODO
%attr(755,root,root) %{_sbindir}/%{name}
%attr(744,root,root) %{_sysconfdir}/init.d/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%dir %{_var}/lib/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/%{name}.conf
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.conf.*
