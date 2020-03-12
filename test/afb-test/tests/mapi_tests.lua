--[[
    Copyright (C) 2019 - 2020 "IoT.bzh"
    Author Marec Frédéric <frederic.marec@iot.bzh>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


    NOTE: strict mode: every global variables should be prefixed by '_'
--]]

_AFT.testVerbStatusSuccess("TestListSuccess", "mapi-helloworld", "list", {})

_AFT.testVerbStatusSuccess("TestSubscribeSuccess", "mapi-helloworld", "subscribe", {})

_AFT.testVerbStatusSuccess("TestUnsubscribeSuccess", "mapi-helloworld", "unsubscribe", {})

_AFT.testVerbStatusError("TestWrongVerbError", "mapi-helloworld", "wrong_verb", {})

_AFT.testVerbStatusSkipped("TestSkippedVerb", "mapi-helloworld", "skipped_verb", {})
