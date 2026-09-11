# Configuration and usage

## Runtime configuration

`helloworld-binding` does not require an application-specific runtime configuration file. For source-tree development, the binding is loaded by `afb-binder` and exposes the `helloworld` API. For the complete binder command-line interface, refer to the [`afb-binder` manual](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-binder.1.html).

When installed as a redpesk package, `manifest.yml` describes the packaged service and declares the `helloworld` API to the redpesk application framework. It is stored as `rpconfig/manifest.yml` in the sources and installed as `.rpconfig/manifest.yml` in the application directory.

## Run a source build

After building the project, start `afb-binder` and load the binding directly from the build directory:

```bash
afb-binder -v -b ./build/helloworld-binding.so
```

Unless another port is configured, the binder listens on port `1234`.

## Run the installed service

Start the packaged redpesk application through the application framework:

```bash
afm-util start helloworld-binding
```

Loading the installed shared library directly with `afb-binder` can be useful for development or debugging, but it bypasses the normal application-framework startup path and should not be used as the standard packaged-service workflow.

## Call the API

When the source build is started manually with `afb-binder` on the default port, use `afb-client` from another terminal:

```bash
afb-client -H localhost:1234/api helloworld hello
```

A packaged application started through `afm-util` may expose the API through a transport selected by the application framework, such as a Unix socket, so do not assume that `localhost:1234` is available in that mode. Use the endpoint provided by the application configuration.

Calls to the application verbs also publish the `helloworld/verb_called` event. See the [API reference](./4-API-Reference.html) for the complete verb, request, reply and event contract.

## Running on a redpesk target

The binding can be installed and executed on any compatible redpesk target using the same RPM package.

Target provisioning, image boot and package deployment are platform-level operations and are intentionally not duplicated in this project documentation:

- [Application deployment](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/deployment.html)
- [Booting a redpesk image with QEMU](https://docs.redpesk.bzh/docs/en/master/download/boards/docs/boards/qemu.html)

## Troubleshooting

If the binder cannot load the binding during local development, first verify that the shared library exists at the path passed to `-b` and that its runtime dependencies are available.

For an installed package:

```bash
rpm -ql helloworld-binding
```

For a local build:

```bash
ls -l ./build/helloworld-binding.so
```

Increase binder verbosity when diagnosing local API loading or request handling issues:

```bash
afb-binder -vvv -b ./build/helloworld-binding.so
```
