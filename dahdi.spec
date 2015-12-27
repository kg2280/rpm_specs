Summary: Modulis version of complete Dahdi tools
Name: modulis-dahdi-complete
Version: 2.10.2
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-dahdi-complete-2.10.2.tar.gz
URL: http://www.asterisk.org/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>

%description
This the complete dahdi rpm package build by Modulis

%prep
rm -rf $RPM_BUILD_DIR/modulis-dahdi-complete*
rm -rf $RPM_BUILD_ROOT/modulis-dahdi-complete*
zcat $RPM_SOURCE_DIR/modulis-dahdi-complete-2.10.2.tar.gz | tar -xvf -

%setup
cd $RPM_BUILD_DIR/modulis-dahdi-complete*

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
make config DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
cp $RPM_BUILD_DIR/modulis-dahdi-complete-2.10.2/tools/dahdi.init $RPM_BUILD_ROOT/etc/init.d/dahdi
rm -rf $RPM_BUILD_ROOT/lib/modules/3.10.0-327.3.1.el7.x86_64/modules*


%files
%defattr(-,root,root,-)
%doc README
/etc/bash_completion.d/dahdi
/etc/dahdi/*
/etc/hotplug/usb/xpp_fxloader
/etc/hotplug/usb/xpp_fxloader.usermap
/etc/init.d/dahdi
/etc/modprobe.d/dahdi.blacklist.conf
/etc/modprobe.d/dahdi.conf
/etc/udev/rules.d/dahdi.rules
/etc/udev/rules.d/xpp.rules
/lib/firmware/.dahdi-*
/lib/firmware/dahdi-*
/lib/modules/3.10.0-327.3.1.el7.x86_64/dahdi*
/usr/include/dahdi/*
/usr/lib/libtonezone.a
/usr/lib/libtonezone.so
/usr/lib/libtonezone.so.1
/usr/lib/libtonezone.so.1.0
/usr/lib/libtonezone.so.2
/usr/lib/libtonezone.so.2.0
/usr/local/share/perl5/Dahdi.pm
/usr/local/share/perl5/Dahdi/*
/usr/sbin/astribank_is_starting
/usr/sbin/dahdi_*
/usr/sbin/fxotune
/usr/sbin/lsdahdi
/usr/sbin/sethdlc
/usr/sbin/twinstar
/usr/sbin/xpp_blink
/usr/sbin/xpp_sync
/usr/share/dahdi/*
/usr/share/man/man8/astribank_is_starting.8.gz
/usr/share/man/man8/dahdi_*
/usr/share/man/man8/fxotune.8.gz
/usr/share/man/man8/lsdahdi.8.gz
/usr/share/man/man8/twinstar.8.gz
/usr/share/man/man8/xpp_blink.8.gz
/usr/share/man/man8/xpp_sync.8.gz

%changelog

%post
depmod -a
ldconfig
