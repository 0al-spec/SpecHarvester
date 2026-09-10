# HTTP2 <Badge type="warning" text="Experimental" /> <Badge type="tip" text="v1.13.0+" />

Experimental HTTP/2 support was added to the `http` adapter in version `1.13.0`. It is available in Node.js environments only.

## Basic usage

Use the `httpVersion` option to select the protocol version for a request. Setting it to `2` enables HTTP/2.

```js
const { data, headers, status } = await axios.post(
  "https://httpbin.org/post",
  form,
  {
    httpVersion: 2,
  },
);
```

## `http2Options`

Additional native options for the internal `session.request()` call can be passed via the `http2Options` config object. This also includes the custom `sessionTimeout` parameter, which controls how long (in milliseconds) an idle HTTP/2 session is kept alive before being closed. It defaults to `1000ms`.

```js
{
  httpVersion: 2,
  http2Options: {
    rejectUnauthorized: false, // accept self-signed certificates (dev only)
    sessionTimeout: 5000,      // keep idle session alive for 5 seconds
  },
}
```

::: warning
HTTP/2 support is currently experimental. The API may change in future minor or patch releases.
:::

::: warning Redirects are not supported over HTTP/2
The HTTP/2 adapter does not currently follow redirects. If a request issued with `httpVersion: 2` receives a `3xx` response, the redirect is not followed automatically. Handle these responses manually or stay on HTTP/1.x for endpoints that rely on redirects.
