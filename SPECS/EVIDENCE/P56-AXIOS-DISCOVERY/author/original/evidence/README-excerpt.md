## Features

- Make [XMLHttpRequests](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) from the browser.
- Make [http](https://nodejs.org/api/http.html) requests from Node.js.
- Use the [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) API for asynchronous request handling.
- Intercept requests and responses to add custom logic or transform data.
- Transform request and response data.
- Cancel requests with built-in cancellation APIs.
- Serialize and parse [JSON](https://www.json.org/json-en.html) data.
- Serialize data objects to `multipart/form-data` or `application/x-www-form-urlencoded`.
- Add client-side protection against [Cross-Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery).

## Browser support

|                                                     Chrome                                                     |                                                      Firefox                                                      |                                                     Safari                                                     |                                                    Opera                                                    |                                                   Edge                                                   |
## Example

```js
import axios from 'axios';
//const axios = require('axios'); // legacy way

try {
  const response = await axios.get('/user?ID=12345');
  console.log(response);
} catch (error) {
  console.error(error);
}

// Optionally the request above could also be done as
axios
  .get('/user', {
    params: {
      ID: 12345,
    },
    timeout: 5000, // 5 seconds. See "Handling Timeouts" below for matching error handling
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });

// Want to use async/await? Add the `async` keyword to your outer function/method.
async function getUser() {
  try {
    // Example: GET request with query parameters
    const response = await axios.get('/user', {
      params: {
        ID: 12345,
      },
    });

    // Using the `params` option improves readability and automatically formats query strings

##### axios.request(config)

##### axios.get(url[, config])

##### axios.delete(url[, config])

##### axios.head(url[, config])

##### axios.options(url[, config])

##### axios.post(url[, data[, config]])

##### axios.put(url[, data[, config]])

##### axios.patch(url[, data[, config]])

###### Note

When using the alias methods `url`, `method`, and `data` properties don't need to be specified in config.

### Concurrency (deprecated)

Use `Promise.all` instead of these helpers.

Helper functions for dealing with concurrent requests.

axios.all(iterable)
axios.spread(callback)

### Creating an instance

You can create a new instance of axios with a custom config.

##### axios.create([config])

```js
const instance = axios.create({
  baseURL: 'https://some-domain.com/api/',
  timeout: 1000,
  headers: { 'X-Custom-Header': 'foobar' },
});
```

### Instance methods

The following instance methods are available. Axios merges the specified config with the instance config.

##### axios#request(config)

##### axios#get(url[, config])

##### axios#delete(url[, config])

##### axios#head(url[, config])

##### axios#options(url[, config])

##### axios#post(url[, data[, config]])

##### axios#put(url[, data[, config]])

##### axios#patch(url[, data[, config]])

##### axios#getUri([config])

## Request config

### Security notice: decompression-bomb protection is opt-in

By default `maxContentLength` and `maxBodyLength` are `-1` (unlimited). A malicious or compromised server can return a tiny gzip/deflate/brotli/zstd body that expands to gigabytes and exhaust the Node.js process.

If you call servers you do not fully trust, **set a cap**:

```js
axios.defaults.maxContentLength = 10 * 1024 * 1024; // 10 MB
axios.defaults.maxBodyLength = 10 * 1024 * 1024;
```

See the [security guide](https://axios.rest/pages/misc/security.html) for details.

These config options are available for requests. Only `url` is required. Requests default to `GET` when `method` is not set.

```js
{
  // `url` is the server URL for the request
  url: '/user',

  // `method` is the request method to be used when making the request
  method: 'get', // default

  // Axios prepends `baseURL` to `url` unless `url` is absolute and `allowAbsoluteUrls` is set to true.
## Response schema

The response to a request contains the following information.

```js
{
  // `data` is the response that was provided by the server
  data: {},

  // `status` is the HTTP status code from the server response
  status: 200,

  // `statusText` is the HTTP status message from the server response
  statusText: 'OK',

  // `headers` the HTTP headers that the server responded with
  // All header names are lowercase and can be accessed using the bracket notation.
  // Example: `response.headers['content-type']`
  headers: {},

  // `config` is the config that was provided to `axios` for the request
  config: {},

  // `request` is the request that generated this response
  // It is the last ClientRequest instance in node.js (in redirects)
  // and an XMLHttpRequest instance in the browser
  request: {}
}
```

When using `then`, you receive the response like this:

```js
const response = await axios.get('/user/12345');
console.log(response.data);
console.log(response.status);
console.log(response.statusText);
console.log(response.headers);
console.log(response.config);
```

When using `catch`, or passing a [rejection callback](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then) as the second parameter of `then`, read the response from the `error` object. See [Handling errors](#handling-errors).

## Config defaults

Config defaults apply to every request.

### Global axios defaults

```js
axios.defaults.baseURL = 'https://api.example.com';
## Handling errors

By default, Axios rejects responses with status codes outside the 2xx range.

```js
axios.get('/user/12345').catch(function (error) {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.log(error.response.data);
    console.log(error.response.status);
    console.log(error.response.headers);
  } else if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    console.log(error.request);
  } else {
    // Something happened in setting up the request that triggered an Error
    console.log('Error', error.message);
  }
  console.log(error.config);
});
```

Use `validateStatus` to override the default condition (`status >= 200 && status < 300`) and choose which HTTP status codes should reject.

```js
axios.get('/user/12345', {
  validateStatus: function (status) {
    return status < 500; // Resolve only if the status code is less than 500
  },
});
```

By default, explicit `validateStatus: undefined` keeps legacy behavior and resolves every response status because `transitional.validateStatusUndefinedResolves` defaults to `true`. Set it to `false` to make explicit `validateStatus: undefined` behave like the option was omitted, so Axios uses the configured/default validator and rejects non-2xx responses by default.

`validateStatus: null` still accepts every response status. If you disable the transitional behavior and intentionally want all statuses to resolve, use `null` or `() => true`.

```js
axios.get('/user/12345', {
  validateStatus: undefined,
  transitional: {
    validateStatusUndefinedResolves: false,
  },
});
```

Use `toJSON` to get more information about the HTTP error.

```js
axios.get('/user/12345').catch(function (error) {
  console.log(error.toJSON());
});
```

To avoid logging secrets from `error.config`, pass a `redact` array in the request config. Matching config keys are masked case-insensitively at any depth when `AxiosError#toJSON()` is called.

```js
axios
  .get('/user/12345', {
    headers: { Authorization: 'Bearer token' },
    redact: ['authorization'],
  })
  .catch(function (error) {
    console.log(error.toJSON().config.headers.Authorization); // [REDACTED ****]
  });
```

## Handling timeouts

```js
async function fetchWithTimeout() {
  try {
    const response = await axios.get('https://example.com/data', {
      timeout: 5000, // 5 seconds
      transitional: {
        // set to true if you prefer ETIMEDOUT over ECONNABORTED
        clarifyTimeoutError: false,
      },
    });

    console.log('Response:', response.data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
        console.error('Request timed out. Please try again.');
        return;
      }

      console.error('Axios error:', error.message);
      return;
    }

    console.error('Unexpected error:', error);
  }
}
```

## Cancellation

### AbortController

Since `v0.22.0`, Axios supports AbortController:

```js
const controller = new AbortController();

axios
  .get('/foo/bar', {
    signal: controller.signal,
  })
  .then(function (response) {
    //...
  });
// cancel the request
controller.abort();
```

### CancelToken (deprecated)

You can also cancel a request using a _CancelToken_.

> The axios cancel token API is based on the withdrawn [cancellable promises proposal](https://github.com/tc39/proposal-cancelable-promises).

> This API is deprecated since v0.22.0 and should not be used in new projects.

Create a cancel token with the `CancelToken.source` factory:

```js
const CancelToken = axios.CancelToken;
const source = CancelToken.source();

axios
  .get('/user/12345', {
