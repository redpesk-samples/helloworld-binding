Name:    helloworld-binding
Version: 2.0.0
Release: 1%{?dist}
License: MIT
Summary: helloworld service set to be used in redpesk
URL:     https://github.com/redpesk-samples/helloworld-binding
Source:  %{name}-%{version}.tar.gz

%bcond_with coverage
%bcond_with cpp

%if %{with cpp}
%global cpp_build ON
%else
%global cpp_build OFF
%endif

%global _afmappdir %{_prefix}/redpesk

%if %{with coverage}
%global coverage_dir %{_libexecdir}/redtest/%{name}/coverage_data
%endif

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(afb-binding)

%description
Provides a simple API showcasing the basics of binding development

%package redtest
Summary: redtest package
Requires: %{name} = %{version}-%{release}
Requires: afb-test-py
Requires: afb-libpython
Requires: pkgconfig(afb-binding)
%if %{with coverage}
Requires: gcc
%endif

%description redtest
This package contains the redtest test suite. Coverage support is disabled by
default and can be enabled at build time with --with coverage.

%prep
%autosetup -p 1

%build
mkdir build && cd build
%cmake \
  -DCPP=%{cpp_build} \
  -DAFM_APP_DIR=%{_afmappdir} \
%if %{with coverage}
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

# Install redtest scripts (for testing)
install -Dm755 redtest/run-redtest %{buildroot}%{_libexecdir}/redtest/%{name}/run-redtest
install -Dm755 redtest/gcov-total.sh %{buildroot}%{_libexecdir}/redtest/%{name}/gcov-total.sh
install -Dm644 redtest/tests.py %{buildroot}%{_libexecdir}/redtest/%{name}/tests.py

%if %{with coverage}
# The main package already contains the instrumented binding used by redtest.
# Preserve the CMake build directory in the coverage metadata layout. Runtime
# .gcda files generated through GCOV_PREFIX/GCOV_PREFIX_STRIP keep this level
# (for example redhat-linux-build/), so .gcno files must use the same path.
mkdir -p %{buildroot}%{coverage_dir}
cd build
find . -name "*.gcno" -exec cp --parents {} %{buildroot}%{coverage_dir}/ \;
cd ..

# Enable coverage in the installed redtest runner.
sed -i 's/^COVERAGE=no$/COVERAGE=yes/' \
  %{buildroot}%{_libexecdir}/redtest/%{name}/run-redtest
%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md CHANGELOG
%dir %{_afmappdir}/%{name}
%{_afmappdir}/%{name}/lib/
%{_afmappdir}/%{name}/.rpconfig/

%files redtest
%defattr(-,root,root)
%{_libexecdir}/redtest/%{name}/run-redtest
%{_libexecdir}/redtest/%{name}/gcov-total.sh
%{_libexecdir}/redtest/%{name}/tests.py
%if %{with coverage}
%{coverage_dir}
%endif
