# API Reference

## API

The binding exposes the following AFB API:

```text
helloworld
```

It provides three verbs: `hello`, `sum` and `info`.

For the AFB V4 API model, verb declaration and request handling concepts used by this sample, see the [AFB Binding V4 tutorial](https://docs.redpesk.bzh/docs/en/master/developer-guides/afb-binding-tutorial-v4.html).

## `hello`

Returns a greeting.

### Request hello

The first argument is optional. When it can be converted to a string, it is used as the name in the reply.

Without an argument:

```bash
afb-client -H localhost:1234/api helloworld hello
```

With an argument:

```bash
afb-client -H localhost:1234/api helloworld hello Bob
```

### Reply hello

Without an argument:

```text
Hello world!
```

With `Bob` as the first argument:

```text
Hello Bob!
```

### Event hello

Each call publishes `helloworld/verb_called` with `hello` as payload.

## `sum`

Computes the sum of a JSON array of integers.

### Request sum

Exactly one argument is expected. It must be a JSON array containing only integers.

Example:

```bash
afb-client -H localhost:1234/api helloworld sum '[1,2,3,4]'
```

### Reply sum

The reply is a signed 64-bit integer containing the sum of all array elements.

For the previous example, the result is:

```text
10
```

An empty array returns `0`.

### Error sum

If the request does not contain exactly one parameter, if the parameter is not a JSON array, or if one of its elements is not an integer, the request fails with:

```text
parameter should be a JSON array of integers
```

### Event sum

Each successful or rejected call publishes `helloworld/verb_called` with `sum` as payload before the request parameters are validated.

## `info`

Returns the static metadata describing the sample API and its verbs.

### Request info

No argument is required:

```bash
afb-client -H localhost:1234/api helloworld info
```

### Reply info

The reply is a JSON object containing the binding metadata and the descriptions of the `hello`, `sum` and `info` verbs.

## Event reference

### `helloworld/verb_called`

The `verb_called` event demonstrates AFB event publication and client subscription.

| Property | Value |
| --- | --- |
| Event name | `helloworld/verb_called` |
| Payload type | string |
| Payload | name of the called verb |
| Emitted by | `hello`, `sum` |
| Subscription | automatic, per client |

The client context records whether the client has already been subscribed, preventing repeated subscription setup on subsequent requests.
