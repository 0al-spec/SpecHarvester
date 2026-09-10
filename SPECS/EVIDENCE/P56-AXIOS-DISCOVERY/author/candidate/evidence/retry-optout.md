## Opting out of retries per request

If some requests should never be retried (e.g. non-idempotent mutations you don't want to duplicate), add a flag to the request config:

```js
// Add this to your interceptor before the retry logic:
if (config._noRetry) return Promise.reject(error);

// Then opt out on specific calls:
await api.post("/payments/charge", body, { _noRetry: true });
```

## Combining retry with cancellation

Use an `AbortController` to cancel a request that is waiting for a backoff delay:
