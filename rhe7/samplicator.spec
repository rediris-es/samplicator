Summary:       Send copies of (UDP) datagrams to multiple receivers
Name:          samplicator
Version:       1.3.8
Release:       rc2.1
License:       Artistic License/GPL
Group:         System Environment/Daemons
Source0:       %{version}%{release}.tar.gz
Source1:       %{name}.init
Source2:       %{name}.sysconfig
URL:	       https://github.com/rediris-es/samplicator/archive/%{version}%{release}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%(id -u -n)

%description
This simple program listens for UDP datagrams on a network port,
and sends copies of these datagrams on to a set of destinations.
Optionally, it can perform sampling, i.e. rather than forwarding
every packet, forward only 1 in N. Another option is that it can
"spoof" the IP source address, so that the copies appear to come
from the original source, rather than the relay. Currently only
supports IPv4.

It can been used to distribute e.g. Netflow packets, SNMP traps
(but not informs), or Syslog messages to multiple receivers.

%prep
%setup -q -n %{name}-%{version}%{release}

%build
./autogen.sh
%configure
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv %{buildroot}%{_bindir}/samplicate %{buildroot}%{_bindir}/%{name}

#%{__install} -D -p -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# systemd init file 
mkdir -p  %{buildroot}/usr/lib/systemd/system/
mkdir -p  %{buildroot}/etc/samplicator/
mkdir -p  %{buildroot}/usr/sbin/

%{__install} -D -p -m0644 rhe7/samplicator.service %{buildroot}/usr/lib/systemd/system
%{__install} -D -p -m0644 rhe7/example.ini %{buildroot}/etc/samplicator/
%{__install} -D -p -m0755 rhe7/samplicatorctl %{buildroot}/usr/sbin/
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make clean

%files
%defattr(-, root, root, -)
%doc README.md INSTALL.md AUTHORS
%{_bindir}/%{name}
%{_sbindir}/samplicatorctl
%config(noreplace) %{_sysconfdir}/samplicator/example.ini
/usr/lib/systemd/system/samplicator.service

%changelog
* Mon Mar 27 2017 RedIRIS - 1.3.8-rc2.1
- Initial Version for RHE7


