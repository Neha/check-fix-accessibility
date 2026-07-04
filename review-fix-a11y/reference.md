# Accessibility Reference

Use this when you need WCAG criteria, ARIA patterns, native mobile, or component examples beyond the main skill checklist.

## Scope: web vs native mobile

- **Web (desktop + mobile web)**: SKILL.md checklist and patterns apply. Same HTML/ARIA/semantics.
- **Native mobile** (React Native, iOS UIKit, Android View, Flutter): Same principles (labels, focus order, semantics, contrast) but different APIs. Use platform accessibility APIs; automated tools differ. See "Native mobile" below.

## WCAG 2.2 Level A & AA (summary)

WCAG 2.2 became a W3C Recommendation on 5 Oct 2023 (a revised edition was published 12 Dec 2024). It builds on 2.1 and adds success criteria such as focus not obscured (2.4.11), dragging movements (2.5.7), and target size minimum (2.5.8). WCAG 2.2 also **removed** 4.1.1 Parsing (it is now obsolete, as modern user agents handle parsing errors). Conformance to 2.2 satisfies 2.0 and 2.1.

- **Perceivable**: Text alternatives for non-text content; captions/alternatives for media; content presentable in different ways (structure, contrast); distinguishable (contrast, not color-only, resize text).
- **Operable**: Keyboard access; enough time; no seizure-inducing content; navigable (skip links, titles, focus order, link purpose); input modalities (pointer gestures not required, or have keyboard alternative).
- **Understandable**: Readable (language of page); predictable (on focus/input, no unexpected context change); input assistance (labels, error identification/suggestion, help).
- **Robust**: Name, role, value for UI components; compatibility with assistive tech. (Note: 4.1.1 Parsing was removed in WCAG 2.2 and no longer applies.)

## ARIA patterns (high level)

- **Dialog**: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (and optional `aria-describedby`). Trap focus; Escape closes; focus return.
- **Menu / menubar**: `role="menu"` / `role="menubar"`, `role="menuitem"`; arrow keys and Enter/Space; `aria-expanded` on submenus.
- **Tabs**: `role="tablist"`, `role="tab"` (`aria-selected`, `aria-controls`), `role="tabpanel"` (`id`); arrow keys + Enter/Space.
- **Tree**: `role="tree"`, `role="treeitem"` (`aria-expanded`, `aria-level`); arrow keys for expand/collapse and move.
- **Combobox**: `role="combobox"`, `aria-expanded`, `aria-controls` (listbox), `aria-activedescendant` for current option; listbox with `role="option"`; arrow keys + Enter.

Full patterns: [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/).

## Target size (touch/pointer)

- **WCAG 2.2 AA — 2.5.8 Target Size (Minimum)**: pointer targets are at least **24×24 CSS px**, or have sufficient spacing so a 24 px circle centered on the target doesn't overlap neighbors. Exceptions: inline links in text, targets controlled by the user agent, or an equivalent alternative on the same page.
- **WCAG 2.2 AAA — 2.5.5 Target Size (Enhanced)**: at least **44×44 CSS px**.
- **Platform best practice**: Apple HIG recommends **44×44 pt**; Android Material recommends **48×48 dp**. These exceed the AA minimum and are a good default for primary touch controls.

So: **24×24 is the AA bar; 44×44 is best practice / AAA**, not the AA requirement. Aim for the larger size where practical, especially on touch UIs.

## Contrast and color

- Normal text: contrast ratio ≥ 4.5:1 (AA) or 7:1 (AAA).
- Large text (18pt+ or 14pt+ bold): ≥ 3:1 (AA) or 4.5:1 (AAA).
- UI components and graphics: ≥ 3:1 against adjacent colors.

## Testing tools

Pin exact versions (install as `devDependencies` + lockfile) rather than relying on `npx <latest>`, so results are reproducible. Versions below are known-good as of the "Last reviewed" date in SKILL.md; bump them deliberately.

- **Lighthouse**: Chrome DevTools → Lighthouse → Accessibility. (Version tracks Chrome; note it in reports.)
- **axe**: `npm i -D @axe-core/cli@4.12.1 axe-core@4.12.1`; `npx axe <url>` or use the axe DevTools extension.
- **pa11y**: `npm i -D pa11y@9.1.1`; `npx pa11y <url>`.
- **ESLint**: `eslint-plugin-jsx-a11y@6.10.2` (React), `eslint-plugin-vuejs-accessibility@2.5.0` (Vue).
- **Contrast**: Chrome DevTools Inspect → Accessibility pane; or WebAIM Contrast Checker.

## Screen reader testing (manual)

- **Windows**: NVDA (free), JAWS.
- **macOS**: VoiceOver (Cmd+F5).
- **Mobile**: TalkBack (Android), VoiceOver (iOS).

Test: focus order, all interactive elements reachable, names and states announced correctly, dynamic content announced when appropriate.

### Screen reader corner cases

- **Visually hidden label**: Use a utility (e.g. `.sr-only`, `.visually-hidden`) that keeps content in the DOM and readable by SR but hides visually (e.g. `position: absolute; width: 1px; height: 1px; clip: rect(0,0,0,0)`). Don't use `display: none` or `visibility: hidden` for content that should be announced.
- **Tables**: Use `<th scope="col">` / `scope="row"` or `headers="id-of-th"` on `<td>` for complex tables. Add `<caption>` or `aria-labelledby` so the table has a name.
- **Live region timing**: Set `aria-live` and update content after a short delay if the SR might miss very fast updates. Use `aria-atomic="true"` when the whole region should be re-announced.
- **Iframe**: Always give `<iframe title="Description of content">` or `aria-label` so SR knows what the embedded content is.

## Voice control / Voice View

- **Voice control** (e.g. Windows Voice Access, macOS Voice Control, Dragon): Users speak commands like "Click Submit" or "Select checkbox I agree". Labels must be unique and easy to say; avoid long or identical names. Test by speaking the visible labels and numbers.
- **Voice View** (and similar): Voice-driven browsing or assistant features rely on the same accessible names and roles. Ensure every interactive element has a clear, speakable name.

## Native mobile (brief)

- **React Native**: Use `accessibilityLabel`, `accessibilityHint`, `accessibilityRole` (e.g. `button`, `link`, `header`), `accessibilityState` (e.g. `{ disabled, selected, expanded }`), and `accessibilityLiveRegion`. Test with TalkBack (Android) and VoiceOver (iOS).
- **iOS (Swift/UIKit)**: `accessibilityLabel`, `accessibilityHint`, `accessibilityTraits`, `isAccessibilityElement`. Use `UIAccessibility` APIs for custom controls and announcements.
- **Android**: `contentDescription`, `android:importantForAccessibility`, `AccessibilityNodeInfo` for custom views. Use `announceForAccessibility()` for live announcements.
- **Guidelines**: iOS HIG (Accessibility), Android Accessibility guidelines, WCAG applied to mobile where applicable.
