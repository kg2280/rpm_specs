Summary: Modulis build of Zonkey 
Name: modulis-zonkey
Version: 66
Release: 1
License: GPL
Group: Applications/VoIP
Source: modulis-zonkey-66_1.tar.gz
URL: http://www.modulis.ca/
Distribution: CentOS
Vendor: Modulis, Inc.
Packager: Kevin Gagne <kevin.gagne@modulis.ca>
BuildRequires: git


%description
This is the web interface for Zonkey

%prep

%setup


%build

%install
prod=`git ls-remote git@github.com:modulis/zonkey.git | grep heads/v  | sort | tail -1 | grep -P 'v\d+' -o`
git clone --depth 2 git@github.com:modulis/zonkey.git -b $prod $RPM_BUILD_ROOT/var/www/zonkey

%files
%defattr(-,apache,apache,-)
/var/www/zonkey

%changelog

%post
echo "export RAILS_ENV=production" >> ~/.bashrc
source ~/.bashrc

