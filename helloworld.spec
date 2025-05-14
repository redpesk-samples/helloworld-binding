Name:    helloworld-binding
Version: 2.0.0
Release: 1%{?dist}
License: APL2.0
Summary: helloworld service set to be used in redpesk
URL:     https://git.ovh.iot/redpesk/redpesk-samples/helloworld-binding
Source:  %{name}-%{version}.tar.gz

%global _afmappdir %{_prefix}/redpesk

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(afb-binding)

%description
Provides a simple API showcasing the basics of binding development


%package redtest
Summary: redtest package
Requires: %{name} = %{version}-%{release}
%description redtest


%prep
%autosetup -p 1

%build
%cmake -DAFM_APP_DIR=%{_afmappdir} .
%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root)
%dir %{_afmappdir}/%{name}
%{_afmappdir}

%files redtest
%{_libexecdir}/redtest/%{name}/run-redtest
%{_libexecdir}/redtest/%{name}/tests.py

%changelog
