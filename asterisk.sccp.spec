Summary: Modulis build of Certified Asterisk for SCCP phones
Name: modulis-cert-asterisk-sccp
Version: 11.6
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-cert-asterisk-sccp-11.6.tar.gz
URL: http://www.asterisk.org/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>

%description
This an asterisk rpm package build by Modulis

%prep
rm -rf $RPM_BUILD_DIR/modulis-cert-asterisk-sccp*
rm -rf $RPM_BUILD_ROOT/modulis-cert-asterisk-sccp*
rm -rf $RPM_BUILD_DIR/addons
zcat $RPM_SOURCE_DIR/modulis-cert-asterisk-sccp-11.6.tar.gz | tar -xvf -
$RPM_BUILD_DIR/modulis-cert-asterisk-sccp-11.6/contrib/scripts/get_mp3_source.sh

%setup
$RPM_BUILD_DIR/modulis-cert-asterisk-sccp-11.6/configure
mv $RPM_BUILD_DIR/addons/* $RPM_BUILD_DIR/modulis-cert-asterisk-sccp-11.6/addons/
make menuselect.makeopts
menuselect/menuselect --enable cdr_mysql --enable app_meetme --enable ODBC_STORAGE --enable CORE-SOUNDS-EN-ULAW --enable CORE-SOUNDS-EN-GSM --enable CORE-SOUNDS-EN-G722 --enable CORE-SOUNDS-FR-ULAW --enable CORE-SOUNDS-FR-GSM --enable CORE-SOUNDS-FR-G722 --enable EXTRA-SOUNDS-EN-ULAW --enable EXTRA-SOUNDS-EN-GSM --enable EXTRA-SOUNDS-EN-G722 --enable EXTRA-SOUNDS-FR-ULAW --enable EXTRA-SOUNDS-FR-GSM --enable EXTRA-SOUNDS-FR-G722 --enable G711_NEW_ALGORITHM --enable G711_REDUCED_BRANCHING menuselect.makeopts

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
make config DESTDIR=$RPM_BUILD_ROOT
make samples DESTDIR=$RPM_BUILD_ROOT
make install-logrotate DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/etc/asterisk
git clone git@github.com:modulis/asterisk-su-zonkey.git $RPM_BUILD_ROOT/etc/asterisk


%files
%defattr(-,root,root,-)
%doc README
/etc/asterisk
/etc/logrotate.d/asterisk
/usr/include/asterisk
/usr/include/asterisk.h
/usr/lib/asterisk
/usr/lib/libasteriskssl.so
/usr/lib/libasteriskssl.so.1
/usr/sbin/astcanary
/usr/sbin/astdb2bdb
/usr/sbin/astdb2sqlite3
/usr/sbin/asterisk
/usr/sbin/astgenkey
/usr/sbin/autosupport
/usr/sbin/rasterisk
/usr/sbin/safe_asterisk
/usr/share/man/man8/asterisk.8.gz
/usr/share/man/man8/astgenkey.8.gz
/usr/share/man/man8/autosupport.8.gz
/usr/share/man/man8/safe_asterisk.8.gz
/var/lib/asterisk
/var/spool/asterisk


%changelog

%post
ldconfig
useradd -d /var/run/asterisk/ -M -c "Asterisk PBX user" -r -U -s /sbin/nologin asterisk
test -d /etc/zonkey || mkdir /etc/zonkey/
cp -R /etc/asterisk/CUSTOMCONF/asterisk_config /etc/zonkey/asterisk
rsync -av /etc/asterisk/CUSTOMCONF/bin/ /etc/zonkey/bin
chown -R asterisk. /var/run/asterisk/ /var/lib/asterisk/ /var/log/asterisk/ /var/spool/asterisk/ /usr/lib/asterisk/ /etc/zonkey/asterisk /dev/dahdi
chown --recursive root:asterisk /etc/asterisk
chmod --recursive u=rwX,g=rX,o= /var/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /var/log/asterisk
chmod --recursive u=rwX,g=rX,o= /var/run/asterisk
chmod --recursive u=rwX,g=rX,o= /var/spool/asterisk
chmod --recursive u=rwX,g=rX,o= /usr/lib/asterisk
chmod --recursive u=rwX,g=rX,o= /dev/dahdi
chmod --recursive u=rwX,g=rX,o= /etc/asterisk

cat << EOF > /usr/lib/systemd/system/asterisk.service
[Unit]
Description=Asterisk PBX And Telephony Daemon
After=network.target

[Service]
User=asterisk
Group=asterisk
Environment=HOME=/var/lib/asterisk
WorkingDirectory=/var/lib/asterisk
ExecStart=/usr/sbin/asterisk -f -C /etc/asterisk/asterisk.conf
ExecStop=/usr/sbin/asterisk -rx 'core stop now'
ExecReload=/usr/sbin/asterisk -rx 'core reload'

[Install]
WantedBy=multi-user.target
EOF
systemctl enable asterisk
systemctl start asterisk
/etc/zonkey/bin/test_services.sh

