Summary: 	PBSWeb
Url:		http://www.cs.ualberta.ca/~pinchak/PBSWeb/
Name: 		pbsweb-butf
Version:	0.9
Release:	%mkrel 6
License:	GPL 
Group:		Monitoring 
Provides: 	pbsweb-butf
Source:		%{name}-%{version}.tar.bz2
Source1:	setup_postgres_pbs
Patch0:		pbsweb-createdb.psql.patch.bz2
Patch1:		pbsweb-dbutils.php.patch.bz2
BuildArch:      noarch
Prefix:         %{_prefix}
Requires:	php-common >= 4.1, php >= 4.1, php-xml >= 4.1, mod_php >= 4.1 
Requires:	apache-conf >= 1.3, apache-common >= 1.3, apache-modules >= 1.3 
Requires:	postgresql , postgresql-server, php-pgsql

%description
PBSWeb was designed as an aid to the Portable Batch System (PBS) job 
scheduler.  PBS is responsible for scheduling jobs on high-performance 
(often massively parallel) machines so as to ensure fair access to 
resources.  However, many users find PBS hard to use.  PBS requires 
users to write scripts containing complex directives and options, and 
so many potential users avoid using PBS and the machine upon which it 
is installed. PBSWeb simplifies the task of creating these scripts by 
allowing the user to specify these directives and options through the 
use of HTML forms.

%prep 
%setup
%patch0 -p0 
%patch1 -p0 

%build
rm -rf %{buildroot}
cp %{SOURCE1} ~/rpm/BUILD/%{name}-%{version}/setup_postgres_pbs
chmod 644 ~/rpm/BUILD/%{name}-%{version}/Papers/*
chmod 644 ~/rpm/BUILD/%{name}-%{version}/README.PBSWeb 
chmod 644 ~/rpm/BUILD/%{name}-%{version}/createdb.psql

%install
mkdir -p %{buildroot}/var/www/html/pbsweb
mv %{_builddir}/%{name}-%{version}/PBSWebExport/* %{buildroot}/var/www/html/pbsweb/
chmod 755 %{buildroot}/var/www/html/pbsweb/img
chmod 644 %{buildroot}/var/www/html/pbsweb/img/*

%files 
%defattr(-,root,root)
%doc Papers/* README.PBSWeb createdb.psql setup_postgres_pbs
%attr(644,postgres,postgres) /var/www/html/pbsweb/*.php
%attr(644,postgres,postgres) /var/www/html/pbsweb/*.py
%attr(644,postgres,postgres) /var/www/html/pbsweb/*.html
%attr(755,postgres,postgres) /var/www/html/pbsweb/Help
/var/www/html/pbsweb/img/*
/var/www/html/pbsweb/Makefile
/var/www/html/pbsweb/*.txt

%post
hostserver=`hostname`
pbswebdocroot="/var/www/html/pbsweb"
cp ${pbswebdocroot}/PBSWebConstants.php ${pbswebdocroot}/PBSWebConstants.php.sauv
sed -e 's/^$DEFAULTHOST.*/\$DEFAULTHOST="'${hostserver}'"\;/' ${pbswebdocroot}/PBSWebConstants.php.sauv > ${pbswebdocroot}/PBSWebConstants.php
mkdir -p /var/tmp/pbsweb.upload
chown -R postgres.pbs /var/tmp/pbsweb.upload

# apache modification
apache_conf=/etc/httpd/conf
cp ${apache_conf}/commonhttpd.conf ${apache_conf}/commonhttpd.conf.pbsweb
sed -e 's/^User apache/User postgres/' ${apache_conf}/commonhttpd.conf.pbsweb > ${apache_conf}/commonhttpd.conf.pbsweb1
sed -e 's/^Group apache/Group postgres/' ${apache_conf}/commonhttpd.conf.pbsweb1 > ${apache_conf}/commonhttpd.conf
rm -f ${apache_conf}/commonhttpd.conf.pbsweb1

%clean
rm -rf %{buildroot}

