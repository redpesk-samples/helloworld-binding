# Usage

The [installation chapter](./2-Installation.html) has generated the two binding:

* **helloworld-skeleton**

* **helloworld-subscribe-event**

## Application

In the first time, launch your helloworld application by doing

```bash
export PORT=9999
afb-binder --workdir=${WORK_DIR}/build/package --binding=lib/afb-helloworld-skeleton.so --port=${PORT} -vvv
```

Your output will be like:

```bash
------BEGIN OF CONFIG-----
-- {
--   "workdir": "${WORK_DIR}/build/package",
--   "binding": [
--     "lib/afb-helloworld-skeleton.so"
--   ],
--   "port": 9999,
--   "apitimeout": 20,
--   "cache-eol": 100000,
--   "cntxtimeout": 32000000,
--   "session-max": 200,
--   "jobs-max": 200,
--   "threads-max": 5,
--   "uploaddir": ".",
--   "rootbase": "/opa",
--   "rootapi": "/api",
--   "rootdir": ".",
--   "log": "error+warning+notice+info+debug"
-- }
------END OF CONFIG-----
INFO: running with pid 1097
INFO: API monitor added
INFO: Cant connect supervision socket to @urn:AGL:afs:supervision:socket: Connection refused
INFO: binding [lib/afb-helloworld-skeleton.so] looks like an AFB binding V3
INFO: API helloworld added
DEBUG: Init config done
NOTICE: API helloworld starting...
INFO: API helloworld started
NOTICE: API monitor starting...
INFO: API monitor started
NOTICE: Serving rootdir=. uploaddir=.
NOTICE: Listening interface *:9999
NOTICE: Browser URL= http://localhost:9999
```

Now your application is reachable by HTTP or websocket through the port `${PORT}`.  
Open a new terminal and do the following requests:

* **HTTP**

```bash
curl -H "Content-Type: application/json" http://localhost:${PORT}/api/helloworld/ping | jq
```

```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    89  100    89    0     0  29666      0 --:--:-- --:--:-- --:--:-- 29666
{
  "jtype": "afb-reply",
  "request": {
    "status": "success",
    "info": "Ping count = 0"
  },
  "response": 0
}
```

* **websocket**

```bash
afb-client -H ws://localhost:${PORT}/api?token=x\&uuid=magic helloworld ping
```

```bash
ON-REPLY 1:helloworld/ping: OK
{
  "jtype":"afb-reply",
  "request":{
    "status":"success",
    "info":"Ping count = 1"
  },
  "response":1
}
```

<!-- ### Tests

For launching the **helloworld-binding-test**, you should first install the Application test framework. For example, Ubuntu user can run:  

```bash
sudo apt install agl-app-afb-test-dev
```

Then launch the helloworld test by doing:  

```bash
afm-test ${WORK_DIR}/build/package ${WORK_DIR}/build/package-test
```

Then the test output in TAP format should prompt in your terminal as follow:  

A file entitled `test.log` can be found from where you launch the afm-test command.  
This files gathered more information than the terminal output and can be useful whenever you want to debug the tests. -->
