# Response schema

Every axios request resolves to a response object with the following shape. The schema is consistent across both browser and Node.js environments.

```js
{
  // The response data provided by the server.
  // When using `transformResponse`, this will be the result of the last transform.
  data: {},

  // The HTTP status code from the server response (e.g. 200, 404, 500).
  status: 200,

  // The HTTP status message matching the status code (e.g. "OK", "Not Found").
  statusText: "OK",

  // The response headers sent by the server.
  // Header names are lower-cased. You can access them using bracket or dot notation.
  headers: {},

  // The axios config that was used for this request, including baseURL,
  // headers, timeout, params, and any other options you provided.
  config: {},

  // The underlying request object.
  // In Node.js: the last `http.ClientRequest` instance (after any redirects).
  // In the browser: the `XMLHttpRequest` instance.
  request: {},
}
