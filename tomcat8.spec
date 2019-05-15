# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/spions/rpm-tomcat8/master/tomcat8.spec -O ~/rpmbuild/SPECS/tomcat8.spec
# wget https://raw.github.com/spions/rpm-tomcat8/master/tomcat8.init -O ~/rpmbuild/SOURCES/tomcat8.init
# wget https://raw.github.com/spions/rpm-tomcat8/master/tomcat8.sysconfig -O ~/rpmbuild/SOURCES/tomcat8.sysconfig
# wget https://raw.github.com/spions/rpm-tomcat8/master/tomcat8.logrotate -O ~/rpmbuild/SOURCES/tomcat8.logrotate
# wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.39//bin/apache-tomcat-8.5.39.tar.gz -O ~/rpmbuild/SOURCES/apache-tomcat-8.5.39.tar.gz
# rpmbuild -bb ~/rpmbuild/SPECS/tomcat8.spec

%define __jar_repack %{nil}
%define tomcat_home /opt/tomcat8
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine, RI for Servlet 2.4/JSP 2.0 API
Name:       tomcat8
Version:    8.5.39
BuildArch:  noarch
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init
Source2:    %{name}.sysconfig
Source3:    %{name}.logrotate
Requires:   java-1.8.0-openjdk
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{tomcat_home}/conf %{buildroot}/%{_sysconfdir}/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s %{_sysconfdir}/%{name} conf
cd -

# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.init %{buildroot}/%{_initrddir}/%{name}

# Drop sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%{tomcat_home}/*
/var/log/%{name}/
%defattr(-,root,root)
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart >/dev/null 2>&1
fi

%changelog
* Wed Apr 5 2018 Yoann Le Garff <pe.weeble@yahoo.fr>
- 8.5.39
* Fri Jun 5 2015 Wayne Carty <wayne.carty@risk.lexisnexis.com>
- 8.0.23 
* Thu Sep 4 2014 Edward Bartholomew <edward@bartholomew>
- 7.0.55
* Mon Jul 1 2013 Nathan Milford <nathan@milford.io>
- 7.0.41
