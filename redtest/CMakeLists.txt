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

set(BINDING_NAME "agl-service-helloworld")
set(BINDING_TEST_NAME "agl-service-helloworld-test")
set(PACKAGE_REDTEST "agl-service-helloworld-redtest")

configure_file(run-redtest.in run-redtest @ONLY)

install(PROGRAMS ${CMAKE_BINARY_DIR}/redtest/run-redtest
	DESTINATION /usr/lib/${PACKAGE_REDTEST}/redtest)

