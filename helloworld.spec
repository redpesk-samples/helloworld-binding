Name:    helloworld-binding
Version: 2.0.0
Release: 1%{?dist}
License: Apache-2.0
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
Summary: redtest package (coverage build)
Requires: lcov
%description redtest
This package contains binaries built with coverage instrumentation.

%prep
%autosetup -p 1

%build
# Build (no coverage)
mkdir build-no-coverage && cd build-no-coverage
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DAFM_APP_DIR=%{_afmappdir} ..
%cmake_build
cd ..

# Build coverage (with coverage flags)
mkdir build-coverage && cd build-coverage
%cmake \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_FLAGS="--coverage -fPIC" \
  -DCMAKE_CXX_FLAGS="--coverage -fPIC" \
  -DAFM_APP_DIR=%{coverage_dir} ..
%cmake_build
cd ..

%install
# Install (base package)
cd build-no-coverage
%cmake_install
cd ..

# Install coverage build (for redtest package)
cd build-coverage
# Clean any existing .so or .gcno
rm -rf %{buildroot}%{coverage_dir}
%cmake_install

# Copy the coverage files (.gcno) into the coverage_data directory for redtest
find . -name "*.gcno" -exec cp --parents {} %{buildroot}%{coverage_dir}/ \;
cd ..

# Install redtest scripts (for testing)
install -Dm755 redtest/run-redtest %{buildroot}%{_libexecdir}/redtest/%{name}/run-redtest
install -Dm644 tests/tests.py %{buildroot}%{_libexecdir}/redtest/%{name}/tests.py

%files
%defattr(-,root,root)
%dir %{_afmappdir}/%{name}
%{_afmappdir}/%{name}/lib/
%{_afmappdir}/%{name}/.rpconfig/

%files redtest
%defattr(-,root,root)
%{_libexecdir}/redtest/%{name}/run-redtest
%{_libexecdir}/redtest/%{name}/tests.py
%{coverage_dir}
