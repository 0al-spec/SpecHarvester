# Cancellation

Starting from v0.22.0 Axios supports AbortController to cancel requests in a clean way. This feature is available in the browser and in Node.js when using a version of Axios that supports AbortController. To cancel a request, you need to create an instance of `AbortController` and pass its `signal` to the request's `signal` option.

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

## CancelToken <Badge type="danger" text="Deprecated" />

You can also use the `CancelToken` API to cancel requests. This API is deprecated and will be removed in the next major release. It is recommended to use `AbortController` instead. You can create a cancel token using the `CancelToken.source` factory as shown below:
