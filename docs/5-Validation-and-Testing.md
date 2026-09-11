# Validation and testing

## Test strategy

The project provides functional tests for the public AFB API and a [redtest integration](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/quickstart/2_applications-sources.html) for execution in redpesk validation workflows.

The tests cover:

- `hello` replies with and without parameters;
- conversion of supported argument types for `hello`;
- `verb_called` event emission;
- valid `sum` requests, including empty arrays and signed 64-bit values;
- invalid `sum` requests;
- AFB request/reply behavior through the real binding loaded by the test binder.

## Test dependencies

The Python functional tests use `afb-test-py` and `afb-libpython`.

Prepare one of the development environments described in [Build and installation](./2-Build-and-Installation.html) before running the functional tests.

When using an RPM-based redpesk development environment, the test dependencies can alternatively be installed with:

```bash
sudo dnf install afb-binder afb-client afb-binding-devel afb-libpython afb-test-py
```

## Run the functional tests

Build the binding first:

```bash
cmake -S . -B build
cmake --build build
```

Then run the test suite with the build directory in the library search path:

```bash
LD_LIBRARY_PATH=./build python3 ./redtest/tests.py
```

To produce TAP output:

```bash
LD_LIBRARY_PATH=./build python3 ./redtest/tests.py --tap
```

The helper script `redtest/run.sh` can also be used for the default local build directory:

```bash
./redtest/run.sh
```

A successful run ends with all test cases reported as successful.

## redtest package

The RPM specification provides the `helloworld-binding-redtest` subpackage. The default coverage-enabled RPM build instruments the binding installed by the main `helloworld-binding` package. The redtest subpackage contains:

- `tests.py`;
- the `run-redtest` entry point;
- coverage metadata;
- the project sources under a stable path used by `lcov`.

The coverage build remaps build-time source paths to:

```text
/usr/libexec/redtest/helloworld-binding/sources
```

This allows target-side coverage tools to resolve the original source files after the temporary RPM build directory has disappeared.

Install it together with the binding on a compatible redpesk test environment:

```bash
dnf install helloworld-binding helloworld-binding-redtest
```

The installed test entry point is:

```text
/usr/libexec/redtest/helloworld-binding/run-redtest
```

It can be executed directly when validating the package:

```bash
/usr/libexec/redtest/helloworld-binding/run-redtest
```

## Test artifacts

The redtest runner produces validation artifacts under:

```text
/var/log/redtest/helloworld-binding/
```

The main outputs are:

- `helloworld.tap`: functional test results in TAP format;
- `coverage.xml`: code coverage in Cobertura-compatible XML format.

The runner returns a failure status when the TAP report contains a `not ok` result, allowing the test to be integrated into automated validation pipelines.

When `/var/log/redtest/helloworld-binding/` is not writable, for example during local development, the runner falls back to a `logs/` directory at the project root.

## Local coverage workflow

For local coverage collection, configure the regular `build/` directory with GCC coverage instrumentation:

```bash
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_FLAGS="--coverage -fPIC" \
  -DCMAKE_CXX_FLAGS="--coverage -fPIC"
cmake --build build
```

Then run the redtest entry point from the source tree:

```bash
./redtest/run-redtest
```

The runner detects whether it is executing from an installed redtest package or from the project source tree, configures the binding search path accordingly, captures LCOV data, and generates `coverage.xml`.

## redpesk validation workflow

The `-redtest` package is intended to make the sample usable in redpesk test campaigns in addition to local developer testing.

For integrating application tests into redpesk test campaigns, refer to the official [redtests in application sources](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/quickstart/2_applications-sources.html) documentation.
