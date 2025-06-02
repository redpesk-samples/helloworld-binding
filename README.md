[![Pipeline Status](https://git.ovh.iot/redpesk/redpesk-samples/helloworld-binding/badges/master/pipeline.svg)](https://git.ovh.iot/redpesk/redpesk-samples/helloworld-binding/-/pipelines)


# helloworld binding

A binding example, implemented in a redpesk context
![rp_image](https://avatars2.githubusercontent.com/u/58298458?s=400&v=4?raw=true)

## Pre-requisites

To follow this tutorial without inconvenience, you have to get the following tools ready to use:

- wget

- xz

- ssh

- qemu (more details at a later stage)

Moreover, in order to use redpesk services, you must register [here](https://community-app.redpesk.bzh/signup) ! You can either use a GitHub or a GitLab account.

## Project configuration

Refer to the [documentation](https://docs.redpesk.bzh/) for detailed guidance on creating and configuring your redpesk project and application setup.

#### ⚠️ Key consideration

Ensure that the application name specified in your spec file matches the name used during the application's creation.


## Deploy on a board

Now that a helloworld-binding package has been generated using redpesk, let's see how to install it on a board. Since redpesk supports cross-compilation, we will use an emulated x86_64 board (**qemu-x86_64**) for this purpose.

Refer to the [documentation](https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/qemu.html#download-the-x86_64-image) for detailed instructions on installing QEMU.

### Getting a redpesk image

Download the latest redpesk image according to your board architecture.

For more details, please refer to the documentation [here](https://docs.redpesk.bzh/docs/en/master/redpesk-os/boards/docs/boards/up-board.html).

```bash
$ mkdir ~/redpeskimage

$ cd ~/redpeskimage

$ wget -r -nd -nc --no-parent --accept-regex='redpesk.*smack.*\.(bmap|xz|sha256)' --reject-regex '(image\.raw|ova|index)' 'https://download.redpesk.bzh/redpesk-lts/batz-2.1-update/images/smack/minimal/x86_64/generic/'

$ tar xJf redpesk*.tar.xz
```

### Running a redpesk image

Here we are, you are about to run the redpesk image. 

```bash
$ ls
redpesk-lts-batz-2.1-update-smack-minimal-x86_64-generic-2025_04_10_0641.bmap           Redpesk-OS.img
redpesk-lts-batz-2.1-update-smack-minimal-x86_64-generic-2025_04_10_0641.tar            Redpesk-OS.img.bmap
redpesk-lts-batz-2.1-update-smack-minimal-x86_64-generic-2025_04_10_0641.tar.xz.sha256

```

The image you have just downloaded has the following configuration:

- login: root

- password: root

Then, simply run the redpesk image by doing:

```bash
export TCP_PORT=3333
qemu-system-x86_64 \
  -hda Redpesk-OS.img \
  -enable-kvm \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=/usr/share/OVMF/OVMF_VARS.fd \
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

### Installing your package

After building your package, refer to the documentation [here](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/deployment.html), specifically section 4: "Install your package," to proceed with the installation.


If you correctly set your project name and version as explained in the **Build** part, you should have the following output during the package installation

```bash
[root@localhost ~]# dnf install helloworld-binding --nogpgcheck
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered with an entitlement server. You can use subscription-manager to register.

hello-2_f098e52f--redpesk-lts-batz-2.1-update-build                                  4.8 kB/s | 2.1 kB     00:00    
redpesk-lts-batz-2.1-update-build                                                    2.0 MB/s | 6.3 MB     00:03    
redpesk-lts-batz-2.1-update-middleware-build                                         608 kB/s | 324 kB     00:00    
redpesk-config-build                                                                 3.5 kB/s | 1.6 kB     00:00    
RedPesk Middleware batz-2.1 Update - x86_64                                          658 kB/s | 323 kB     00:00    
RedPesk Baseos batz-2.1 Update - x86_64                                              9.0 MB/s | 7.9 MB     00:00    
RedPesk Config                                                                       2.8 kB/s | 903  B     00:00    
Dependencies resolved.
=====================================================================================================================
 Package            Arch   Version                         Repository                                           Size
=====================================================================================================================
Installing:
 helloworld-binding x86_64 1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1
                                                           hello-2_f098e52f--redpesk-lts-batz-2.1-update-build  13 k

Transaction Summary
=====================================================================================================================
Install  1 Package

Total download size: 13 k
Installed size: 16 k
Is this ok [y/N]: y
Downloading Packages:
helloworld-binding-1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1.x86_64.r  64 kB/s |  13 kB     00:00    
---------------------------------------------------------------------------------------------------------------------
Total                                                                                 60 kB/s |  13 kB     00:00     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                             1/1 
  Installing       : helloworld-binding-1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1.x86_64          1/1 
  Running scriptlet: helloworld-binding-1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1.x86_64          1/1 
  Verifying        : helloworld-binding-1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1.x86_64          1/1 
Installed products updated.

Installed:
  helloworld-binding-1.1.1+20240722+30+ga9c2297-1.hello.2_f098e52f.rpbatz_1_1.x86_64                                 

Complete!
```

This implies that your widget has been installed correctly.

Verify if your package is properly installed :

```bash
[root@localhost ~]# rpm -ql helloworld-binding
/usr/lib/.build-id
/usr/lib/.build-id/12
/usr/lib/.build-id/12/87c1ceb24a017dc7318252044c04533873f330
/usr/redpesk
/usr/redpesk/helloworld-binding
/usr/redpesk/helloworld-binding/.rpconfig
/usr/redpesk/helloworld-binding/.rpconfig/manifest.yml
/usr/redpesk/helloworld-binding/lib
/usr/redpesk/helloworld-binding/lib/helloworld-binding.so
```

You can then start the binding by running:

```bash
[root@localhost ~]# afb-binder -v -b /usr/redpesk/helloworld-binding/lib/helloworld-binding.so
```
The binder has started successfully.

```bash
   NOTICE: Browser URL= http://localhost:1234
   NOTICE: Serving rootdir=. uploaddir=.
   NOTICE: API helloworld starting...
   NOTICE: API monitor starting...
   NOTICE: Listening interface *:1234
   NOTICE: [REQ/API helloworld] context initialized for new client
```

In another terminal on the same machine (you can open one terminal with SSH and another terminal with QEMU for the same machine), you can query the verb `hello`, for example:

```bash
[root@localhost ~]# afb-client -H localhost:1234/api helloworld hello
```
and the response with success

```bash
implicit null in arguments is deprecated and will be removed soon.
ON-EVENT helloworld/verb_called:
{
  "jtype":"afb-event",
  "event":"helloworld/verb_called",
  "data":"hello"
}
ON-REPLY 1:helloworld/hello: OK
{
  "jtype":"afb-reply",
  "request":{
    "status":"success",
    "code":0
  },
  "response":"Hello world!"
}
```

## Automated testing in a non-embedded environment

Since this helloworld binding is not connected to real hardware, it can be run and tested on a Linux workstation.

In order to run the tests you need afb-libpython. It is available in redpesk SDK.

If you haven't already, please follow the quick installation guide available [here](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-getting.html#add-the-sdk-repository) to ensure your platform is supported and properly set up.

Install then Python bindings on your platform thanks to your distribution's tools: 
```bash
sudo dnf install afb-binder afb-client afb-binding-devel afb-libpython
```


### Build the project

To build the `helloworld-binding` binding, follow these steps after cloning the repository onto your host machine:


```bash
cd helloworld-binding # this repo

# Create a build directory
mkdir build
cd build

# Configure the build system
/helloworld-binding/build$ cmake ..
-- The C compiler identification is GNU 14.2.1
-- The CXX compiler identification is GNU 14.2.1
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found PkgConfig: /usr/bin/pkg-config (found version "2.3.0")
-- Checking for modules 'json-c;afb-binding>=4.1.0'
--   Found json-c, version 0.17
--   Found afb-binding, version 4.1.11
-- Configuring done (0.9s)
-- Generating done (0.0s)
-- Build files have been written to: /home/iheb/orig/helloworld-binding/build

# Build the project
/helloworld-binding/build$ make
[ 25%] Generating info_verb.c
[ 50%] Building C object CMakeFiles/helloworld-binding.dir/src/helloworld.c.o
[ 75%] Building C object CMakeFiles/helloworld-binding.dir/info_verb.c.o
[100%] Linking C shared library helloworld-binding.so
[100%] Built target helloworld-binding
```
You can see that the build process has successfully generated the `helloworld-binding.so` file for the binding.

```bash
/helloworld-binding/build$ ls
CMakeCache.txt  CMakeFiles  cmake_install.cmake  helloworld-binding.so  info_verb.c  Makefile
```
### Test binding

Now you can test either manually, as demonstrated earlier on QEMU using `afb-binder` and `afb-client`, or automatically using the script `./tests/tests.py`.

```bash
LD_LIBRARY_PATH=./build python  ./tests/tests.py --tap
```

Then a prompt appears in TAP format, describing which test is currently running and whether it succeed or failed.

```bash
$ LD_LIBRARY_PATH=./build python  ./tests/tests.py
Entering Python module initialization function PyInit_libafb
     INFO: API py-binder added
     INFO: API monitor added
     INFO: binding [helloworld-binding.so] looks like an AFB binding V4
     INFO: API helloworld added
   NOTICE: Entering binder mainloop
   NOTICE: API helloworld starting...
     INFO: API helloworld started
   NOTICE: API py-binder starting...
     INFO: API py-binder started
   NOTICE: API monitor starting...
     INFO: API monitor started
   NOTICE: [REQ/API helloworld] context initialized for new client
.   NOTICE: Entering binder mainloop
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[0]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[1]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[2]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[3]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[4]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[5]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[6]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[7]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[8]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[9]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[10]
.   NOTICE: Entering binder mainloop
.   NOTICE: Entering binder mainloop
.   NOTICE: Entering binder mainloop
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[11]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[12]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[13]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[14]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[15]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[16]
    ERROR: [API helloworld] parameter should be a JSON array of integers [/home/iheb/orig/helloworld-binding/src/helloworld.c:165,sum_verb]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[17]
    ERROR: [API helloworld] parameter should be a JSON array of integers [/home/iheb/orig/helloworld-binding/src/helloworld.c:165,sum_verb]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[18]
    ERROR: [API helloworld] parameter should be a JSON array of integers [/home/iheb/orig/helloworld-binding/src/helloworld.c:165,sum_verb]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[19]
    ERROR: [API helloworld] parameter should be a JSON array of integers [/home/iheb/orig/helloworld-binding/src/helloworld.c:165,sum_verb]
     INFO: [API py-binder] orphan event=[helloworld/verb_called] count=[20]

.
----------------------------------------------------------------------
Ran 5 tests in 0.012s

OK

```




