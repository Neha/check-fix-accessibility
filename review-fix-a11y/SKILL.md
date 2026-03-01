---
name: check-fix-accessibility
description: Check and fix accessibility (a11y) on front-end projects (web and mobile web), including Next.js, React, Vue, Angular. Use when the user asks about accessibility, a11y, WCAG, screen readers, voice control, Voice View, keyboard navigation, focus management, ARIA, semantic HTML, color contrast, or fixing accessibility issues in HTML, React, Next.js, Vue, or other front-end code. For native mobile apps (React Native, iOS, Android), see reference; patterns differ.
---

# Check and Fix Front-End Accessibility

Systematically audit and fix accessibility issues in any front-end project. Prioritize WCAG 2.2 Level A and AA unless the user specifies otherwise.

## Scope

- **Web (desktop + mobile web)**: Full scope. This skill applies to HTML/CSS/JS, React, **Next.js**, Vue, Angular, and other web frameworks, including responsive and PWA. Next.js: use `metadata` or `<Head>` for page `<title>`; client-side navigation counts as SPA route changes — update focus/announce on route change (see Corner cases).
- **Native mobile apps** (React Native, Swift/Kotlin, Flutter): Different APIs and patterns (e.g. `accessibilityLabel`, `accessibilityRole`). Apply the same principles (labels, focus order, semantics) but use platform APIs. See [reference.md](reference.md) for pointers.

## Quick workflow

1. **Audit** – Run automated checks and/or review key pages/components.
2. **Prioritize** – Address critical (blocking) and serious issues first.
3. **Fix** – Apply fixes following patterns below; re-check after changes.
4. **Verify** – Confirm keyboard flow and, if possible, screen reader behavior.

## Running audits

Use at least one automated tool; combine with manual review for important flows.

- **Lighthouse** (Chrome DevTools): Run Accessibility audit. Good for full-page snapshot.
- **axe DevTools** (browser extension or `@axe-core/cli`, `axe-core` in tests): Run on the page or component. Report and fix by rule ID.
- **pa11y** (CLI): `npx pa11y <url>` for terminal reports.
- **ESLint + plugins**: `eslint-plugin-jsx-a11y` (React), `vue-eslint-plugin-vuejs-accessibility` (Vue). Add to CI and fix reported rules.

When fixing, use the tool’s rule ID (e.g. `button-name`, `label`, `color-contrast`) to look up the exact requirement and apply the right fix.

## Checklist: common issues and fixes

Copy and use as a progress list. Not exhaustive; expand from audit results.

### Semantics and structure

- [ ] **Page title**: One `<title>` per page, descriptive and unique.
- [ ] **Landmarks**: Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>` (or ARIA `role="main"` etc. only when you can’t use the element). One `<main>` per page.
- [ ] **Headings**: Logical order (`h1` → `h2` → `h3`), no skips. Use for structure, not just styling.
- [ ] **Lists**: Use `<ul>`/`<ol>`/`<li>` for list content; don’t use only divs + CSS.
- [ ] **Buttons vs links**: Use `<button>` for actions (submit, open modal, toggle). Use `<a href="...">` for navigation. Don’t use `<div>` or `<span>` for buttons/links without making them focusable and exposing role and name.

### Focus and keyboard

- [ ] **Focus visible**: All interactive elements show a visible focus indicator (outline/box-shadow). Never remove focus outline without replacing it with a clear custom style.
- [ ] **Tab order**: DOM order matches visual/logical order, or use `tabIndex` and/or `aria-flowto` only when necessary and documented.
- [ ] **Keyboard operable**: Every mouse action has a keyboard path (click → Enter/Space; hover reveals → focus reveals or separate keyboard trigger).
- [ ] **Focus trapping**: Modals/dialogs trap focus inside until closed; focus returns to trigger on close.
- [ ] **Skip link**: Provide "Skip to main content" (or equivalent) for repeated nav; ensure it’s visible on focus and moves focus to main content.

### Forms and labels

- [ ] **Labels**: Every form control has an associated `<label>` (by `id`/`for` or wrapping) or `aria-label`/`aria-labelledby`. Placeholder is not the label.
- [ ] **Errors**: Associate error messages with controls (e.g. `aria-describedby`, `aria-invalid`) and announce errors to screen readers.
- [ ] **Required/optional**: Indicate with `aria-required` and/or visible text; ensure required fields are clearly marked.
- [ ] **Grouping**: Use `<fieldset>` + `<legend>` for radio/checkbox groups.

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

### Color and contrast

- [ ] **Contrast**: Text (and important graphics) meets WCAG AA: 4.5:1 for normal text, 3:1 for large text. Use a contrast checker (e.g. DevTools, WebAIM) and fix background/foreground.
- [ ] **Not color alone**: Don’t convey information or state by color only. Add icons, text, or pattern (e.g. "Error" + red; "Required" + asterisk).

### Motion and animation

- [ ] **Reduce motion**: Respect `prefers-reduced-motion: reduce` (CSS or JS) by disabling or simplifying non-essential motion. Don’t rely on animation for critical information.

### Responsive and zoom

- [ ] **Zoom**: Layout works at 200% zoom (and preferably up to 400%). No horizontal scrolling at 320px width unless the content is inherently wide (e.g. data tables).
- [ ] **Touch targets**: Interactive elements at least 44×44 CSS pixels where possible.

## Corner cases and edge cases

Handle these explicitly; they are often missed by automated tools.

### Screen readers

- **Screen-reader-only text**: When visible label would be redundant (e.g. icon-only button), add a visible-for-SR label (e.g. `.sr-only` / `aria-label`) so the control has a clear name. Don't rely on `title` alone for critical labels.
- **Tables**: Data tables use `<table>`, `<th>` with `scope` or `headers`, and `<caption>` or `aria-labelledby` so screen reader users can navigate by cell. Avoid tables for layout.
- **Iframes**: Every `<iframe>` needs a descriptive `title` (or `aria-label`) so SR users know what the region is.
- **Link purpose**: Link text must make sense out of context. Avoid "Click here" or "Read more" alone; use descriptive text or `aria-label` that includes context.
- **Duplicate announcements**: Avoid announcing the same thing twice (e.g. both `aria-label` and visible text saying the same; multiple live regions for one update). Use one clear source of truth.
- **Language of parts**: Use `lang` on an element when its content is in a different language than the page (e.g. `<span lang="fr">`), so SR uses the correct pronunciation.
- **Announcement order**: Ensure live regions and focus moves don't create confusing order (e.g. result announced before "Loading" is removed). Use `aria-busy` during loading and clear it when content is ready.

### Voice control / Voice View

- **Distinct, speakable labels**: Users of voice input (e.g. Voice Access, Dragon, Voice Control) say element names. Avoid many elements with the same label (e.g. multiple "Submit" or "Button"). Use unique, short labels (e.g. "Submit registration", "Cancel") so users can say "Click Submit registration".
- **Numbering**: If labels can't be unique, voice software may fall back to "first button", "second link". Prefer unique labels over relying on order.

### Single-page apps (SPA) and dynamic content

- **Route / view changes**: On navigation, update `<title>` and move focus to main content or announce the change (e.g. `aria-live="polite"` region or focus to `<main>`/heading) so SR users know the page changed.
- **Loading states**: Use `aria-busy="true"` on the loading container and set to `false` when done. Optionally use a live region to announce "Loading…" and then the result.
- **Hidden but focusable**: Content that is hidden (e.g. `display: none`, `hidden`, inactive tab panel) must not contain focusable elements, or those elements must be removed from the accessibility tree (e.g. `aria-hidden="true"` on container, or `inert` where supported). Otherwise keyboard/SR users can focus "invisible" elements.

### Other

- **Time limits**: If the content has a time limit (session timeout, quiz), provide a way to extend, turn off, or adjust it (WCAG 2.2).
- **CAPTCHA / verification**: Provide an accessible alternative (e.g. audio CAPTCHA, alternative task) and ensure the flow is keyboard/SR accessible.
- **RTL**: For right-to-left languages, set `dir="rtl"` (or appropriate `dir`) on the document or container so layout and reading order are correct.
- **Third-party embeds**: If you embed widgets or iframes you don't control, document that they should be accessible or provide an alternative (e.g. link to same content elsewhere).

## Fix patterns (concise)

- **Custom control**: Use the right native element or add `role`, `tabindex="0"` (or `-1` if managed by script), and `aria-*` state/name. Handle Enter/Space and focus.
- **Modal**: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (title), focus move to dialog on open, trap focus, Escape closes, focus return on close.
- **Expand/collapse**: `aria-expanded` and `aria-controls` on trigger; `id` on panel; toggle on Enter/Space.
- **Tabs**: `role="tablist"`, `role="tab"` (with `aria-selected`, `aria-controls`), `role="tabpanel"` (with `id`); arrow keys switch tabs; activate on Enter/Space.
- **Error message**: `aria-describedby="id-of-error"` on control, `aria-invalid="true"` when invalid; ensure error element has `id` and is in DOM when invalid.

## Providing feedback

When reporting issues, use:

- **Critical**: Blocks access (e.g. no focus, missing labels, no keyboard path). Fix first.
- **Serious**: Major barrier (e.g. poor contrast, wrong semantics). Fix soon.
- **Minor**: Improves experience (e.g. redundant ARIA, heading order). Fix when practical.

Include: file/component, element or selector, rule or guideline, and a concrete fix (code or steps).

## After fixing

- Re-run the same audit tool and confirm violations are gone or explained.
- Test keyboard-only navigation through the flow.
- If possible, test with one screen reader (e.g. NVDA, VoiceOver) for the changed components.

## Reference

For detailed WCAG criteria, ARIA patterns, and component examples, see [reference.md](reference.md) when you need deeper guidance.
