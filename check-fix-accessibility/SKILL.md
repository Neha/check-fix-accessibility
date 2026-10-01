---
name: check-fix-accessibility
description: Check and fix accessibility (a11y) on front-end projects (web and mobile web), including Next.js, React, Vue, Angular. Use when the user asks about accessibility, a11y, WCAG, screen readers, voice control, Voice View, keyboard navigation, focus management, ARIA, semantic HTML, color contrast, or fixing accessibility issues in HTML, React, Next.js, Vue, or other front-end code. For native mobile apps (React Native, iOS, Android), see reference; patterns differ.
version: 1.8.0
standard: WCAG 2.2 (Level A & AA)
last_reviewed: 2026-10-01
---

# Check and Fix Front-End Accessibility

Systematically audit and fix accessibility issues in any front-end project. Prioritize WCAG 2.2 Level A and AA unless the user specifies otherwise. AAA is opt-in: see [reference.md](reference.md#when-the-user-asks-for-aaa).

> **Versioning & currency**: This skill is versioned (see `version` above) and reviewed against a specific standard on the `last_reviewed` date. WCAG and tooling evolve — before relying on it, confirm the standard and pinned tool versions are still current, and bump `version` + `last_reviewed` and the [Changelog](#changelog) when you update guidance.

## Scope

- **Web (desktop + mobile web)**: Full scope. This skill applies to HTML/CSS/JS, React, **Next.js**, Vue, Angular, and other web frameworks, including responsive and PWA. Next.js: use `metadata` or `<Head>` for page `<title>`; client-side navigation counts as SPA route changes — update focus/announce on route change (see Corner cases). Per-framework label, button, modal, and router snippets: [frameworks.md](frameworks.md).
- **Native mobile apps** (React Native, Swift/Kotlin, Flutter): Different APIs and patterns (e.g. `accessibilityLabel`, `accessibilityRole`). Apply the same principles (labels, focus order, semantics) but use platform APIs. See [reference.md](reference.md) for pointers.

## Quick workflow

1. **Audit** – Run automated checks and/or review key pages/components.
2. **Prioritize** – Address critical (blocking) and serious issues first.
3. **Fix** – Apply fixes following patterns below; re-check after changes.
4. **Verify** – Confirm keyboard flow and, if possible, screen reader behavior.

## Running audits

Use at least one automated tool; combine with manual review for important flows.

**Pin tool versions for reproducibility.** Install tools as `devDependencies` with an exact version (in `package.json` and the lockfile). Pins below were checked on 2026-10-01 against the snippets in this skill. They are not a claim that a newer release is wrong. A newer major is named when it would change the snippet.

- **Lighthouse** (Chrome DevTools): Run Accessibility audit. Good for a full-page snapshot. Note the Chrome/Lighthouse version in the report.
- **axe DevTools** (browser extension or `@axe-core/cli`, `axe-core` in tests): Report and fix by rule ID. Pin: `npm i -D @axe-core/cli@4.13.0 axe-core@4.13.0`.
- **pa11y** (CLI): `npm i -D pa11y@10.0.0`, then `npx pa11y <url>`. pa11y 10 needs Node `^22.13.0` or `>=24`. The command is the same as 9.1.1, which still runs on older Node.
- **ESLint + plugins**: `eslint-plugin-jsx-a11y@6.10.2` (React), `eslint-plugin-vuejs-accessibility@2.6.0` (Vue). Add them to CI and fix the reported rules.

When fixing, use the tool’s rule ID (e.g. `button-name`, `label`, `color-contrast`) to look up the exact requirement and apply the right fix.

Test the rendered component, not only the deployed URL. Prefer role and name queries over test ids. React, Vue, and Angular lint plugins and one axe example each: [frameworks.md](frameworks.md#component-tests). React runtime detail (cypress-axe, Playwright): [reference.md](reference.md#automated-testing-in-react).

## Checklist: common issues and fixes

Copy and use as a progress list. Not exhaustive; expand from audit results.

### Semantics and structure

- [ ] **Page language** (3.1.1 A): Set `lang` on `<html>`.
- [ ] **Page title**: One `<title>` per page, descriptive and unique.
- [ ] **Landmarks**: Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>` (or ARIA `role="main"` etc. only when you can’t use the element). One `<main>` per page.
- [ ] **Headings** (2.4.6 AA): The heading text describes the section. Skipping a level is a best-practice issue, not what 2.4.6 checks, and not an automatic AA failure.
- [ ] **Lists**: Use `<ul>`/`<ol>`/`<li>` for list content; don’t use only divs + CSS.
- [ ] **Buttons vs links**: Use `<button>` for actions (submit, open modal, toggle). Use `<a href="...">` for navigation. Don’t use `<div>` or `<span>` for buttons or links.
- [ ] **Consistent help** (3.2.6 AA): Keep help in the same relative order on every page. See [rationale](reference.md#checklist-rationale).

### Focus and keyboard

- [ ] **Focus visible** (2.4.7 AA): Every interactive element has a visible focus indicator. Don’t remove the outline without a replacement.
- [ ] **Tab order** (2.4.3 A): DOM order matches visual order. Don’t use a positive `tabindex`. There is no `aria-flowto` attribute.
- [ ] **No keyboard trap** (2.1.2 A): Focus can always move away, except a modal that traps on purpose and then releases.
- [ ] **Keyboard operable** (2.1.1 A): Every mouse action has a keyboard path (Enter/Space, or a focusable control instead of hover-only).
- [ ] **Focus trapping**: A modal traps focus until it closes, then returns focus to the trigger.
- [ ] **Skip link** (2.4.1 A): "Skip to main content" is visible on focus and moves focus to `<main>`.
- [ ] **Focus not obscured** (2.4.11 AA): Sticky headers, footers, and banners don’t fully cover the focused element. See [rationale](reference.md#checklist-rationale).
- [ ] **Character key shortcuts** (2.1.4 A, not AA): Single-character shortcuts can be turned off, remapped, or limited to when the control is focused.
- [ ] **Dragging alternative** (2.5.7 AA): Drag actions also work with a click, tap, or text field.

### Forms and labels

- [ ] **Labels**: Every control has a `<label>` (`for`/`id` or wrapping) or `aria-label`/`aria-labelledby`. Placeholder is not a label.
- [ ] **Label in name** (2.5.3 AA): The accessible name includes the visible text. `aria-label` replaces the contents, so don’t use it on a control that already shows a label.
- [ ] **Errors** (3.3.1 A): The error is visible text, not only a color or a live region. Point at it with `aria-describedby`, set `aria-invalid="true"`, and keep it in the DOM while it applies.
- [ ] **Required/optional**: Mark required fields in text and with `aria-required` or the `required` attribute.
- [ ] **Grouping**: Use `<fieldset>` and `<legend>` for radio and checkbox groups.
- [ ] **Unavailable controls**: `disabled` removes the control from tab order. Use `aria-disabled="true"` when the user still needs to focus it and hear why.
- [ ] **Input purpose** (1.3.5 AA): Set `autocomplete` (`name`, `email`, `tel`, `street-address`, and so on).
- [ ] **Accessible authentication** (3.3.8 AA): Allow paste and password managers. Don’t make a puzzle or transcription the only way in.
- [ ] **Redundant entry** (3.3.7 AA): Don’t ask for the same information again in one process. Auto-fill it or let the user select it.
- [ ] **No surprise on focus or input** (3.2.1 A, 3.2.2 A): Focusing or typing in a control doesn’t change context (submit, navigate, or open a new window) by itself.

### Images and media

- [ ] **Alt text**: All meaningful images have `alt` describing content or function. Decorative images use `alt=""`.
- [ ] **Complex images**: Charts, diagrams, etc. have extended description (long description page, `aria-describedby`, or visible text).
- [ ] **Video/audio**: Provide captions and/or transcripts where applicable; ensure controls are keyboard accessible and labeled.

### ARIA (when HTML isn’t enough)

- [ ] **Roles**: Use native elements first (button, link, heading, etc.). Add ARIA roles only for custom widgets (e.g. `role="dialog"`, `role="tablist"`).
- [ ] **Names**: Interactive elements and regions have an accessible name: `aria-label`, `aria-labelledby`, or visible text content.
- [ ] **Live regions**: Use `aria-live`, `aria-atomic`, `aria-relevant` for dynamic content that should be announced (toasts, errors, updates). Prefer `aria-live="polite"` unless urgent.
- [ ] **State**: Expose state (expanded/collapsed, selected, current) with `aria-expanded`, `aria-selected`, `aria-current`, etc., and keep it in sync with the UI.
- [ ] **Avoid**: Don’t use `role`/`aria-*` on elements that already have that semantics (e.g. `role="button"` on `<button>`). Prefer not to add `aria-hidden="true"` to focusable content.
- [ ] **Content on hover or focus** (1.4.13 AA): Tooltips are dismissible (Escape), hoverable, and persistent. See [rationale](reference.md#checklist-rationale).
- [ ] **Status messages** (4.1.3 AA): Results that don’t move focus (toasts, "Saved", form errors) go through a live region.

### Color and contrast

- [ ] **Contrast** (1.4.3 AA): 4.5:1 for normal text, 3:1 for large text. See [reference.md](reference.md#contrast-and-color).
- [ ] **Non-text contrast** (1.4.11 AA): Meaningful icons and control boundaries are at least 3:1 against the adjacent color.
- [ ] **Not color alone** (1.4.1 A): Add text, an icon, or a pattern. Color can’t be the only cue.
- [ ] **Forced colors**: Don’t rely on background images for meaning. See [rationale](reference.md#checklist-rationale).

### Motion and animation

- [ ] **Pause, stop, hide** (2.2.2 A): Content that moves, blinks, or auto-updates for more than 5 seconds can be paused, stopped, or hidden.
- [ ] **Reduce motion** (2.3.3 AAA): Honor `prefers-reduced-motion: reduce` for non-essential animation. This is AAA, not AA.

### Responsive and zoom

- [ ] **Resize text** (1.4.4 AA): Text can grow to 200% without clipping. Don't set `user-scalable=no`, and don't lock type to `px` if that cuts it off.
- [ ] **Reflow** (1.4.10 AA): At 400% zoom, no two-dimensional scrolling except for content that needs it (maps, tables, diagrams). This is separate from 1.4.4.
- [ ] **Text spacing** (1.4.12 AA): User spacing overrides don’t clip content. See [rationale](reference.md#checklist-rationale).
- [ ] **Touch targets** (2.5.8 AA): At least 24×24 CSS px, or spacing that meets the criterion. 44×44 is AAA / platform practice, not the AA minimum. See [reference.md](reference.md#target-size-touchpointer).

## Corner cases and edge cases

Handle these explicitly; they are often missed by automated tools.

### Screen readers

- **Screen-reader-only text**: When visible label would be redundant (e.g. icon-only button), add a visible-for-SR label (e.g. `.sr-only` / `aria-label`) so the control has a clear name. Don't rely on `title` alone for critical labels.
- **Tables**: Data tables use `<table>`, `<th>` with `scope` or `headers`, and `<caption>` or `aria-labelledby` so screen reader users can navigate by cell. Avoid tables for layout.
- **Iframes**: Every `<iframe>` needs a descriptive `title` (or `aria-label`) so SR users know what the region is.
- **Link purpose** (2.4.4 A): The purpose is clear from the link text together with its context (the sentence, list item, or cell). "Read more" passes A/AA when that context names the destination. Link text that must stand alone is 2.4.9 AAA, in [reference.md](reference.md#when-the-user-asks-for-aaa).
- **Duplicate announcements**: Avoid announcing the same thing twice (e.g. both `aria-label` and visible text saying the same; multiple live regions for one update). Use one clear source of truth.
- **Language of parts**: Use `lang` on an element when its content is in a different language than the page (e.g. `<span lang="fr">`), so SR uses the correct pronunciation.
- **Announcement order**: Ensure live regions and focus moves don't create confusing order (e.g. result announced before "Loading" is removed). Use `aria-busy` during loading and clear it when content is ready.

### Voice control and VoiceView

These are different tools. Don’t treat VoiceView as speech input.

- **Voice control** (Voice Access, macOS Voice Control, Dragon): Users speak the accessible name ("Click Submit registration"). Names must be unique and short. Prefer that over "first button / second button".
- **VoiceView** (Amazon Fire OS screen reader): It reads names, roles, and states, the same way TalkBack does. It is not a voice-command product. Test procedure: [reference.md](reference.md#screen-reader-testing-manual).

### Single-page apps (SPA) and dynamic content

- **Route / view changes**: On navigation, update `<title>` and move focus to main content or announce the change (e.g. `aria-live="polite"` region or focus to `<main>`/heading) so SR users know the page changed. The skip link and `<main>` are the same target. React Router, Next.js, Vue Router, and Angular: [frameworks.md](frameworks.md#react-routing). React focus-trap libraries: [reference.md](reference.md#focus-trap-libraries).
- **Loading states**: Use `aria-busy="true"` on the loading container and set to `false` when done. Optionally use a live region to announce "Loading…" and then the result.
- **Hidden but focusable**: Content that is hidden (e.g. `display: none`, `hidden`, inactive tab panel) must not contain focusable elements, or those elements must be removed from the accessibility tree (e.g. `aria-hidden="true"` on container, or `inert` where supported). Otherwise keyboard/SR users can focus "invisible" elements.

### Other

- **Time limits**: If the content has a time limit (session timeout, quiz), provide a way to extend, turn off, or adjust it (WCAG 2.2).
- **CAPTCHA / verification**: Provide an accessible alternative (e.g. audio CAPTCHA, alternative task) and ensure the flow is keyboard/SR accessible.
- **RTL**: For right-to-left languages, set `dir="rtl"` (or appropriate `dir`) on the document or container so layout and reading order are correct.
- **Third-party embeds**: If you embed widgets or iframes you don't control, document that they should be accessible or provide an alternative (e.g. link to same content elsewhere).

## Fix patterns (concise)

- **Custom control**: Use the native element. If you can’t, add `role`, `tabindex="0"` (or `-1` when script manages focus), an accessible name, and Enter/Space handling.
- **Modal**: Prefer `<dialog>` opened with `showModal()`. In current browsers that traps focus. It does not promise `aria-modal`; give the dialog `aria-labelledby`. A custom dialog needs `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, focus moved in, focus trapped, Escape to close, and focus returned to the trigger.
- **Expand/collapse**: `aria-expanded` and `aria-controls` on trigger; `id` on panel; toggle on Enter/Space.
- **Tabs**: `role="tablist"`, `role="tab"` (with `aria-selected`, `aria-controls`), `role="tabpanel"` (with `id`); arrow keys switch tabs; activate on Enter/Space.
- **Error message**: `aria-describedby="id-of-error"` on control, `aria-invalid="true"` when invalid; ensure error element has `id` and is in DOM when invalid.

## Providing feedback

When reporting issues, use:

- **Critical**: Blocks access (e.g. no focus, missing labels, no keyboard path). Fix first.
- **Serious**: Major barrier (e.g. poor contrast, wrong semantics). Fix soon.
- **Minor**: Improves experience (e.g. redundant ARIA, heading order). Fix when practical.

Include: severity, file or component, element or selector, rule or guideline, and a concrete fix.

**Example**

**Serious** — `src/components/IconButton.tsx` — `button.icon-delete` — axe `button-name` (4.1.2 Name, Role, Value, A). The delete control is an icon-only `<button>` with no accessible name. Add `aria-label="Delete item"` or visually hidden text. Re-run axe on this component and confirm `button-name` is gone. Then Tab to the button and activate it with Enter and Space.

## After fixing

- Re-run the same audit tool and confirm violations are gone or explained.
- Test keyboard-only navigation through the flow.
- If possible, test with one screen reader (e.g. NVDA, VoiceOver) for the changed components.

## Reference

For detailed WCAG criteria, ARIA patterns, and component examples, see [reference.md](reference.md) when you need deeper guidance. Where the checklist above and `reference.md` overlap (e.g. contrast ratios, target sizes, tables), **`reference.md` is the source of truth** — update it first and keep the checklist in sync.

## Changelog

- **1.8.0** (2026-10-01): Rechecked tool pins and stopped calling the July pins current. axe CLI and axe-core are 4.13.0, the Vue ESLint plugin is 2.6.0, pa11y is 10.0.0 (Node 22.13+), jest-axe is 11.0.0. `@testing-library/jest-dom` stays on 6.9.1 because 7.0.1 peers with Vitest only. Route focus is one `<main>` in the app shell and skips the first load. Axe examples call `expect.extend`. Link purpose in context is 2.4.4 A; out-of-context link text stays AAA. Headings 2.4.6 is the description, not the outline. Added 1.4.4 resize text, 3.3.1 visible errors, a combobox pattern, a warning that site navigation is not `role="menu"`, and native modal, decorative-image, and dynamic-type notes. `showModal()` is no longer described as setting `aria-modal`.
- **1.7.0** (2026-10-01): Added an opt-in WCAG AAA section (contrast 7:1, focus not obscured enhanced, focus appearance, 44×44 targets, link purpose from link text alone, reduced motion, accessible authentication enhanced). A and AA stay the default. Added a copy-paste `a11y:axe` / `a11y:pa11y` npm script snippet; this repo does not ship a runner.
- **1.6.0** (2026-10-01): Replaced the one-line screen-reader note with a pass/fail procedure for NVDA, JAWS, VoiceOver, TalkBack, and Amazon VoiceView, including the gestures that move and activate. VoiceView stays a screen reader; Samsung Voice Assistant is named so the two are not swapped. The visually hidden CSS snippet now actually hides the text.
- **1.5.0** (2026-10-01): Added `frameworks.md` with React, Vue, and Angular patterns for labels and ids, native buttons, modals (`createPortal`, `<Teleport>`, `cdkTrapFocus` / CDK dialog), and focus on route change (React Router, Next.js, Vue Router, Angular `NavigationEnd`). Component axe tests for Vue and Angular sit next to the existing React ones. Shared anti-patterns stay in this file.
- **1.4.0** (2026-10-01): Corrected checklist accuracy: removed the non-existent `aria-flowto` attribute; 2.1.4 Character Key Shortcuts is Level A, not AA; skipped headings are best practice, not an automatic AA fail; added 3.1.1 language, 2.5.3 label in name, 2.1.2 no keyboard trap, 1.4.11 non-text contrast, 4.1.3 status messages, 2.2.2 pause/stop/hide, and 3.2.1/3.2.2. Labeled `prefers-reduced-motion` as 2.3.3 AAA. Prefer `<dialog>` / `showModal()`. Distinguished voice control from Amazon VoiceView. Moved long WCAG rationale into `reference.md` and added a worked issue report. Tool version pins from 1.1.0–1.3.0 are unchanged.
- **1.3.0** (2026-07-05): Added the new WCAG 2.2 AA success criteria that were missing from the checklist — 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication — plus 1.3.5 Input Purpose (`autocomplete`), 1.4.13 Content on Hover/Focus, 2.1.4 Character Key Shortcuts, 1.4.12 Text Spacing, and forced-colors/high-contrast guidance. Enumerated all new-in-2.2 criteria in `reference.md`. Renamed the skill folder to `check-fix-accessibility` to match the skill `name` and repo, and noted `reference.md` as the source of truth for overlapping guidance.
- **1.2.0** (2026-07-04): Added React-specific `reference.md` guidance — "Automated testing in React" (jest-axe/vitest-axe, Testing Library role queries, cypress-axe / `@axe-core/playwright`, all pinned) and "React focus & routing" (useEffect+ref focus, react-router, focus-trap libs, accessible primitives like React Aria/Radix/Headless UI); cross-linked from SKILL.md.
- **1.1.0** (2026-07-04): Corrected WCAG 2.2 Recommendation date (Oct 2023; revised edition Dec 2024); removed obsolete 4.1.1 Parsing from Robust; clarified target size (2.5.8 AA = 24×24 CSS px, 44×44 is AAA/platform best practice); pinned tool versions and fixed the Vue ESLint plugin package name; added version/last_reviewed metadata and this changelog.
- **1.0.0**: Initial skill (audit workflow, checklist, corner cases, fix patterns, reference).
