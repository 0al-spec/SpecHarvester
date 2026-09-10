{
  "name": "axios",
  "version": "1.19.0",
  "description": "Promise based HTTP client for the browser and node.js",
  "main": "./dist/node/axios.cjs",
  "module": "./index.js",
  "type": "module",
  "types": "index.d.ts",
  "jsdelivr": "dist/axios.min.js",
  "unpkg": "dist/axios.min.js",
  "typings": "./index.d.ts",
  "exports": {
    ".": {
      "types": {
        "require": "./index.d.cts",
        "default": "./index.d.ts"
      },
      "bun": {
        "require": "./dist/node/axios.cjs",
        "default": "./index.js"
      }
    },
    "./lib/adapters/http.js": "./lib/adapters/http.js",
    "./lib/adapters/xhr.js": "./lib/adapters/xhr.js",
    "./unsafe/*": "./lib/*",
    "./unsafe/core/settle.js": "./lib/core/settle.js",
    "./unsafe/core/buildFullPath.js": "./lib/core/buildFullPath.js",
    "./unsafe/helpers/isAbsoluteURL.js": "./lib/helpers/isAbsoluteURL.js",
    "./unsafe/helpers/buildURL.js": "./lib/helpers/buildURL.js",
    "./unsafe/helpers/combineURLs.js": "./lib/helpers/combineURLs.js",
    "./unsafe/adapters/http.js": "./lib/adapters/http.js",
    "./unsafe/adapters/xhr.js": "./lib/adapters/xhr.js",
    "./unsafe/utils.js": "./lib/utils.js",
    "./lib/platform/node/classes/FormData.js": "./lib/helpers/null.js"
  },
  "react-native": {
    "./dist/node/axios.cjs": "./dist/browser/axios.cjs",
    "./lib/adapters/http.js": "./lib/helpers/null.js",
    "./lib/platform/node/index.js": "./lib/platform/browser/index.js",
    "./lib/platform/node/classes/Buffer.js": "./lib/helpers/null.js",
    "./lib/platform/node/classes/FormData.js": "./lib/helpers/null.js"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/axios/axios.git"
  },
  "keywords": [
    "xhr",
    "http",
    "ajax",
    "promise",
    "Willian Agostini (https://github.com/WillianAgostini)",
    "Rikki Gibson (https://github.com/RikkiGibson)"
  ],
  "sideEffects": false,
  "license": "MIT",
  "bugs": {
    "url": "https://github.com/axios/axios/issues"
  },
  "homepage": "https://axios-http.com",
  "files": [
    "index.js",
