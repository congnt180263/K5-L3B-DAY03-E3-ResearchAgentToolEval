---
name: dedupe_sources
track: core
kind: local_formatter
provider: null
requires_env: []
inputs: [items]
outputs: [tool, items, duplicate_count, error, message]
side_effect: false
---
# dedupe_sources

Use this tool when you already have research results and want one entry per URL
before making a digest or a citation list. Use search or fetch tools first if the
user still needs sources or page content.

- `items` is a list of JSON objects. Each object must contain a string `url`
  with an absolute HTTP(S) URL. The tool keeps the first object for each URL,
  including its original URL and metadata. The order of retained items follows
  the input. An empty list returns an empty list and zero duplicates.
- For comparison, the tool trims surrounding whitespace, normalizes host case
  and default ports, treats an empty path as `/`, and ignores fragments. It
  preserves scheme, path case and query values/order. It does not resolve
  redirects, remove tracking parameters or compare article text.
- Invalid input returns an error object with `tool`, `error` and `message`
  instead of a partial list. The tool makes no network requests or file writes.
  Fragment-based pages on the same URL will be treated as one source.

Input

```json
{"items":[{"title":"AI report","url":"https://Example.com/report#summary"},{"title":"Same report","url":"https://example.com:443/report"}]}
```

Output

```json
{"tool":"dedupe_sources","items":[{"title":"AI report","url":"https://Example.com/report#summary"}],"duplicate_count":1}
```
