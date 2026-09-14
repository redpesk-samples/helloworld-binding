# Overview

## Purpose

`helloworld-binding` is a minimal [AFB Binding V4](https://docs.redpesk.bzh/docs/en/master/developer-guides/afb-binding-tutorial-v4.html) example intended to demonstrate the core mechanisms required to implement an AFB service in a redpesk environment.

The project is deliberately small so that the binding lifecycle, API implementation and test strategy remain easy to identify in the source code.

The sample demonstrates:

- an AFB V4 API and verbs;
- request parameter conversion and typed replies;
- binding lifecycle handling with `mainctl`;
- event creation and publication;
- per-client context management and event subscription;
- equivalent C and C++ implementations;
- functional validation with `afb-test-py` and redtest integration.

## Architecture

The binding exposes the `helloworld` API through [`afb-binder`](https://docs.redpesk.bzh/docs/en/master/redpesk-os/afb-binder/afb-overview.html).

```text
                 +----------------------+
                 |      AFB client      |
                 | afb-client / tests   |
                 +----------+-----------+
                            |
                            | AFB requests / events
                            v
                 +----------------------+
                 |      afb-binder      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | helloworld-binding.so|
                 |                      |
                 | API: helloworld      |
                 | - hello              |
                 | - sum                |
                 | - info               |
                 |                      |
                 | Event: verb_called   |
                 +----------------------+
```

The binding itself does not depend on external hardware. It can therefore be executed on a development host, in a redpesk development environment (like using the [localbuilder](https://docs.redpesk.bzh/docs/en/master/getting_started/local_builder_quickstart/docs/quickstart/0_quick-installation.html)), or on a redpesk target (QEMU, aarch64 or x86_64 [target](https://docs.redpesk.bzh/docs/en/master/download/boards/docs/boards/download-images.html)).

## Binding lifecycle

The binding registers a `mainctl` callback. During the AFB initialization stage, this callback creates the `verb_called` event used by the sample.

If the event cannot be created, the initialization fails. Other lifecycle stages are accepted without additional processing.

## Client context and events

The sample uses the AFB request context to keep a small per-client state indicating whether the client is already subscribed to the `verb_called` event.

When a client calls `hello` or `sum` for the first time, the binding:

1. creates the client context;
2. subscribes the client to `verb_called`;
3. pushes an event containing the name of the called verb.

Subsequent calls reuse the existing client context and subscription.

## C and C++ implementations

The same API is implemented in:

- `src/helloworld.c`, using the AFB C API;
- `src/helloworld.cpp`, using the AFB C++ wrapper.

The C implementation is built by default. The C++ implementation can be selected with the CMake `CPP` option.

This makes the project useful as a compact reference when comparing both AFB programming interfaces.

## redpesk integration

The project includes RPM packaging, an application manifest and redtest support so that the same sample can be used from local development through package deployment and validation on redpesk.

For platform-level topics such as creating a redpesk project, building applications and managing targets, refer to the [redpesk developer getting started guide](https://docs.redpesk.bzh/docs/en/master/getting_started/quickstart/02-overview-developer.html).
