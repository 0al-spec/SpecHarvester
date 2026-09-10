# Axios discovery depth: до и после

## Краткий итог

Original candidate уже правильно отвечал на базовый вопрос: Axios — Promise-based HTTP client для browser и Node.js с request aliases, configured instances, response/error model, timeout, AbortController и body limits. Проблема не в полной пустоте, а в низкой различимости: три крупные capability сворачивали несколько важных consumer outcomes, а outbound HTTP interaction был указан только как `network_read`.

Alternate preview сохраняет тот же package id `axios.http_client`, версию `1.19.0`, `preview_only: true` и draft status. Он не доказывает улучшение поиска, runtime behavior или готовность к публикации. Его практическая ценность ограничена тем, что natural-language discovery и сравнение теперь могут опираться на более точные, source-backed различия.

## Что изменилось

**Уже было покрыто и лишь лучше организовано:**

- Request API и aliases, `axios.create`, Promise response и error branches.
- Timeout, `AbortController`, deprecated `CancelToken`, `validateStatus`, `maxContentLength` и `maxBodyLength`.
- Transform, multipart, URL-encoded, XSRF, progress, `maxRate`, adapter и HTTP/2 keywords/fields частично уже находились в README/type evidence. Поэтому они не названы полностью отсутствовавшими.

**Новое structured coverage:**

- Serialization выделена как outcome: JSON, query params, URL-encoded и automatic FormData, включая browser boundary handling, Node `formDataHeaderPolicy` и nesting limit.
- Authentication/XSRF описаны по режимам и условиям: Basic auth, custom Authorization/API-key headers, cookies, `withCredentials` и `withXSRFToken`.
- Interceptors получили lifecycle semantics: instance isolation, `runWhen`, synchronous option, eject/clear, request LIFO и response FIFO.
- Progress и bandwidth control разделены по ограничениям: три события в секунду, отсутствие Node FormData upload progress, риск buffering при redirects, `maxRate` только для Node HTTP adapter.
- Transport choice теперь различает XHR, HTTP, fetch, fallback order, custom adapter и experimental Node HTTP/2 без automatic redirects.

Самое существенное semantic исправление — data flow. Было: `network_read: A request causes an outbound HTTP interaction and receives a remote response`. Стало: отдельный `network_write` перечисляет destination, query, headers, credentials/tokens и body; второй `network_write` квалифицирует mutation-capable methods; `network_read` отдельно описывает status, headers и response data. Успех remote mutation, storage и retention не заявлены.

## Какие вопросы теперь разрешимы

- «Подойдет ли клиент для ограничения скорости больших upload/download в browser?» — нет: `maxRate` документирован только для Node.js HTTP adapter.
- «Можно ли включить HTTP/2 и сохранить automatic redirects?» — HTTP/2 experimental, Node-only, redirects не follow автоматически.
- «Как передаются Basic, Bearer, cookies и XSRF при cross-origin?» — режимы и независимые config conditions перечислены, а disclosure отражен как outbound effect.
- «Есть ли встроенный retry/backoff/cache?» — retry examples являются application interceptors; retry/cache policy исключена, а cache behavior в bounded review не установлено.
- «Можно ли безопасно считать `baseURL` origin boundary?» — нет; docs прямо требуют валидировать untrusted URL input.

## Диагноз и пределы

Наблюдаемая потеря информации подтверждается самим original evidence: transform/FormData/XSRF перечислены в README excerpt, а `maxRate`, adapter, `fetchOptions`, `httpVersion` и `http2Options` присутствуют в type excerpt, но не становятся самостоятельными сравнимыми outcomes. Original source notes также честно признают, что adapter selection и все config fields не были установлены. Это совместимо с недостаточно глубоким bounded investigation, но hidden reasoning автора недоступен, поэтому причина не приписывается модели.

Эксперимент не запускал Axios, tests, builds, examples, endpoints или search engine. Он не устанавливает cache semantics, custom-adapter effects, remote retention, exhaustive proxy/redirect behavior или полный browser/runtime matrix.
