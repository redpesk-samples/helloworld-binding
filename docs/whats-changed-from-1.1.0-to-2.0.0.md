# List of changes between helloworld-binding 1.1.0 and 2.0.0

## TODO

- update helloworld-binding documentation
- update presentation materials which use helloworld-binding

## Removed

- tests
- HTML application
- `.gitreview` file
- every single mention of a widget
- AGL autobuild
- Debian packaging
- documentation from before 1.1.0

## Changed

- single `CMakeLists.txt` file
  - standalone: no AFM macros, no `conf.d/cmake/config.cmake`
  - but still less than 40 lines
- packaging
  - removed v3 dependencies
  - removed AFM macros

### The binding itself

- use v4 framework instead of v3
- single binding instead of two components

#### Showcased AF features

In both: logging, request reply, parameter handling, events

Differences:

| helloworld v3       | helloworld v4        |
| ------------------- | -------------------- |
| JSON object parsing | JSON array iteration |
| JSON creation       |                      |
| timers              |                      |
|                     | client context       |
|                     | mainctl              |
|                     | C++ wrapper          |

#### Verbs implemented

v3, first binding:

- `pingSample`: increments a counter at each call, replies with the counter value
- `testArgsSample`: requires a specific key/value in a JSON object to deliver a value (sésame, ouvre-toi)
- `infoSample`: kind of a `--help` but it's a dynamically constructed JSON

v3, second binding:

- `startTimer`: pushes an event every second
- `subscribe`: subscribes to the event pushed by `startTimer`
- `unsubscribe`: unsubscribes to the event pushed by `startTimer`
- `info`: same as `infoSample`

v4: all requests emit an event with the called verb name as data (all clients are automatically subscribed to this event)

- `hello`: replies `Hello world!` or `Hello <param>!` if param was specified
- `sum`: returns the sum of all integers supplied in a JSON array
