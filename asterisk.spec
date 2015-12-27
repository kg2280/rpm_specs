Summary: Modulis build of Certified Asterisk
Name: modulis-cert-asterisk
Version: 11.6
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-cert-asterisk-11.6.tar.gz
URL: http://www.asterisk.org/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>

%description
This an asterisk rpm package build by Modulis

%prep
rm -rf $RPM_BUILD_DIR/modulis-cert-asterisk-*
rm -rf $RPM_BUILD_ROOT/modulis-cert-asterisk-*
rm -rf $RPM_BUILD_DIR/addons
zcat $RPM_SOURCE_DIR/modulis-cert-asterisk-11.6.tar.gz | tar -xvf -
$RPM_BUILD_DIR/modulis-cert-asterisk-11.6/contrib/scripts/get_mp3_source.sh

%setup
$RPM_BUILD_DIR/modulis-cert-asterisk-11.6/configure
mv $RPM_BUILD_DIR/addons/* $RPM_BUILD_DIR/modulis-cert-asterisk-11.6/addons/
make menuselect.makeopts
menuselect/menuselect --enable chan_sip --enable chan_dahdi --enable res_timing_dahdi --enable app_dahdibarge --enable cdr_mysql --enable app_meetme --enable ODBC_STORAGE --enable CORE-SOUNDS-EN-ULAW --enable CORE-SOUNDS-EN-GSM --enable CORE-SOUNDS-EN-G722 --enable CORE-SOUNDS-FR-ULAW --enable CORE-SOUNDS-FR-GSM --enable CORE-SOUNDS-FR-G722 --enable EXTRA-SOUNDS-EN-ULAW --enable EXTRA-SOUNDS-EN-GSM --enable EXTRA-SOUNDS-EN-G722 --enable EXTRA-SOUNDS-FR-ULAW --enable EXTRA-SOUNDS-FR-GSM --enable EXTRA-SOUNDS-FR-G722 --enable G711_NEW_ALGORITHM --enable G711_REDUCED_BRANCHING menuselect.makeopts

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
make config DESTDIR=$RPM_BUILD_ROOT
make samples DESTDIR=$RPM_BUILD_ROOT
make install-logrotate DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/etc/asterisk
prod=`git ls-remote git@github.com:modulis/asterisk-zonkey.git | grep heads/v | awk '{print $2}' | sort | tail -1 | grep -P 'v\d+' -o`
git clone git@github.com:modulis/asterisk-zonkey.git -b $prod $RPM_BUILD_ROOT/etc/asterisk


%files
%defattr(-,root,root,-)
%doc README
/etc/logrotate.d/asterisk
/etc/asterisk/*
/etc/asterisk/.*
/usr/include/asterisk.h
/usr/include/asterisk/*
/usr/lib/libasteriskssl.so
/usr/lib/libasteriskssl.so.1
/usr/lib/asterisk/*
/usr/sbin/ast*
/usr/sbin/autosupport
/usr/sbin/rasterisk
/usr/sbin/safe_asterisk
/usr/share/man/man8/*
/var/lib/asterisk/*
/var/log/asterisk/*
/var/run/asterisk/
/var/spool/asterisk/*


%changelog

%post
ldconfig
useradd -d /var/run/asterisk/ -M -c "Asterisk PBX user" -r -U -s /sbin/nologin asterisk
test -d /etc/zonkey || mkdir /etc/zonkey/
cp -R /etc/asterisk/etc_zonkey/asterisk /etc/zonkey/
rsync -av /etc/asterisk/etc_zonkey/bin/ /etc/zonkey/bin
chown -R asterisk. /var/run/asterisk/ /var/lib/asterisk/ /var/log/asterisk/ /var/spool/asterisk/ /usr/lib/asterisk/ /etc/zonkey/asterisk /dev/dahdi
chown --recursive root:asterisk /etc/asterisk
chmod --recursive u=rwX,g=rX,o= /var/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /var/log/asterisk
chmod --recursive u=rwX,g=rX,o= /var/run/asterisk
chmod --recursive u=rwX,g=rX,o= /var/spool/asterisk
chmod --recursive u=rwX,g=rX,o= /usr/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /dev/dahdi
chmod --recursive u=rwX,g=rX,o= /etc/asterisk



