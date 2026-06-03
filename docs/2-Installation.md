# Installation

## From package

You can run the same command on a target runing a redpesk OS or in the [SDK container]({% chapter_link sdk-container-doc.overview %}) (development mode).

```bash
dnf install helloworld-binding
```

## From sources

When developing inside the SDK container, to install the build dependencies, run the following command:

```bash
dnf builddep helloworld-binding
```

Then clone and build from sources.

```bash
git clone https://github.com/redpesk-samples/helloworld-binding.git
cd helloworld-binding
export WORK_DIR="${PWD}"
mkdir build
cd build
cmake -DVERSION=8.99.6 ..
make 
```

> Note: To rebuild all (including application framework) from sources, please refer to this [chapter]({% chapter_link host-build-doc.build-framework-on-your-computer %}).
