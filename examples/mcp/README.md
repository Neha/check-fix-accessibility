# Optional a11y-mcp examples

These files are **not** loaded by any assistant. Copy a snippet into the config path in the main README only after you accept that `https://a11y-mcp.withjavascript.com` is a third-party host.

- `cursor.mcp.json` — also the shape for Claude Code (`.mcp.json`) and Kiro (`.kiro/settings/mcp.json`).
- `antigravity.mcp_config.json` — Antigravity uses `serverUrl`.

Codex reads TOML (`~/.codex/config.toml`) and its `url` field is Streamable HTTP, not this legacy SSE path. There is no Codex snippet here on purpose.
