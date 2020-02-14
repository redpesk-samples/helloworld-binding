###########################################################################
# Copyright 2015, 2016, 2017 IoT.bzh
#
# author: Fulup Ar Foll <fulup@iot.bzh>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###########################################################################

%define debug_package %{nil}

Name:    agl-service-helloworld
Version: 8.99.5
Release: 1%{?dist}
License: APL2.0
Summary: helloworld agl service set to be used in redpesk
Url:     https://github.com/redpesk/agl-service-helloworld
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc gcc-c++
BuildRequires: cmake-apps-module
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(libsystemd) >= 222
BuildRequires: pkgconfig(afb-daemon)
BuildRequires: pkgconfig(libmicrohttpd) >= 0.9.55
BuildRequires: pkgconfig(afb-helpers)
Requires: agl-app-framework-main
Requires: agl-app-framework-binder


%description
helloworld agl service set to be used in redpesk

%prep
%autosetup

%build
[ ! -d build ] && mkdir build
cd build
%cmake -DVERSION=%{version} -DCMAKE_BUILD_TYPE=RELEASE ..
%__make %{?_smp_mflags}
%__make widget

%install
install -d %{?buildroot}/%{_prefix}/AGL
install -m 0644 %{_builddir}/%{name}-%{version}/build/%{name}.wgt %{?buildroot}/%{_prefix}/AGL

%files
%{_prefix}/AGL/%{name}.wgt

%post
afm-util install /usr/AGL/%{name}.wgt

