Most APIs require some form of authentication. This page covers the most common patterns for attaching credentials to axios requests.

## Bearer tokens (JWT)

The most common approach is to attach a JWT in the `Authorization` header. The cleanest way to do this is via a request interceptor on your axios instance, so the token is read fresh on every request:

```js
import axios from "axios";

const api = axios.create({ baseURL: "https://api.example.com" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});
```

## HTTP Basic auth

For APIs that use HTTP Basic authentication, pass the `auth` option. axios will encode the credentials and set the `Authorization` header automatically:

```js
const response = await axios.get("https://api.example.com/data", {
  auth: {
    username: "myUser",
    password: "myPassword",
  },
});
```

If `auth` is not supplied, the Node.js HTTP and fetch adapters can also derive Basic auth credentials from the request URL, for example `https://myUser:myPassword@api.example.com/data`. Percent-encoded URL credentials are decoded before the `Authorization` header is generated. Prefer the explicit `auth` option for new code; it takes precedence over URL-embedded credentials.

::: tip
For Bearer tokens and API keys, use a custom `Authorization` header rather than the `auth` option — `auth` is only for HTTP Basic.
:::

## API keys

API keys are typically passed as a header or a query parameter, depending on what the API expects:

```js
// As a header
const api = axios.create({
  baseURL: "https://api.example.com",
  headers: { "X-API-Key": "your-api-key-here" },
});

// As a query parameter
const response = await axios.get("https://api.example.com/data", {
  params: { apiKey: "your-api-key-here" },
});
```
