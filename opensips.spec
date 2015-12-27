Summary: Modulis build of Opensips
Name: modulis-opensips
Version: 1_11
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-opensips-1_11.tar.gz
URL: http://www.opensips.org/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>

%description
This is a Modulis rpm build of Opensips

%prep
rm -rf $RPM_BUILD_ROOT/modulis-opensips-*
zcat $RPM_SOURCE_DIR/modulis-opensips-1_11.tar.gz | tar -xvf -

%setup


%build
cd $RPM_BUILD_DIR/modulis-opensips-1_11*
git checkout 9ce6c4abfc3ec7c180443c4
TLS=1 make

%install
TLS=1 make install 
rm -rf $RPM_BUILD_ROOT/opt/opensips/etc/opensips
git clone git@github.com:modulis/opensips-zonkey.git -b master $RPM_BUILD_ROOT/opt/opensips/etc/opensips
cd $RPM_BUILD_ROOT/opt/opensips/etc/opensips
./scripts/afterbuild.sh
git fetch origin
git checkout v41


%files
%defattr(-,root,root,-)
%doc README
/opt/opensips/etc/opensips/*
/opt/opensips/etc/opensips/.*


%changelog

%post
depmod -a
mkdir -p /etc/zonkey/opensips/
cp -R /opt/opensips/etc/opensips/customconf/* /etc/zonkey/opensips/
rm -f /opt/opensips/etc/opensips/opensipsctlrc
cp -f /opt/opensips/etc/opensips/opensipsctlrc.zonkey /opt/opensips/etc/opensips/opensipsctlrc
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
useradd -c "OpenSIPs SIP proxy" -MrU -s/sbin/nologin opensips
mkdir -p /var/log/opensips
mkdir /opt/opensips/run
chown -R opensips. /opt/opensips/ /var/log/opensips/
echo 'net.ipv4.ip_nonlocal_bind = 1' >> /etc/sysctl.conf 
sysctl -p
sed -i 's!S_MEMORY=64!S_MEMORY=512!' /etc/default/opensips
sed -i 's!P_MEMORY=4!P_MEMORY=32!' /etc/default/opensips
sed -i '/EOF:/ i# UNIX datagram MI socket' /etc/zonkey/opensips/modules_params.cfg
sed -i '/EOF:/ imodparam("mi_datagram", "socket_name", "udp:10.6.8.50:8000")' /etc/zonkey/opensips/modules_params.cfg
opensips -c /opt/opensips/etc/opensips/opensips.cfg

ldconfig