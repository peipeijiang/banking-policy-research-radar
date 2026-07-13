# One-click WeCom feedback

This Cloudflare Worker turns signed WeCom links into one-click paper feedback.
Opening a link renders a small confirmation page that automatically sends a
POST request. Link-preview crawlers only perform GET requests and therefore do
not create feedback by themselves.

## Deploy

1. Copy `wrangler.toml.example` to `wrangler.toml`.
2. Run `npx wrangler login` and `npx wrangler deploy`.
3. Configure Worker secrets:

```bash
npx wrangler secret put GITHUB_TOKEN
npx wrangler secret put FEEDBACK_SIGNING_SECRET
```

`GITHUB_TOKEN` should be a fine-grained token limited to this repository with
Issues read/write permission. Generate a long random signing secret, for
example with `openssl rand -hex 32`.

4. Add the following GitHub Actions repository secrets:

- `FEEDBACK_API_URL`: the deployed `https://...workers.dev` URL
- `FEEDBACK_SIGNING_SECRET`: exactly the same signing secret used by Worker

When both values are present, new WeCom cards use the one-click endpoint.
Without them, notification links continue to open GitHub's prefilled Issue
form as a safe fallback.
