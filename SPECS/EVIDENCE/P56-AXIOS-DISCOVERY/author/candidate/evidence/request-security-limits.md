### `xsrfCookieName`

The `xsrfCookieName` is the name of the cookie to use as a value for `XSRF` token.

### `xsrfHeaderName`

The `xsrfHeaderName` is the name of the header to use as a value for `XSRF` token.

### `withXSRFToken`

`withXSRFToken` controls whether axios reads the XSRF cookie and sets the XSRF header on browser requests. It accepts:

- `undefined` _(default)_ — set the XSRF header only for same-origin requests.
- `true` — always set the XSRF header, including for cross-origin requests.
- `false` — never set the XSRF header.
- `(config: InternalAxiosRequestConfig) => boolean | undefined` — a callback that decides per-request, receiving the internal config object.

```ts
withXSRFToken: boolean | undefined | ((config: InternalAxiosRequestConfig) => boolean | undefined);
```

::: warning Cross-origin XSRF and `withCredentials`
`withCredentials` controls whether cross-site requests include credentials (cookies, HTTP auth). `withXSRFToken` controls whether axios sets the XSRF header. For cross-origin requests, set `withXSRFToken: true` to force the header; additionally set `withCredentials: true` only when the request also needs credentials/cookies.

```js
axios.get('/user', { withCredentials: true, withXSRFToken: true });
```

:::

### `onUploadProgress`

The `onUploadProgress` function allows you to listen to the progress of an upload.

### `onDownloadProgress`

The `onDownloadProgress` function allows you to listen to the progress of a download.

### `maxContentLength` <Badge type="warning" text="Node.js HTTP/fetch adapter" />

The `maxContentLength` property defines the maximum response size in bytes. The Node.js HTTP adapter enforces it for buffered and streamed responses. The fetch adapter enforces it when the response length is declared, the response stream can be tracked, or the response size can otherwise be determined.

> ⚠️ **Security:** defaults to `-1` (unlimited). Unbounded responses combined with gzip/deflate/brotli/zstd decompression allow decompression-bomb DoS.
> Set an explicit limit when requesting servers you do not fully trust.

### `maxBodyLength` <Badge type="warning" text="Node.js HTTP/fetch adapter" />

The `maxBodyLength` property defines the maximum request body size in bytes. The Node.js HTTP adapter enforces it, and the fetch adapter enforces it when the request body length can be determined.

### `redact`

The `redact` property is an optional array of config key names to mask when an `AxiosError` is serialized with `toJSON()`. Matching is case-insensitive and recursive across the serialized request config. Matching values are replaced with `[REDACTED ****]`.

`redact` only affects error serialization. It does not change request data, headers, or the original config object.
