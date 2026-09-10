      // HTTP basic authentication
      let auth = undefined;
      const configAuth = own('auth');
      if (configAuth) {
        const username = utils.getSafeProp(configAuth, 'username') || '';
        const password = utils.getSafeProp(configAuth, 'password') || '';
        auth = username + ':' + password;
      }

      if (!auth && (parsed.username || parsed.password)) {
        const urlUsername = decodeURIComponentSafe(parsed.username);
        const urlPassword = decodeURIComponentSafe(parsed.password);
        auth = urlUsername + ':' + urlPassword;
      }

      auth && headers.delete('authorization');

      let path;

      try {
        path = buildURL(
          parsed.pathname + parsed.search,
          own('params'),
          own('paramsSerializer')
        ).replace(/^\?/, '');
      } catch (err) {
        return reject(
          AxiosError.from(err, AxiosError.ERR_BAD_REQUEST, config, null, null, {
            url: own('url'),
            exists: true
          })
        );
      }

      headers.set(
        'Accept-Encoding',
        utils.hasOwnProp(transitional, 'advertiseZstdAcceptEncoding') &&
        transitional.advertiseZstdAcceptEncoding === true ? ACCEPT_ENCODING_WITH_ZSTD : ACCEPT_ENCODING,
        false
      );

      // Null-prototype to block prototype pollution gadgets on properties read
      // directly by Node's http.request (e.g. insecureHTTPParser, lookup).
      const options = Object.assign(Object.create(null), {
        path,
        method: method,
        headers: toByteStringHeaderObject(headers),
        agents: { http: httpAgent, https: httpsAgent },
        auth,
        protocol,
        family,
        beforeRedirect: dispatchBeforeRedirect,
        beforeRedirects: Object.create(null),
        http2Options,
      });
