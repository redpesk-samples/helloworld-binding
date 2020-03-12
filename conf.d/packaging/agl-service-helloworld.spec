###########################################################################
# Copyright 2015 - 2020 IoT.bzh
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
Version: 8.99.6
Release: 8%{?dist}
License: APL2.0
Summary: helloworld agl service set to be used in redpesk
URL:     https://github.com/redpesk/agl-service-helloworld
Source0: %{name}-%{version}.tar.gz

BuildRequires: afm-rpm-macros
BuildRequires: cmake
BuildRequires: gcc gcc-c++
BuildRequires: cmake-apps-module
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(libsystemd) >= 222
BuildRequires: pkgconfig(afb-daemon)
BuildRequires: pkgconfig(libmicrohttpd) >= 0.9.55
BuildRequires: pkgconfig(afb-helpers)

%description
The helloworld agl service gathers two bindings.
- helloworld-skeleton: Increment a counter
- helloworld-subscribe-event: Subscribe and get notified whether an event is emited

%afm_package_widget
%afm_package_widget_test

%prep
%autosetup -p 1

%build
%afm_configure_cmake_release
%afm_build_cmake
%afm_widget

%install
%afm_install_widget
%afm_install_widgettest

%check

%clean

%changelog
* Wed Feb 19 2020 IoT.bzh <redpesk.list.iot.bzh> 8.99.5
- Modifications in order to add a test subpackages

* Fri Feb 14 2020 IoT.bzh <redpesk.list.iot.bzh> 8.99.5
- Creation of the spec file from RedPesk generator
