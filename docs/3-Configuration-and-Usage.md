# Configuration and Usage

## Runtime configuration

`helloworld-binding` does not require an application-specific runtime configuration file. The binding is loaded by `afb-binder` and exposes the `helloworld` API. For the complete binder command-line interface, refer to the [`afb-binder` manual](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-binder.1.html).

When installed as a redpesk package, `.rpconfig/manifest.yml` describes the packaged service and declares the `helloworld` API to the redpesk application framework.

## Run a source build

After building the project, start `afb-binder` and load the binding directly from the build directory:

```bash
afb-binder -v -b ./build/helloworld-binding.so
```

Unless another port is configured, the binder listens on port `1234`.

## Run the installed binding

For an RPM installation, load the packaged shared library:

```bash
afb-binder -v -b /usr/redpesk/helloworld-binding/lib/helloworld-binding.so
```

## Call the API

Use `afb-client` from another terminal to call the API.

Call `hello` without an argument:

```bash
afb-client -H localhost:1234/api helloworld hello
```

The reply contains:

```text
Hello world!
```

Call `hello` with a value:

```bash
afb-client -H localhost:1234/api helloworld hello Bob
```

The reply contains:

```text
Hello Bob!
```

Call `sum` with a JSON array of integers:

```bash
afb-client -H localhost:1234/api helloworld sum '[1,2,3,4]'
```

The returned value is `10`.

The complete request and response contract is described in the [API Reference](./4-API-Reference.html).

## Events

Calls to `hello` and `sum` publish the `helloworld/verb_called` event. The client is automatically subscribed the first time one of these verbs is called.

For example, calling `hello` produces an event whose payload is the called verb name:

```json
{
  "event": "helloworld/verb_called",
  "data": "hello"
}
```

This behavior demonstrates AFB event publication, subscription and per-client context management in a minimal example.

## Running on a redpesk target

The binding can be installed and executed on any compatible redpesk target using the same RPM package.

Target provisioning, image boot and package deployment are platform-level operations and are intentionally not duplicated in this project documentation:

- [Application deployment](https://docs.redpesk.bzh/docs/en/master/getting_started/docs/deployment.html)
- [Booting a redpesk image with QEMU](https://docs.redpesk.bzh/docs/en/master/download/boards/docs/boards/qemu.html)

## Troubleshooting

If the binder cannot load the binding, first verify that the shared library exists at the path passed to `-b` and that its runtime dependencies are available.

For an installed package:

```bash
rpm -ql helloworld-binding
```

For a local build:

```bash
ls -l ./build/helloworld-binding.so
```

Increase binder verbosity when diagnosing API loading or request handling issues:

```bash
afb-binder -vvv -b ./build/helloworld-binding.so
```
