Summary: Modulis build of Opensips
Name: modulis-opensips
Version: 1_11
Release: 3
License: GPL
Group: Applications/VoIP
Source: modulis-opensips-1_11.tar.gz
URL: http://www.opensips.org/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>
BuildRequires: bison flex zlib-devel openssl-devel mysql-devel subversion pcre-devel libxml2-devel libicu-devel ruby-devel libapreq2-devel perl-libapreq2 perl-JSON perl-Redis curl curl-devel libiodbc mariadb-devel redis hiredis hiredis-devel perl perl-SOAP-Lite ncurses-devel perl-devel bison-devel bison lynx flex pcre-devel libmicrohttpd-devel perl-ExtUtils-Embed perl-RPC-XML perl-XMLRPC-Lite


%description
This is a Modulis rpm build of Opensips

%prep
rm -rf $RPM_BUILD_ROOT/modulis-opensips-*
zcat $RPM_SOURCE_DIR/modulis-opensips-1_11.tar.gz | tar -xvf -

%setup


%build
cd $RPM_BUILD_DIR/modulis-opensips-1_11*
cp /home/modulis/rpmbuild/SPECS/rpm_specs/opensips_Makefile.conf Makefile.conf
git checkout 9ce6c4abfc3ec7c180443c4
sed -i '69i #include <unistd.h>' cfg.lex
sed -i '38i #include "../../strcommon.h"' modules/mi_xmlrpc_ng/http_fnc.c

TLS=1 make cfg-target=%{_sysconfdir}/opensips/ prefix=/usr

%install
TLS=1 make install basedir=$RPM_BUILD_ROOT cfg-target=%{_sysconfdir}/opensips/ prefix=/usr cfg-prefix=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/etc/opensips
git clone git@github.com:modulis/opensips-zonkey.git -b master $RPM_BUILD_ROOT/etc/opensips
cd $RPM_BUILD_ROOT/etc/opensips
./scripts/afterbuild.sh
git fetch origin
git checkout v41
mkdir -p $RPM_BUILD_ROOT/etc/default/ $RPM_BUILD_ROOT/etc/init.d/
cp $RPM_BUILD_DIR/modulis-opensips-1_11/packaging/rpm/opensips.default $RPM_BUILD_ROOT/etc/default/opensips
cp $RPM_BUILD_DIR/modulis-opensips-1_11/packaging/rpm/opensips.init $RPM_BUILD_ROOT/etc/init.d/opensips

%files
%defattr(-,root,root,-)
%doc README
/etc/default/opensips
/etc/init.d/opensips
/etc/opensips
/usr/lib64/opensips
/usr/sbin/opensips
/usr/sbin/opensipsctl
/usr/sbin/opensipsdbctl
/usr/sbin/opensipsunix
/usr/sbin/osipsconfig
/usr/sbin/osipsconsole
/usr/share/doc/opensips
/usr/share/man/man5/opensips.cfg.5.gz
/usr/share/man/man8/opensips.8.gz
/usr/share/man/man8/opensipsctl.8.gz
/usr/share/man/man8/opensipsunix.8.gz
/usr/share/opensips

%changelog
* Sat Jan 09 2016 Kevin Gagné <kevin.gagne@modulis.ca>
- Use default location instead of /opt/opensips 

%post
depmod -a
mkdir -p /etc/zonkey/opensips/
sed -i 's#path=$CHROOT_DIR/tmp/$name#path=/opt/opensips/run/$name#' /usr/lib64/opensips/opensipsctl/opensipsctl.fifo
cp -R /etc/opensips/customconf/* /etc/zonkey/opensips/
rm -f /etc/opensips/opensipsctlrc
cp -f /etc/opensips/opensipsctlrc.zonkey /etc/opensips/opensipsctlrc
sed -i 's/#setscriptflag(11)/setscriptflag(11)/g' /etc/zonkey/opensips/custom_setup.cfg
sed -i 's/setscriptflag(12)/#setscriptflag(12)/g' /etc/zonkey/opensips/custom_setup.cfg
sed -i 's/# setscriptflag(13)/setscriptflag(13)/g' /etc/zonkey/opensips/custom_setup.cfg
sed -i 's/# debug=4/debug=3/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# server_signature=yes/server_signature=yes/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# server_header=/server_header=/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# user_agent_header=/user_agent_header=/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# db_default_url=/db_default_url=/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# mpath=/mpath=/g' /etc/zonkey/opensips/global_params.cfg
sed -i 's/# modparam/modparam/g' /etc/zonkey/opensips/modules_params.cfg

sed -i 's/# mod/mod/g' /etc/zonkey/opensips/shared_vars.cfg
sed -i 's/#mod/mod/g' /etc/zonkey/opensips/shared_vars.cfg
sed -i 's/modparam("cfgutils", "shvset", "pstn=s:10.130.8.240")/# modparam("cfgutils", "shvset", "pstn=s:10.130.8.240")/g' /etc/zonkey/opensips/shared_vars.cfg
sed -i 's/modparam("cfgutils", "shvset", "suhost=s:10.130.8.35")/# modparam("cfgutils", "shvset", "suhost=s:10.130.8.35")/g' /etc/zonkey/opensips/shared_vars.cfg
echo 'export PATH="$PATH:/opt/opensips/sbin:/etc/opensips/scripts"' >> ~/.bashrc
source ~/.bashrc

useradd -c "OpenSIPs SIP proxy" -MrU -s/sbin/nologin opensips
mkdir -p /var/log/opensips
mkdir /var/run/opensips
chown -R opensips. /var/run/opensips/ /var/log/opensips/
echo 'net.ipv4.ip_nonlocal_bind = 1' >> /etc/sysctl.conf 
sysctl -p
sed -i 's!S_MEMORY=64!S_MEMORY=512!' /etc/default/opensips
sed -i 's!P_MEMORY=4!P_MEMORY=32!' /etc/default/opensips
sed -i '/EOF:/ i# UNIX datagram MI socket' /etc/zonkey/opensips/modules_params.cfg
sed -i '/EOF:/ imodparam("mi_datagram", "socket_name", "udp:10.6.8.50:8000")' /etc/zonkey/opensips/modules_params.cfg
opensips -c /etc/opensips/opensips.cfg
chmod +x /etc/init.d/opensips
echo "# OpenSIPs" >> /etc/rsyslog.conf
echo "local5.*                                                -/var/log/opensips/opensips.log" >> /etc/rsyslog.conf
cat <<LOGROT > /etc/logrotate.d/opensips
/var/log/opensips/opensips.log {
  rotate 20
  size 200M
  missingok
  notifempty
  postrotate
    /bin/kill -HUP \`cat /var/run/syslogd.pid 2> /dev/null\` 2>/dev/null || :
  endscript
}
LOGROT
systemctl restart rsyslog

ldconfig
