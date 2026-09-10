# Retry and error recovery

Network requests can fail for transient reasons — a server blip, a brief network drop, or a rate-limit response. Implementing a retry strategy in an interceptor lets you handle these failures transparently, without cluttering your application code.

## Basic retry with a response interceptor

The simplest approach is to catch specific error status codes and immediately re-send the original request a limited number of times:

```js
import axios from "axios";

const api = axios.create({ baseURL: "https://api.example.com" });

const MAX_RETRIES = 3;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;

    // Only retry on network errors or 5xx server errors
    const shouldRetry =
      !error.response || (error.response.status >= 500 && error.response.status < 600);

    if (!shouldRetry) {
      return Promise.reject(error);
    }

    config._retryCount = config._retryCount ?? 0;

    if (config._retryCount >= MAX_RETRIES) {
      return Promise.reject(error);
    }

    config._retryCount += 1;
    return api(config);
  }
);
```
