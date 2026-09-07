# Build and Installation

## Prerequisites

The recommended development environment is the redpesk SDK, which provides the AFB development stack and the packages required to build bindings.

For more information, see [Setup your build host](https://docs.redpesk.bzh/docs/en/master/getting_started/host-configuration/docs/1-Setup-your-build-host.html) and [Getting the binder](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-getting.html) in the official redpesk documentation.

The main build dependencies are:

- CMake;
- a C compiler, and a C++ compiler when building the C++ implementation;
- `json-c` development files;
- AFB Binding V4 development files (`afb-binding >= 4.1.0`).

When the redpesk source repositories are configured, the RPM build dependencies can be installed with:

```bash
dnf builddep helloworld-binding
```

## Install from packages

On a system configured with the appropriate redpesk repositories, install the binding with:

```bash
dnf install helloworld-binding
```

The packaged binding is installed under:

```text
/usr/redpesk/helloworld-binding/
```

The shared library is located at:

```text
/usr/redpesk/helloworld-binding/lib/helloworld-binding.so
```

To verify the installed files, run:

```bash
rpm -ql helloworld-binding
```

For package deployment on a redpesk target, refer to the [redpesk application deployment documentation](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/deployment.html).

## Build from sources

Clone the project and configure a build directory:

```bash
git clone https://github.com/redpesk-samples/helloworld-binding.git
cd helloworld-binding
cmake -S . -B build
```

Build the binding:

```bash
cmake --build build
```

The resulting shared library is:

```text
build/helloworld-binding.so
```

## Build the C++ implementation

The C implementation is selected by default. To build the C++ implementation instead, enable the `CPP` CMake option:

```bash
cmake -S . -B build-cpp -DCPP=ON
cmake --build build-cpp
```

The generated library exposes the same `helloworld` API as the C implementation.

## Install a source build

A source build can be installed with the standard CMake installation mechanism:

```bash
sudo cmake --install build
```

The installation prefix can be customized at configuration time with `CMAKE_INSTALL_PREFIX` and the application directory with `AFM_APP_DIR`.

For development and validation, installing the source build is not required: `afb-binder` can load the shared library directly from the build directory.
