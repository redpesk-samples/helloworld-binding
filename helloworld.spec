Name:    helloworld-binding
Version: 2.0.0
Release: 1%{?dist}
License: APL2.0
Summary: helloworld service set to be used in redpesk
URL:     https://github.com/redpesk-samples/helloworld-binding
Source:  %{name}-%{version}.tar.gz

%global _afmappdir %{_prefix}/redpesk
%global coverage_dir %{_libexecdir}/redtest/%{name}/coverage_data

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: lcov
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(afb-binding)

%description
Provides a simple API showcasing the basics of binding development

%package redtest
Summary: redtest package
Requires: %{name} = %{version}-%{release}
Requires: lcov
%description redtest

%prep
%autosetup -p 1

%build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_C_FLAGS="--coverage -fPIC" \
  -DCMAKE_CXX_FLAGS="--coverage -fPIC" \
  -DAFM_APP_DIR=%{_afmappdir} .
%cmake_build

%install
%cmake_install

# Copy coverage files
mkdir -p %{buildroot}%{coverage_dir}
find %{_builddir}/%{name}-%{version} -name "*.gcno" -exec cp {} %{buildroot}%{coverage_dir}/ \;

%files
%defattr(-,root,root)
%dir %{_afmappdir}/%{name}
%{_afmappdir}/%{name}/lib/
%{_afmappdir}/%{name}/.rpconfig/

%files redtest
%defattr(-,root,root)
%{_libexecdir}/redtest/%{name}/run-redtest
%{_libexecdir}/redtest/%{name}/tests.py
%dir %{coverage_dir}
%{coverage_dir}/*.gcno