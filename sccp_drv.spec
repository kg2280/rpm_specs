Summary: Modulis build of Asterisk SCCP driver
Name: modulis-chan-sccp-stable
Version: 4.2.2.r6497
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-chan-sccp-stable-4.2.2.r6497.tar.gz
URL: http://sourceforge.net/projects/chan-sccp-b/files/latest/download?source=files
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>

%description
This a sccp sriver rpm package build by Modulis

%prep
rm -rf $RPM_BUILD_DIR/modulis-chan-sccp-stable*
rm -rf $RPM_BUILD_ROOT/modulis-chan-sccp-stable*
zcat $RPM_SOURCE_DIR/modulis-chan-sccp-stable-*.tar.gz | tar -xvf -
cd modulis-chan-sccp-stable-*
cp /home/modulis/rpmbuild/SPECS/rpm_specs/0001-odbc-mwi-fix.patch .
patch -p1 < 0001-odbc-mwi-fix.patch

%setup
./configure --enable-conference --with-hash-size=3001

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,asterisk,-)
/usr/lib/asterisk/modules/chan_sccp.so

%changelog

%post
ldconfig

