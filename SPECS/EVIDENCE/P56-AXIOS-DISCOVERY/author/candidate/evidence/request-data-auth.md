### `headers`

The `headers` are the HTTP headers to be sent with the request. The `Content-Type` header is set to `application/json` by default.

### `params`

The `params` are the URL parameters to be sent with the request. This must be a plain object or a URLSearchParams object. If the `url` contains query parameters, they will be merged with the `params` object.

### `paramsSerializer`

The `paramsSerializer` function allows you to serialize the `params` object before it is sent to the server. There are a few options available for this function, so please refer to the full request config example at the end of this page.

#### Strict RFC 3986 percent-encoding

By default, axios decodes `%3A`, `%24`, `%2C` and `%20` back to `:`, `$`, `,` and `+` for readability (the `+` follows the `application/x-www-form-urlencoded` convention for spaces in query strings). These characters are valid in a query component under [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986#section-3.4), so the default output is correct. However, some backends require strict percent-encoding and reject the readable form.

Use the `encode` option to override the default encoder:

```js
// Per-request: emit strict RFC 3986 percent-encoding for query values
axios.get('/foo', {
  params: { filter: JSON.stringify({ startedAt: '2026-01-23' }) },
  paramsSerializer: { encode: encodeURIComponent },
});

// Or set it on the instance defaults
const client = axios.create({
  paramsSerializer: { encode: encodeURIComponent },
});
```

### `data`

The `data` is the data to be sent as the request body. This can be a string, a plain object, a Buffer, ArrayBuffer, FormData, Stream, or URLSearchParams. Only applicable for request methods `PUT`, `POST`, `DELETE` , and `PATCH`. When no `transformRequest` is set, must be of one of the following types:

- string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
- Browser only: FormData, File, Blob
- React Native: FormData
- Node only: Stream, Buffer, FormData (form-data package)

For browser, web worker, and React Native `FormData`, do not manually set `Content-Type`; the runtime adds the multipart boundary.

For Node.js `FormData` objects that provide a `getHeaders()` method, axios copies all returned headers by default for v1 compatibility. If the `FormData` object is custom or not fully trusted, set `formDataHeaderPolicy: 'content-only'` to copy only `Content-Type` and `Content-Length`, and set any other request headers explicitly via the request `headers` config.

### `formDataHeaderPolicy` <Badge type="warning" text="Node.js only" />

Controls how axios copies headers returned by Node.js `FormData#getHeaders()`. The default is `'legacy'`, which copies all returned headers to preserve existing v1 behavior. Set `'content-only'` to copy only `Content-Type` and `Content-Length` from `getHeaders()`.

### `timeout`

The `timeout` is the number of milliseconds before the request times out. If the request takes longer than `timeout`, the request will be aborted.

### `withCredentials`

The `withCredentials` property indicates whether or not cross-site Access-Control requests should be made using credentials such as cookies, authorization headers, or TLS client certificates. Setting withCredentials has no effect on same-site requests.

### `adapter`

`adapter` allows custom handling of requests which makes testing easier. Return a promise and supply a valid response see [adapters](/pages/advanced/adapters) for more information. We also provide a number of built-in adapters. The default adapter is `http` for node and `xhr` for browsers. The full list of built-in adapters as follows:

- fetch
- http
- xhr

You may also pass an array of adapters to be used, axios will use the first adapter that is supported by the environment.

### `auth`

`auth` indicates that HTTP Basic auth should be used, and supplies credentials. This will set an `Authorization` header, overwriting any existing `Authorization` custom headers you have set using `headers`. If `auth` is omitted, the Node.js HTTP and fetch adapters can derive Basic auth credentials from the request URL, for example `https://user:pass@example.com`; percent-encoded URL credentials are decoded, and `auth` always takes precedence over URL-embedded credentials. In the Node.js HTTP adapter, Basic auth is preserved on same-origin redirects and stripped on cross-origin redirects. Please note that only HTTP Basic auth is configurable through this parameter. For Bearer tokens and such, use `Authorization` custom headers instead.

### `responseType`

The `responseType` indicates the type of data that the server will respond with. This can be one of the following:

- arraybuffer
- document
- json
- text
- stream
- blob (browser only)
- formdata (fetch adapter only)

