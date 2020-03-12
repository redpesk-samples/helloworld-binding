# Native build

## Pre-requisites

### Distribution

To run this application in your host, you should first ensure that your distribution is one of the following AGL supported distributions that you can find [here](http://download.opensuse.org/repositories/isv:/LinuxAutomotive:/AGL_Master/)

### Framework

Since AGL widget can be built in a "native" distribution, here is a [guide](https://docs.automotivelinux.org/docs/en/master/devguides/reference/2-download-packages.html)
to add the AGL-Master repository to your distribution.  
After this, do not forget to source the agl shell script

```bash
source /etc/profile.d/agl-app-framework-binder.sh
```

Obviously you must clone this package

```bash
git clone https://github.com/redpesk/agl-service-helloworld.git
cd agl-service-helloworld
export WORK_DIR="${PWD}"
```

## Needed packages

Then here is a list of packages you must installed in your host to build the agl-service-helloworld.

* agl-cmake-apps-module-bin

* libjson-c-dev

* agl-libafb-helpers-dev

## Build

Then to build the project, since we do not set the version in the code because of the afm-rpm-macros, we have to set it manually.  
To do so, check the variable `VERSION` in the specfile  and export it in your terminal, for example let say:  

```bash
export VERSION=8.99.6
```

Then you can build the agl-service-helloworld by doing the following commands:

```bash
cd ${WORK_DIR}
mkdir build && cd build
cmake -DVERSION=${VERSION} -DBUILD_TEST_WGT=TRUE ..
make widget
```

Notice the flag `-DBUILD_TEST_WGT=TRUE` which build the test widget.

## Run

The previous part has generated the two widgets presented in the [README.md](https://github.com/redpesk/agl-service-helloworld/blob/master/README.md)  

* **agl-service-helloworld.wgt**

* **agl-service-helloworld-test.wgt**

Notice that a widget is just an archive, and there content is located respectively in :  

* `${WORK_DIR}/build/package`

* `${WORK_DIR}build/package-test`

### Application

In the first time, launch your helloworld application by doing

```bash
export PORT=9999
afb-daemon --port=${PORT} --workdir=${WORK_DIR}/build/package --ldpaths=lib -vvv
```

Now your application is reachable by HTTP or websocket through the port `${PORT}`.  
Open a new terminal and do the following requests:

* **HTTP**

```bash
curl -H "Content-Type: application/json" http://localhost:${PORT}/api/helloworld/ping | jq
```

* **websocket**

```bash
afb-client-demo -H ws://localhost:${PORT}/api?token=x\&uuid=magic helloworld ping
```

### Tests

For launching the **agl-service-helloworld-test**, you should first install the AGL application test framework. For example, Ubuntu user can run:  

```bash
sudo apt install agl-app-afb-test-dev
```

Then launch the helloworld test by doing:  

```bash
afm-test ${WORK_DIR}/build/package ${WORK_DIR}/build/package-test
```

Then the test output in TAP format should prompt in your terminal as follow:  

```bash
1..6
# Started on Wed Mar 11 09:42:52 2020
# Starting class: testPingSuccess
~~~~~ Begin testPingSuccess ~~~~~
~~~~~ End testPingSuccess ~~~~~
ok     1        testPingSuccess.testFunction
# Starting class: testPingSuccessAndResponse
ok     2        testPingSuccessAndResponse.testFunction
# Starting class: testPingSuccessCallback
ok     3        testPingSuccessCallback.testFunction
# Starting class: testPingError
ok     4        testPingError.testFunction
# Starting class: testPingErrorAndResponse
ok     5        testPingErrorAndResponse.testFunction
# Starting class: testPingErrorCallback
ok     6        testPingErrorCallback.testFunction
# Ran 6 tests in 0.000 seconds, 6 successes, 0 failures
1..5
# Started on Wed Mar 11 09:42:52 2020
# Starting class: TestListSuccess
ok     1        TestListSuccess.testFunction
# Starting class: TestSubscribeSuccess
ok     2        TestSubscribeSuccess.testFunction
# Starting class: TestUnsubscribeSuccess
ok     3        TestUnsubscribeSuccess.testFunction
# Starting class: TestWrongVerbError
ok     4        TestWrongVerbError.testFunction
# Starting class: TestSkippedVerb
ok     5    # SKIP Test (mapi-helloworld, skipped_verb, table: 0x55bb25dd0680, nil) is skipped
# Ran 4 tests in 0.001 seconds, 4 successes, 0 failures, 1 skipped
Tests correctly launched.
```

A file entitled `test.log` can be found from where you launch the afm-test command.  
This files gathered more information than the terminal output and can be useful whenever you want to debug the tests.
