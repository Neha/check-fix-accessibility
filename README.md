# Check and Fix Accessibility (a11y) Skill

A reusable **accessibility (a11y) skill** for AI coding assistants. It teaches the agent how to audit and fix front-end accessibility issues (WCAG 2.2 Level A/AA), including semantics, keyboard navigation, ARIA, forms, contrast, and screen readers—for web (React, Next.js, Vue, Angular) and with pointers for native mobile.

**Skill version 1.8.0** · standard WCAG 2.2 Level A and AA · last reviewed 2026-10-01. The changelog is in [`check-fix-accessibility/SKILL.md`](check-fix-accessibility/SKILL.md#changelog). Pinned tool versions are recorded in the skill; check for newer releases before you adopt them.

Use this skill when you or your team work on accessibility, a11y, WCAG, screen readers, keyboard navigation, focus management, ARIA, semantic HTML, or fixing accessibility issues in HTML/React/Next.js/Vue or other front-end code.

![Check and Fix Accessibility — AI skill for auditing and fixing a11y issues](assets/social-card-dark.png)

---

## Quick start

You can install with the [skills CLI](https://github.com/vercel-labs/skills), which asks which agent to target. Project scope is the usual choice for a team:

```bash
npx skills add Neha/check-fix-accessibility
```

Or install by hand:

1. **Clone this repo** (replace `YOUR_USERNAME` with the GitHub org or user):

   ```bash
   git clone https://github.com/YOUR_USERNAME/check-fix-accessibility.git
   cd check-fix-accessibility
   ```

2. **Copy the `check-fix-accessibility` folder** into your assistant’s skills directory (pick your tool):

   | Assistant | Project (this repo only) | Global (all projects) |
   |-----------|--------------------------|------------------------|
   | **Cursor** | `.cursor/skills/check-fix-accessibility/` | `~/.cursor/skills/check-fix-accessibility/` |
   | **Claude Code** | `.claude/skills/check-fix-accessibility/` or `.claude/rules/` | `~/.claude/skills/check-fix-accessibility/` |
   | **Kiro** | `.kiro/skills/check-fix-accessibility/` | `~/.kiro/skills/check-fix-accessibility/` |
   | **Codex** | — | `$CODEX_HOME/skills/check-fix-accessibility/` (default `~/.codex/skills/`) |
   | **Antigravity** | `.agent/skills/check-fix-accessibility/` | `~/.gemini/antigravity/skills/check-fix-accessibility/` |

   Example (Cursor, project scope):

   ```bash
   mkdir -p .cursor/skills
   cp -r check-fix-accessibility .cursor/skills/
   ```

3. **Restart** your assistant (or start a new session). Ask about accessibility, a11y, or WCAG—the skill should load automatically.

4. **Optional — MCP:** a third-party server. Read the [caveat and exact config paths](#mcp-a11y-mcp-configuration) before you enable it. The skill works without it.

**Detailed steps** (rules, skill-installer, layouts): see [Setup by platform](#setup-by-platform) below.

---

## What’s in this repo

The **repo root** holds LICENSE, README, and .gitignore. The **skill** is in the **check-fix-accessibility** subfolder: copy that folder into your tool's skills directory.

```
check-fix-accessibility/          ← repo root
├── LICENSE
├── README.md
├── .gitignore
├── examples/mcp/                        ← optional MCP samples (not auto-loaded)
└── check-fix-accessibility/             ← the skill (copy this folder when installing)
    ├── SKILL.md                 ← main skill (required by all platforms)
    ├── frameworks.md           ← React, Vue, and Angular patterns
    └── reference.md            ← WCAG, ARIA, testing, native mobile
```

| Path | Purpose |
|------|--------|
| **check-fix-accessibility/SKILL.md** | Main skill: workflow, checklist, fix patterns, corner cases. |
| **check-fix-accessibility/frameworks.md** | React, Vue, and Angular: labels, buttons, modals, route focus, component tests. |
| **check-fix-accessibility/reference.md** | Deeper reference: WCAG summary, ARIA patterns, testing tools, screen readers, native mobile. |
| **README.md** | This file: setup for Cursor, Claude, Kiro, Codex, Google Antigravity. |

When installing, use the **check-fix-accessibility** folder so your tool sees a skill directory named `check-fix-accessibility` containing `SKILL.md`, `frameworks.md`, and `reference.md`.

---

## MCP (a11y-mcp) configuration

Optional, and off unless you turn it on. The endpoint below is a **third-party hosted server** (`a11y-mcp.withjavascript.com`). Content the assistant sends to that server leaves your machine. The server can also go offline or change without notice. Vet it before you enable it, or skip MCP and use the skill on its own. This repo does not ship a live MCP config, so cloning it does not connect you.

Merge the server into the `mcpServers` object you already have. Don’t replace the whole file.

| Assistant | Project file | User file | Notes |
|-----------|--------------|-----------|--------|
| **Cursor** | `.cursor/mcp.json` | `~/.cursor/mcp.json` | Project wins when the same server name is in both. Cursor does not read MCP from `.vscode/settings.json`. |
| **Claude Code** | `.mcp.json` (repo root) | `~/.claude.json` (`mcpServers`) | Not `~/.claude/settings.json`. Prefer `claude mcp add`. |
| **Codex** | `.codex/config.toml` (trusted projects) | `~/.codex/config.toml` | TOML key is `mcp_servers`, not `mcpServers`. `url` is Streamable HTTP. This server publishes legacy SSE (`/sse`), which Codex does not treat as that `url`. Don’t paste it in and assume it connects. |
| **Kiro** | `.kiro/settings/mcp.json` | `~/.kiro/settings/mcp.json` | Workspace overrides user. |
| **Antigravity** | `.agents/mcp_config.json` | `~/.gemini/config/mcp_config.json` | Remote servers use `serverUrl`, not `url`. IDE: agent panel → MCP Servers → View raw config. |

Cursor, Claude Code, and Kiro share this shape. Copy it from [`examples/mcp/cursor.mcp.json`](examples/mcp/cursor.mcp.json) into the file for your tool:

```json
{
  "mcpServers": {
    "a11y-mcp": {
      "url": "https://a11y-mcp.withjavascript.com/sse"
    }
  }
}
```

Antigravity uses `serverUrl` instead of `url`. See [`examples/mcp/antigravity.mcp_config.json`](examples/mcp/antigravity.mcp_config.json).

The heading anchor for this section is [`#mcp-a11y-mcp-configuration`](#mcp-a11y-mcp-configuration).

---

## Setup by platform

Paths are in the [quick start table](#quick-start). Copy the `check-fix-accessibility` folder into the directory for your tool. From the repo root, this is the project-scope Cursor path:

```bash
mkdir -p .cursor/skills
cp -r check-fix-accessibility .cursor/skills/
```

Swap `.cursor/skills` for the directory in that table. Restart the assistant after copying. The installed folder contains `SKILL.md`, `frameworks.md`, and `reference.md`.

### Notes that are not the copy command

- **Cursor:** Do not put the skill in `~/.cursor/skills-cursor/`. That directory is reserved for Cursor's built-in skills.
- **Claude Code:** Copy the folder, or add a short rule that points at it. Project (`.claude/`) overrides user (`~/.claude/`).

  ```markdown
  ---
  description: Accessibility (a11y) audit and fix guidance
  paths: "**/*.tsx","**/*.jsx","**/*.vue","**/*.html"
  ---

  When working on accessibility, read:
  - check-fix-accessibility/SKILL.md
  - check-fix-accessibility/frameworks.md
  - check-fix-accessibility/reference.md
  ```

- **Kiro:** `SKILL.md` already has `name` and `description` frontmatter. A workspace skill in `.kiro/skills/` overrides the same name in `~/.kiro/skills/`. See [Kiro Agent Skills](https://kiro.dev/docs/skills/).
- **Codex:** There is no project-scope skills directory. Ask the skill-installer: "Install the skill from GitHub repo `YOUR_USERNAME/check-fix-accessibility`, path `check-fix-accessibility`." Or copy the folder into `$CODEX_HOME/skills/` (default `~/.codex/skills/`).
- **Antigravity:** The frontmatter `description` is what matches the user's request. [Antigravity skills](https://antigravity.google/docs/skills).

---

## Skill contents (summary)

- **Audit**: Lighthouse, axe, pa11y, and pinned ESLint plugins (`eslint-plugin-jsx-a11y`, `eslint-plugin-vuejs-accessibility`).
- **React tests**: jest-axe / vitest-axe, Testing Library role queries, cypress-axe, `@axe-core/playwright`. See [Automated testing in React](check-fix-accessibility/reference.md#automated-testing-in-react).
- **Checklist**: Semantics, landmarks, headings, focus, keyboard, forms, labels, images, ARIA, contrast, motion, zoom, plus WCAG 2.2 AA items (2.4.11 focus not obscured, 2.5.7 dragging, 2.5.8 target size, 3.2.6 consistent help, 3.3.7 redundant entry, 3.3.8 accessible authentication) and commonly missed 2.1 criteria (1.3.5 autocomplete, 1.4.12 text spacing, 1.4.13 hover/focus content, 2.1.4 character shortcuts, 2.5.3 label in name).
- **Corner cases**: Screen readers, voice control vs Amazon VoiceView, SPAs, modals, live regions, RTL, CAPTCHA.
- **Fix patterns**: Custom controls, native `<dialog>`, expand/collapse, tabs, error messages. A worked report is in [Providing feedback](check-fix-accessibility/SKILL.md#providing-feedback).
- **reference.md**: WCAG 2.2 summary (including the new 2.2 criteria), checklist rationale, target size, ARIA patterns, React focus and routing, screen reader testing, native mobile. In **check-fix-accessibility/reference.md**.
- **frameworks.md**: React (`useId`, `createPortal`, React Router, Next.js), Vue (`useId`, `<Teleport>`, Vue Router), Angular (`cdkTrapFocus`, CDK dialog, `NavigationEnd`), plus component axe tests. In **check-fix-accessibility/frameworks.md**.
- **AAA**: Opt-in only, in [reference.md](check-fix-accessibility/reference.md#when-the-user-asks-for-aaa). A and AA stay the default.
- **Audit snippet**: Copy-paste `a11y:axe` and `a11y:pa11y` scripts in reference.md. This repo does not ship a runner.
- **Version**: 1.8.0, reviewed 2026-10-01 against WCAG 2.2 A/AA. [Changelog](check-fix-accessibility/SKILL.md#changelog).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---

## Contributing

Improvements and fixes are welcome. Suggested focus:

- Keeping WCAG and ARIA guidance aligned with current standards.
- Adding short examples or scripts that match the checklist (e.g. running axe or pa11y).
- Clarifying setup steps for any of the five platforms.

Open an issue or pull request on the GitHub repo.

Pull requests are reviewed by [CodeRabbit](https://coderabbit.ai/) when the GitHub App is installed on this repository. Preferences live in [`.coderabbit.yaml`](.coderabbit.yaml): skill files and the README get an accessibility-accuracy pass, and files under `assets/` are skipped. Reply on the review thread if a comment is wrong. Installing the app is a repository setting (GitHub → Settings → GitHub Apps, or [the CodeRabbit app](https://github.com/apps/coderabbitai)); the yaml file does not install it.
