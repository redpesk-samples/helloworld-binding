# agl-service-helloworld

A binding example for AGL, implemented in a redpesk® context
![rp_image](https://avatars2.githubusercontent.com/u/58298458?s=400&v=4?raw=true)

## Pre-requisites

To follow this tutorial without inconvenience, you have to get the following tools ready to use:

- wget

- xz

- ssh

- qemu (more details at a later stage)

Moreover, in order to use redpesk® services, you must register [here](https://auth.redpesk.bzh/dex/auth?client_id=redpesk&redirect_uri=http%3A%2F%2Fruntime.redpesk.iot%3A8000%2Foauth%2Fcallback&response_type=code&scope=openid+profile+email&state=jIfn4y6gTEG87Asvj2DAxcK2WJv63ASW) ! You can either create your own account, or use your GitHub one.

## Build

The aim of this part is to create a package which contained the agl-service-helloworld application.

### Specfile

In order to correctly build an RPM package in the redpesk® context, your project should contain a specfile.
The agl-service-helloworld specfile can be found at the following path:
[conf.d/packaging/agl-service-helloworld.spec](conf.d/packaging/agl-service-helloworld.spec).
This specfile will be used by redpesk® to describe how to build your AGL application. The resulting build produces an AGL widget that is embedded in a RPM.
Please read the [documentation](https://docs.redpesk.bzh/) to correctly create and set your redpesk® project and application set up.
You may have noticed that the agl-service-helloworld specfile contained several afm rpm macros, such as `%afm_package`.
These macros allow to define a specfile template for AGL application.
For example the three following macros indicate that this package is composed by three sub-packages

- `%afm_package` &rarr; agl-service-helloworld: which is basically the core widget

- `%afm_package_test` &rarr; agl-service-helloworld-test: which is a widget, implementing the tests used to validate the source code. Test source files are located in [test](test) directory

- `%afm_package_redtest` &rarr; agl-service-helloworld-redtest: this package is the one used by the RedPesk infrastructure to run the test. It requires the package agl-service-helloworld-test where the tests truly are. In the case of agl binding test (this is the case here), this package only contains a script that calls the right command to run the agl tests. This script can be found in the [redtest](redtest) directory.

### Project configuration

However, to fit the template introduced by afm rpm macros, your project should match two requirements.
Both of these requirements are taking place in [conf.d/cmake/config.cmake](conf.d/cmake/config.cmake).

- **Project name**
  Your project name should match your package name.
  Here for example in the agl-helloworld-service config.cmake, we can see:
  `set(PROJECT_NAME agl-service-helloworld)`
  Thus the package must be named `agl-service-helloworld`.

- **Project version**
  For convenience, we advise you not to set the project version in the config.cmake.
  ~~`set(PROJECT_VERSION "1.0")`~~
  By doing so, your project version will automatically be set to the version listed in the specfile.
  This tweak allows afm macros to be fully effective regarding your widget management once deployed on a board.

## Deploy on a board

Now that an agl-service-helloworld package have been generated thanks to redpesk®, let's see how to install it on a board.
Since redpesk® support cross-compilation, we can use either a x86_64 or aarch64 board to get your package installed in.
During this part, two cases will be studied:

- Emulated x86_64 board: **qemu-x86_64**

- Real aarch64 board: **m3ulcb**

If you want to use the agl-helloworld-service in an embedded aarch64 context, but do not have a real board, an other tutorial is present in the repository that you can find at the following [path](docs/qemu-aarch64.md).

### Getting a redpesk® image

Download the latest redpesk® image according to your board architecture.

- **qemu-x86_64**

```bash
export RP_IMAGE=RedPesk-minimal-8_II-1.x86_64.raw.xz
wget https://download.redpesk.bzh/redpesk-devel/releases/28/images/minimal/x86_64/$RP_IMAGE
```

- **m3ulcb**

```bash
export RP_IMAGE=RedPesk-minimal-8_II-1.aarch64.raw.xz
wget https://download.redpesk.bzh/redpesk-devel/releases/28/images/minimal/aarch64/latest/$RP_IMAGE
```

The image you have just downloaded has the following configuration:

- login: root

- password: root

### Running a redpesk® image

Here we are, you are about to run the redpesk® image. This section will deal with both types of image: x86_64 & aarch64.

- **qemu-x86_64**

First of all unzip the archive you have just downloaded to retrieve the redpesk® image.

```bash
xz -d --verbose ${RP_IMAGE}
```

Then download the qemu-kvm package. For example, Ubuntu user can run:

```bash
sudo apt install qemu-kvm
```

Then, simply run the redpesk® image by doing:

```bash
export TCP_PORT=3333
qemu-system-x86_64 \
        -hda ${PATH_TO_REDPESK_IMAGE} \
        -enable-kvm \
        -bios /usr/share/qemu/OVMF.fd \
        -machine q35 \
        -m 2048 \
        -cpu kvm64 \
        -cpu qemu64,+ssse3,+sse4.1,+sse4.2,+popcnt \
        -net nic \
        -net user,hostfwd=tcp::${TCP_PORT}-:22 \
        -nographic \
        -snapshot
```

You may have noticed that in the previous command we allow the user to connect to the emulated board by establishing a ssh connection through the port `${TCP_PORT}`.

You can access your emulated board with the following command:

```bash
ssh root@localhost -p ${TCP_PORT}
```

- **m3ulcb**

The aim of this part is to flash the redpesk® raw image on a SDCard. To do so, bmaptools will be used. For example, ubuntu user can run:

```bash
sudo apt-get install bmap-tools
```

Then insert your SDCard and retrieve its device name. To do so you can execute the following command:

```bash
lsblk -dli -o NAME,TYPE,HOTPLUG | grep "disk.*1$"
```

Then export it into the environment variable DEVICE, for example:

```bash
export DEVICE="/dev/sdb"
```

If the SDCard is mounted, umount it.

```bash
sudo unmount ${DEVICE}
```

Now write the image onto the SDCard.

```bash
sudo bmaptool copy ${RP_IMAGE} ${DEVICE}
```

Since then, your SDCard is bootable. You can access it by using the ssh command:

```bash
export YOUR_BOARD_IP=192.168.1.X
ssh root@${YOUR_BOARD_IP}
```

### Installing your package

There are no difference in the command related to your package installation, neither in a x86_64, nor in an aarch64 redpesk® distribution.

Once you get in your redpesk® image, you can proceed to the package installation.
As a reminder, the agl-helloworld-service gathered two sub-package the **agl-service-helloworld** and the **agl-service-helloworld-test**.
To install the widget sub-package, you can simply run

```bash
dnf install agl-service-helloworld
```

If you correctly set your project name and version as explained in the **Build** part, you should have the following output during the package installation

```bash
[root@localhost ~] dnf install agl-service-helloworld
NOTICE: -- Install redpesk widget from /var/local/lib/afm/applications/agl-service-helloworld --
```

This implies that your widget has been installed correctly.

Check if your widget id is `agl-service-helloworld`.

```bash
afm-util list --all
[
  {
    "description":"Provide an AGL Helloworld Binding",
    "name":"agl-service-helloworld",
    "shortname":"",
    "id":"agl-service-helloworld",
    "version":"8.99",
    "author":"Iot-Team <frederic.marec@iot.bzh>",
    "author-email":"",
    "width":"",
    "height":"",
    "icon":"/var/local/lib/afm/applications/agl-service-helloworld/icon.png",
    "http-port":30001
  }
]
```

You can then start the service by running:

```bash
[root@localhost ~] afm-util start agl-service-helloworld
8628
```

For example, you can access to its verb **ping** which belong to its api **helloworld** thanks to a HTTP or websocket request sent to the port `$PORT` such as follow

- HTTP request:

```bash
curl -H "Content-Type: application/json" http://localhost:${PORT}/api/helloworld/ping | jq
```

- Websocket request:

```bash
afb-client-demo -H ws://localhost:${PORT}/api?token=x\&uuid=magic helloworld ping
```

For both requests you should get the following answer from the first request

```bash
ON-REPLY 1:helloworld/ping: OK
{
  "response":0,
  "jtype":"afb-reply",
  "request":{
    "status":"success",
    "info":"Ping count = 0"
  }
}
```

Once again, if you correctly set your project name and version as explained in the **Build** part, to correctly stop and remove your widget, simply run

```bash
dnf remove agl-service-helloworld
```

You should have the following output

```bash
[root@localhost ~] dnf remove agl-service-helloworld-widget
INFO:  kill agl-service-helloworld
INFO:  uninstall agl-service-helloworld
```

## TEST

As explained before, the agl-helloworld service package contained a test sub-package.
This package implements a set of function meant to test the agl-service-helloworld-widget functionalities.
First of all ensure you installed the **agl-service-helloworld**. Then proceed to the test related package installation.

```bash
dnf install agl-service-helloworld-test
```

If you correctly set your project name and version as explained in the Build part, the test widget should be installed in your target.
Keep in mind that to launch tests, the core widget needs to be installed and **currently running** on the target.

```bash
[root@localhost ~] dnf install agl-service-helloworld-test
INFO:  agl-service-helloworld-test installation
```

Now that the test sub-package has been installed.

Check if the widget id is `agl-service-helloworld-test`.

```bash
afm-util list --all
```

In order to launch the test, you must run the following command passing the widget id.

```bash
afm-test agl-service-helloworld-test
```

Then a prompt appears in TAP format, describing which test is currently running and whether it succeed or failed.

```bash
[root@localhost ~] afm-test agl-service-helloworld-test
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
