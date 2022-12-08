# Installation 

## Prerequisites

This part is only useful if you plan to install the package from source.

We advise you to use the [local builder]({% chapter_link local-builder-doc.installation %}) for from source installation. The local builder comes with everything setup to build redpesk@ projects.

Else install the building tools

* gcc
* g++
* make
* cmake
* afb-cmake-modules

Then the following dependencies:

* json-c
* libsystemd
* afb-daemon
* libafb
* libmicrohttpd
* afb-libhelpers

Fedora/OpenSuse:
```bash
dnf install gcc-c++ make cmake afb-cmake-modules json-c-devel afb-binding-devel libmicrohttpd-devel afb-libhelpers-devel pkg-config
```

Ubuntu:
```bash
apt install gcc g++ make cmake afb-cmake-modules libsystemd-dev libjson-c-dev afb-binding-dev libmicrohttpd-dev afb-libhelpers-dev pkg-config
```

## Build

```bash
git clone https://github.com/redpesk-samples/helloworld-binding.git
cd helloworld-binding
export WORK_DIR="${PWD}"
mkdir build
cd build
cmake -DVERSION=8.99.6 ..
make 
```
