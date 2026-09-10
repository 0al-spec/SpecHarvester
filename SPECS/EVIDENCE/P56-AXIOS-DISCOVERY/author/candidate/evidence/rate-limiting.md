# Rate limiting <Badge type="tip" text="New" />

axios supports bandwidth limiting in the Node.js environment via the HTTP adapter. This lets you cap how fast data is uploaded or downloaded, which is useful for bulk operations, background jobs, or polite scraping that shouldn't saturate a connection.

## `maxRate`

The `maxRate` option accepts either a number (bytes per second) or an array where the first value is the upload limit and the second value is the download limit. Use `[uploadRate]` to limit upload only, or `[uploadRate, downloadRate]` to limit both directions. When a single number is passed, the same limit applies to both upload and download.

```js
// Limit both upload and download to 100 KB/s
await axios.get(URL, { maxRate: 100 * 1024 });

// Limit upload to 100 KB/s, download to 500 KB/s
await axios.get(URL, { maxRate: [100 * 1024, 500 * 1024] });
```

::: warning
`maxRate` is only supported by the Node.js HTTP adapter. It has no effect in browser environments.
:::
