Name:    helloworld-binding
Version: 2.0.0
Release: 1%{?dist}
License: Apache-2.0
Summary: helloworld service set to be used in redpesk
URL:     https://github.com/redpesk-samples/helloworld-binding
Source:  %{name}-%{version}.tar.gz

%bcond_with no_coverage
%bcond_with cpp

%if %{with cpp}
%global cpp_build ON
%else
%global cpp_build OFF
%endif

%global _afmappdir %{_prefix}/redpesk
%global coverage_dir %{_libexecdir}/redtest/%{name}/coverage_data

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
%if %{without no_coverage}
BuildRequires: lcov
%endif
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(afb-binding)

%description
Provides a simple API showcasing the basics of binding development

%if %{without no_coverage}
%package redtest
Summary: redtest package (coverage build)
Requires: %{name} = %{version}-%{release}
Requires: lcov
Requires: afb-test-py
Requires: afb-libpython
# Download cobertura in run-redtest
Requires: wget tar
%description redtest
This package contains binaries built with coverage instrumentation.
%endif

%prep
%autosetup -p 1

%build
mkdir build && cd build
%cmake \
  -DCPP=%{cpp_build} \
  -DAFM_APP_DIR=%{_afmappdir} \
%if %{without no_coverage}
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_FLAGS="--coverage -fPIC" \
  -DCMAKE_CXX_FLAGS="--coverage -fPIC" \
%else
  -DCMAKE_BUILD_TYPE=Release \
%endif
  ..
%cmake_build
cd ..

%install
# Install the selected implementation (C by default, C++ with --with cpp)
cd build
%cmake_install
cd ..

%if %{without no_coverage}
# Reuse the same instrumented binary for redtest instead of rebuilding it.
install -Dm755 build/%{__cmake_builddir}/helloworld-binding.so \
  %{buildroot}%{coverage_dir}/%{name}/lib/helloworld-binding.so

# Copy the coverage metadata (.gcno) into the coverage_data directory.
cd build/%{__cmake_builddir}
find . -name "*.gcno" -exec cp --parents {} %{buildroot}%{coverage_dir}/ \;
cd ../..

# Install redtest scripts (for testing)
install -Dm755 redtest/run-redtest %{buildroot}%{_libexecdir}/redtest/%{name}/run-redtest
install -Dm644 tests/tests.py %{buildroot}%{_libexecdir}/redtest/%{name}/tests.py
%else
# CMake installs these helper files unconditionally; remove them when
# the redtest subpackage is disabled.
rm -rf %{buildroot}%{_libexecdir}/redtest/%{name}
%endif

%files
%defattr(-,root,root)
%dir %{_afmappdir}/%{name}
%{_afmappdir}/%{name}/lib/
%{_afmappdir}/%{name}/.rpconfig/

%if %{without no_coverage}
%files redtest
%defattr(-,root,root)
%{_libexecdir}/redtest/%{name}/run-redtest
%{_libexecdir}/redtest/%{name}/tests.py
%{coverage_dir}
%endif
