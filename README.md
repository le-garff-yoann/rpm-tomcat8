# rpm-tomcat8

An RPM spec file to install Tomcat 8.0.

## To Build:

```bash
sudo yum -y install rpmdevtools && rpmdev-setuptree

# git clone

\cp tomcat8.spec ~/rpmbuild/SPECS/tomcat8.spec
\cp tomcat8.init ~/rpmbuild/SOURCES/tomcat8.init
\cp tomcat8.sysconfig ~/rpmbuild/SOURCES/tomcat8.sysconfig
\cp tomcat8.logrotate ~/rpmbuild/SOURCES/tomcat8.logrotate

wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.39/bin/apache-tomcat-8.5.39.tar.gz -O ~/rpmbuild/SOURCES/apache-tomcat-8.5.39.tar.gz

rpmbuild -bb ~/rpmbuild/SPECS/tomcat8.spec # ~/rpmbuild/RPMS/noarch/tomcat8-8.5.39-1.noarch.rpm
```