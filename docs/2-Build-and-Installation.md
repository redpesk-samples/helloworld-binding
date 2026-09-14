# Build and Installation

## Prerequisites

The recommended development setup is to build and install the redpesk framework locally from sources. This avoids relying on a prepackaged SDK and allows the framework to be used on different Linux distributions. Follow [Build framework on your computer](https://docs.redpesk.bzh/docs/en/master/redpesk-os/host-build/README.html) to prepare the AFB development environment.

### Build in the SDK container

As an alternative to installing the development environment directly on the host, the redpesk SDK container provides an isolated environment for building the sample. See the [SDK container overview](https://docs.redpesk.bzh/docs/en/master/redpesk-os/sdk-container/docs/0-overview.html) for an introduction.

Follow [SDK container setup](https://docs.redpesk.bzh/docs/en/master/redpesk-os/sdk-container/docs/1-setup.html) to prepare the container. Once the environment is started, the source-build commands documented below can be run from inside the container.

For binder usage, see [Getting the binder](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-getting.html).

The main build dependencies are:

- CMake;
- a C compiler, and a C++ compiler when building the C++ implementation;
- `json-c` development files;
- AFB Binding V4 development files (`afb-binding >= 4.1.0`).

When using an RPM-based redpesk development environment, the build dependencies can alternatively be installed with:

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
