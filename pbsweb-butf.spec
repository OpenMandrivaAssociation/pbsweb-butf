Name: 		pbsweb-butf
Version:	0.9
Release:	12
Summary: 	PBSWeb
License:	GPL 
Group:		Monitoring 
Provides: 	pbsweb-butf
Url:		https://www.cs.ualberta.ca/~pinchak/PBSWeb/
Source:		%{name}-%{version}.tar.bz2
Source1:	setup_postgres_pbs
Patch0:		pbsweb-createdb.psql.patch.bz2
Patch1:		pbsweb-dbutils.php.patch.bz2
Requires:	mod_php
Requires:	php-xml
Requires:	php-pgsql
Requires:	postgresql-server
BuildArch:      noarch

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
cp %{SOURCE1} .

%build
chmod 644 Papers/*
chmod 644 README.PBSWeb 
chmod 644 createdb.psql

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



%changelog
* Mon Oct 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.9-10mdv2010.0
+ Revision: 454254
- fix dependencies

* Fri Sep 04 2009 Thierry Vignaud <tvignaud@mandriva.com> 0.9-9mdv2010.0
+ Revision: 430245
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.9-8mdv2009.0
+ Revision: 255133
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.9-6mdv2008.1
+ Revision: 132771
- kill invalid packager tag
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import pbsweb-butf


* Mon May 17 2004 Antoine Ginies <aginies@n2.mandrakesoft.com> 0.9-6mdk
- fix permissions (srpm)

* Tue Mar 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.9-5mdk
- fix missing files
- fix requires

* Wed Jun 5 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.9-4mdk
- fix problem with setup_postgres_pbs
- postgres user now launch apache server

* Tue Jun 4 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.9-3mdk
- add post section in spec file
- adjust error in setup_postgres_pbs script

* Tue Jun 4 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.9-2mdk
- patch createdb.psql to fit correct user 

* Tue Jun 4 2002 Antoine Ginies <aginies@mandrakesoft.com> 0.9-1mdk
- First release for Mandrakesoft
