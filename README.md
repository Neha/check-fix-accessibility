# Check and Fix Accessibility (a11y) Skill

A reusable **accessibility (a11y) skill** for AI coding assistants. It teaches the agent how to audit and fix front-end accessibility issues (WCAG 2.2 Level A/AA), including semantics, keyboard navigation, ARIA, forms, contrast, and screen readers—for web (React, Next.js, Vue, Angular) and with pointers for native mobile.

Use this skill when you or your team work on accessibility, a11y, WCAG, screen readers, keyboard navigation, focus management, ARIA, semantic HTML, or fixing accessibility issues in HTML/React/Next.js/Vue or other front-end code.

---

## Installation

Run the following command. It will prompt you to choose your AI agent and different configurations. Installing it as a project skill is recommended for teams

```sh
npx skills add Neha/check-fix-accessibility
```

---

## What’s in this repo

The **repo root** holds LICENSE, README, and .gitignore. The **skill** is in the **review-fix-a11y** subfolder: copy that folder into your tool's skills directory.

```
check-fix-accessibility/          ← repo root
├── LICENSE
├── README.md
├── .gitignore
└── review-fix-a11y/             ← the skill
    ├── SKILL.md                 ← main skill (required by all platforms)
    └── reference.md            ← WCAG, ARIA, testing, native mobile
```

| Path | Purpose |
|------|--------|
| **review-fix-a11y/SKILL.md** | Main skill: workflow, checklist, fix patterns, corner cases. |
| **review-fix-a11y/reference.md** | Deeper reference: WCAG summary, ARIA patterns, testing tools, screen readers, native mobile. |
| **README.md** | This file: setup for Cursor, Claude, Kiro, Codex, Google Antigravity. |

When installing, use the **review-fix-a11y** folder so your tool sees a skill directory named `review-fix-a11y` containing `SKILL.md` and `reference.md`.

---

## Quick reference: where files go

| Platform        | Project scope                          | User scope (global)           |
|----------------|----------------------------------------|-------------------------------|
| **Cursor**     | `.cursor/skills/review-fix-a11y/`      | `~/.cursor/skills/review-fix-a11y/` |
| **Claude**     | `.claude/rules/` (e.g. `accessibility.mdc`) or reference from `CLAUDE.md` | `~/.claude/skills/review-fix-a11y/` + `CLAUDE.md` |
| **Kiro**       | `.kiro/skills/review-fix-a11y/`        | (Check Kiro docs for global path) |
| **Codex**      | —                                      | `$CODEX_HOME/skills/review-fix-a11y/` (default `~/.codex/skills/`) |
| **Antigravity**| `.agent/skills/review-fix-a11y/`       | `~/.gemini/antigravity/skills/review-fix-a11y/` |

Some of the newer version of these tools (cursor, codex, gemini-cli, etc)  also support the [new standard `.agents/skills` directory](https://cursor.com/docs/context/skills#skill-directories)

---

## Skill contents (summary)

- **Audit**: Use Lighthouse, axe, pa11y, ESLint a11y plugins.
- **Checklist**: Semantics, landmarks, headings, focus, keyboard, forms, labels, images/alt, ARIA, contrast, motion, zoom.
- **Corner cases**: Screen readers, voice control, SPAs, modals, live regions, RTL, CAPTCHA.
- **Fix patterns**: Custom controls, modals, expand/collapse, tabs, error messages.
- **reference.md**: WCAG 2.2 summary, ARIA patterns, testing tools, screen reader testing, native mobile (React Native, iOS, Android) pointers. In **review-fix-a11y/reference.md**.

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
