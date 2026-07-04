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

## Automated testing in React

Static linting (`eslint-plugin-jsx-a11y`) only catches a subset of issues; add runtime checks against the rendered DOM. Pin versions (versions below are known-good as of the "Last reviewed" date in SKILL.md).

- **Query by accessibility, not by test id**: Testing Library's role/name queries double as a11y assertions — if `getByRole('button', { name: 'Save' })` can't find it, neither can assistive tech. Prefer `getByRole` / `getByLabelText` over `getByTestId`. `npm i -D @testing-library/react@16.3.2 @testing-library/jest-dom@6.9.1`.

```tsx
import { render, screen } from '@testing-library/react';

test('save button has an accessible name', () => {
  render(<Toolbar />);
  // Throws if no button is exposed with this accessible name/role.
  expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
});
```

- **Component-level axe (Jest)**: `npm i -D jest-axe@10.0.0`. Assert zero violations on rendered output.

```tsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';

test('form has no a11y violations', async () => {
  const { container } = render(<SignupForm />);
  expect(await axe(container)).toHaveNoViolations();
});
```

- **Component-level axe (Vitest)**: use `vitest-axe@0.1.0` (same API as `jest-axe`, wired for Vitest's `expect`).
- **End-to-end axe**: run axe against the real running app in E2E, where routing, portals, and focus behave realistically.
  - Cypress: `npm i -D cypress-axe@1.7.0 axe-core@4.12.1` → `cy.injectAxe()` then `cy.checkA11y()`.
  - Playwright: `npm i -D @axe-core/playwright@4.12.1` → `new AxeBuilder({ page }).analyze()` and assert `results.violations` is empty.
- **Scope caveat**: axe finds ~30–50% of issues. Keep manual keyboard + screen-reader checks for focus order, live-region timing, and semantics that automation can't judge.

## React focus & routing

Generic SPA advice ("move focus / announce on route change") needs concrete React patterns:

- **Focus on mount / step change**: use a `ref` + `useEffect` to move focus (e.g. to a heading or first field). Give the target `tabIndex={-1}` so it's programmatically focusable without joining the tab order.

```tsx
const headingRef = useRef<HTMLHeadingElement>(null);
useEffect(() => { headingRef.current?.focus(); }, [routeKey]);
return <h1 ref={headingRef} tabIndex={-1}>{title}</h1>;
```

- **Route changes (react-router `7.18.1`)**: client navigation doesn't reset focus or update the title like a full page load. On each navigation, update `document.title` and move focus to `<main>`/the page `<h1>` (or announce via a persistent `aria-live="polite"` region). Trigger off `useLocation()`'s `pathname`.
- **Focus trapping (modals/dialogs/menus)**: don't hand-roll it. Use `react-focus-lock@2.13.7` or `focus-trap-react@12.0.3` to trap focus, restore focus to the trigger on close, and handle Escape.
- **Accessible primitives**: prefer libraries that ship correct roles, keyboard interaction, and focus management over building widgets from `div`s: `react-aria@3.50.0` (React Aria / React Aria Components), Radix UI, or Headless UI (`@headlessui/react@2.2.10`). You still supply accessible names and verify behavior, but you inherit the hard parts (arrow-key nav, `aria-*` wiring, focus return).
- **Don't fight the primitive**: when using the libraries above, avoid re-adding `role`/`tabindex`/`aria-*` they already manage — duplicating them causes double or wrong announcements.

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
