## Automatic serialization to FormData <Badge type="tip" text="New" />

Starting from v0.27.0, Axios supports automatic object serialization to a FormData object if the request Content-Type header is set to multipart/form-data. This means that you can pass a JavaScript object directly to the data property of the axios request config. For example when passing data to a POST request:

```js
import axios from 'axios';

axios
  .post(
    'https://httpbin.org/post',
    { x: 1 },
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  )
  .then(({ data }) => console.log(data));
```

In the node.js build, the ([`form-data`](https://github.com/form-data/form-data)) polyfill is used by default. You can overload the FormData class by setting the env.FormData config variable, but you probably won't need it in most cases:

```js
const axios = require('axios');
var FormData = require('form-data');

axios
  .post(
    'https://httpbin.org/post',
    { x: 1, buf: Buffer.alloc(10) },
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  )
  .then(({ data }) => console.log(data));
```

## Header policy for Node.js `FormData` <Badge type="warning" text="Node.js only" />

When you pass a Node.js `FormData` object that exposes `getHeaders()` (such as the [`form-data`](https://github.com/form-data/form-data) package), axios copies all headers it returns onto the request by default. This preserves v1 compatibility but can be problematic when the `FormData` object comes from an untrusted source — `getHeaders()` could overwrite headers like `Authorization` or inject arbitrary ones.

Set `formDataHeaderPolicy: 'content-only'` to copy **only** `Content-Type` and `Content-Length` from `getHeaders()`, then set any other headers explicitly via the request `headers` config:

```js
await axios.post('https://example.com/upload', form, {
  formDataHeaderPolicy: 'content-only',
  headers: {
    Authorization: 'Bearer my-token',
  },
});
```

The default value is `'legacy'`. See [`formDataHeaderPolicy`](/pages/advanced/request-config#formdataheaderpolicy) in the request config reference for details.

## Supported endings

Axios FormData serializer supports some special endings to perform the following operations:

- `{}` - serialize the value with JSON.stringify
- `[]` - unwrap the array-like object as separate fields with the same key

::: warning
Note: unwrap/expand operation will be used by default on arrays and FileList objects
:::

## Configuring the FormData serializer

FormData serializer supports additional options via config.formSerializer: object property to handle rare cases:

- `visitor: Function` - user-defined visitor function that will be called recursively to serialize the data object to a FormData object by following custom rules.
- `dots: boolean = false` - use dot notation instead of brackets to serialize arrays and objects;
- `metaTokens: boolean = true` - add the special ending (e.g `user{}: '{"name": "John"}'`) in the FormData key. The back-end body-parser could potentially use this meta-information to automatically parse the value as JSON.
- `indexes: null|false|true = false` - controls how indexes will be added to unwrapped keys of flat array-like objects
  - `null` - don't add brackets (`arr: 1`, `arr: 2`, `arr: 3`)
  - `false` (default) - add empty brackets (`arr[]: 1`, `arr[]: 2`, `arr[]: 3`)
  - `true` - add brackets with indexes (`arr[0]: 1`, `arr[1]: 2`, `arr[2]: 3`)
- `maxDepth: number = 100` - maximum object nesting depth the serializer will recurse into. If the input exceeds this depth, an `AxiosError` with `code: 'ERR_FORM_DATA_DEPTH_EXCEEDED'` is thrown. This protects server-side applications from DoS attacks via deeply nested payloads. Set to `Infinity` to disable the limit.
- `Blob: typeof Blob` - Blob constructor used when converting ArrayBuffer-like values for spec-compliant `FormData`. Override it only for runtimes that provide a compatible `Blob` constructor under a different binding.

```js
// Allow deeper nesting for schemas that legitimately exceed 100 levels:
axios.postForm('/api', data, { formSerializer: { maxDepth: 200 } });
```

::: warning Security note
The default limit of 100 is intentional. Server-side code that forwards client-controlled JSON to axios as `data` is vulnerable to a call-stack overflow without this guard. Only raise `maxDepth` if your schema genuinely requires it.
