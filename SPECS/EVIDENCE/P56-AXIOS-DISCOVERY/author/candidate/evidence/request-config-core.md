# Request config

The request config is used to configure the request. There is a wide range of options available, but the only required option is `url`. If the configuration object does not contain a `method` field, the default method is `GET`.

::: warning Security: decompression-bomb protection is opt-in
By default `maxContentLength` and `maxBodyLength` are `-1` (unlimited). A malicious or compromised server can return a tiny gzip/deflate/brotli/zstd body that expands to gigabytes and exhaust the Node.js process.

If you call servers you do not fully trust, **set a cap**:

```js
axios.defaults.maxContentLength = 10 * 1024 * 1024; // 10 MB
axios.defaults.maxBodyLength = 10 * 1024 * 1024;
```

See the [security guide](/pages/misc/security) for details.
:::

### `url`

The `url` is the URL to which the request is made. It can be a string or an instance of `URL`.

### `method`

The `method` is the HTTP method to use for the request. The default method is `GET`.

### `baseURL`

The `baseURL` is the base URL to be prepended to the `url` unless the `url` is an absolute URL. This is useful for making requests to the same domain without having to repeat the domain name and any api or version prefix.

`baseURL` is a URL-construction convenience, not a security boundary. If a request `url` comes from untrusted input, validate it before passing it to axios. A relative `url` can contain `..` segments; after axios combines it with `baseURL`, the platform URL parser normalizes the path and may resolve the request outside the intended path prefix. `allowAbsoluteUrls: false` prevents absolute URLs from replacing `baseURL`, but it does not validate or constrain relative paths.

### `allowAbsoluteUrls`

The `allowAbsoluteUrls` determines whether or not absolute URLs will override a configured `baseUrl`. When set to true (default), absolute values for `url` will override `baseUrl`. When set to false, absolute values for `url` will always be prepended by `baseUrl`.

### `transformRequest`

The `transformRequest` function allows you to modify the request data before it is sent to the server. This function is called with the request data as its only argument. This is only applicable for request methods `PUT`, `POST`, `PATCH` and `DELETE`. The last function in the array must return a string or an instance of Buffer, ArrayBuffer, FormData or Stream.
