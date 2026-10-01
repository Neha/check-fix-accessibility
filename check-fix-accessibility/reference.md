# Accessibility Reference

Use this when you need WCAG criteria, ARIA patterns, native mobile, or component examples beyond the main skill checklist.

## Scope: web vs native mobile

- **Web (desktop + mobile web)**: SKILL.md checklist and patterns apply. Same HTML/ARIA/semantics.
- **Native mobile** (React Native, iOS UIKit, Android View, Flutter): Same principles (labels, focus order, semantics, contrast) but different APIs. Use platform accessibility APIs; automated tools differ. See "Native mobile" below.

## WCAG 2.2 Level A & AA (summary)

WCAG 2.2 became a W3C Recommendation on 5 Oct 2023 (a revised edition was published 12 Dec 2024). It builds on 2.1 and adds nine new success criteria (see below). WCAG 2.2 also **removed** 4.1.1 Parsing (it is now obsolete, as modern user agents handle parsing errors). Conformance to 2.2 satisfies 2.0 and 2.1.

- **Perceivable**: Text alternatives for non-text content; captions/alternatives for media; content presentable in different ways (structure, contrast); distinguishable (contrast, not color-only, resize text).
- **Operable**: Keyboard access; enough time; no seizure-inducing content; navigable (skip links, titles, focus order, link purpose); input modalities (pointer gestures not required, or have keyboard alternative).
- **Understandable**: Readable (language of page); predictable (on focus/input, no unexpected context change); input assistance (labels, error identification/suggestion, help).
- **Robust**: Name, role, value for UI components; compatibility with assistive tech. (Note: 4.1.1 Parsing was removed in WCAG 2.2 and no longer applies.)

### New success criteria in WCAG 2.2

Don't overlook these when you claim 2.2 conformance — they're the most common gap in checklists carried over from 2.1.

- **2.4.11 Focus Not Obscured (Minimum)** — *AA*: A focused element is not entirely hidden by author-created overlays (sticky headers/footers, cookie banners). Use `scroll-margin`/offsets so it stays visible.
- **2.4.12 Focus Not Obscured (Enhanced)** — *AAA*: No part of the focused element is hidden.
- **2.4.13 Focus Appearance** — *AAA*: Focus indicator has a minimum area and contrast.
- **2.5.7 Dragging Movements** — *AA*: Any dragging action has a single-pointer (non-drag) alternative, unless dragging is essential.
- **2.5.8 Target Size (Minimum)** — *AA*: Pointer targets ≥ 24×24 CSS px or adequately spaced (see [Target size](#target-size-touchpointer)).
- **3.2.6 Consistent Help** — *AA*: Help mechanisms appear in a consistent relative order across pages.
- **3.3.7 Redundant Entry** — *AA*: Don't require re-entering info already provided in the same process (auto-populate or offer selection).
- **3.3.8 Accessible Authentication (Minimum)** — *AA*: No cognitive-function test (memorization, puzzles, transcription) required to authenticate; allow paste/password managers or provide an alternative.
- **3.3.9 Accessible Authentication (Enhanced)** — *AAA*: As 3.3.8 but without the object-recognition/personal-content exceptions.

## Checklist rationale

The skill checklist stays to one line. The detail that used to sit on those lines:

- **3.2.6 Consistent Help (AA)**: When help exists (contact, chat, help page, self-help), keep it in the same relative order on every page.
- **2.4.11 Focus Not Obscured (AA)**: A focused element must not be entirely hidden by a sticky header, footer, or cookie banner. Use `scroll-margin` or an offset so it stays visible.
- **2.1.4 Character Key Shortcuts (A)**: If a single character fires a shortcut, the user can turn it off, remap it, or have it work only while the control is focused. This stops speech input and stray keypresses from activating it. It is Level A, not AA.
- **2.5.7 Dragging Movements (AA)**: Sliders, reorder, and drag-and-drop also work with a single pointer that does not drag (a button or an input).
- **1.3.5 Identify Input Purpose (AA)**: `autocomplete` tokens such as `name`, `email`, `tel`, and `street-address` let browsers and assistive tech fill the field.
- **3.3.8 Accessible Authentication (AA)**: Don’t require memorizing, transcribing, or solving a puzzle as the only sign-in. Allow paste and password managers, or offer another method (OTP, passkey, show password).
- **3.3.7 Redundant Entry (AA)**: In one process, don’t make the user type information they already gave. Auto-populate it or let them select it.
- **1.4.13 Content on Hover or Focus (AA)**: Extra content shown on hover or focus is dismissible (Escape, without moving the pointer), hoverable (the pointer can move onto it), and persistent until the user dismisses it, moves focus, or the content is no longer valid.
- **1.4.12 Text Spacing (AA)**: Content still works when the user sets line height to at least 1.5×, paragraph spacing to at least 2×, letter spacing to at least 0.12em, and word spacing to at least 0.16em. Don’t lock text in a fixed height.
- **Forced colors**: Under `forced-colors: active` (Windows high contrast), don’t put the meaning only in a background image. Use system colors such as `Canvas`, `CanvasText`, and `Highlight` when you must override, and keep the focus indicator visible.
- **2.5.3 Label in Name (AA)**: Speech users say the text they can see. If the visible label is "Search", the accessible name must contain "Search". `aria-label` replaces the text inside the element, so an `aria-label` of "Submit query" on a button that reads "Search" fails.
- **2.2.2 Pause, Stop, Hide (A)** vs **2.3.3 Animation from Interactions (AAA)**: Carousels and auto-updating regions that run longer than 5 seconds need a pause, stop, or hide control (A). Reducing animation when `prefers-reduced-motion: reduce` is set is the AAA criterion. Do the AAA behavior when the user asks for it; don’t label it as required for AA.

## ARIA patterns (high level)

- **Dialog**: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (and optional `aria-describedby`). Trap focus; Escape closes; focus return.
- **Menu / menubar**: `role="menu"` / `role="menubar"`, `role="menuitem"`; arrow keys and Enter/Space; `aria-expanded` on submenus. This is an application menu of actions (a format menu, a context menu). A site header is `<nav>` and links. `role="menu"` on those links takes them out of the tab order.
- **Tabs**: `role="tablist"`, `role="tab"` (`aria-selected`, `aria-controls`), `role="tabpanel"` (`id`); arrow keys + Enter/Space.
- **Tree**: `role="tree"`, `role="treeitem"` (`aria-expanded`, `aria-level`); arrow keys for expand/collapse and move.
- **Combobox**: `role="combobox"` on the input, `aria-expanded`, `aria-controls` pointing at `role="listbox"`, `role="option"` children, and `aria-activedescendant` for the active option. Arrow keys move that option, Enter selects it, Escape closes the list. The input keeps DOM focus. Do not make every option its own tab stop.

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

## When the user asks for AAA

A and AA stay the default. Apply this section only when the user, the ticket, or the spec says AAA (or names one of these criteria). AAA is a claim about a whole page or process. Don’t stamp "WCAG AAA" on a single component, and don’t drop AA work to chase it.

Check these when they match the UI you are fixing. Say which ones you checked and which you skipped.

- **1.4.6 Contrast (Enhanced)**: normal text 7:1, large text 4.5:1. The AA ratios in the list above are not enough for this criterion.
- **2.4.12 Focus Not Obscured (Enhanced)**: no part of the focused element is hidden. AA (2.4.11) only requires that it not be entirely hidden.
- **2.4.13 Focus Appearance**: the focus indicator has a minimum area and a 3:1 contrast change between focused and unfocused states. Follow the criterion text rather than inventing a pixel size.
- **2.5.5 Target Size (Enhanced)**: 44×44 CSS px. This is the size the checklist already calls best practice. It is not the AA minimum (24×24, 2.5.8).
- **2.4.9 Link Purpose (Link Only)**: the link text alone says where it goes. "Read more" fails even with surrounding context.
- **2.3.3 Animation from Interactions**: honor `prefers-reduced-motion: reduce`. Already noted on the checklist as AAA.
- **3.3.9 Accessible Authentication (Enhanced)**: same as 3.3.8 AA, without the exception for recognizing objects or personal content.
- **1.4.8 Visual Presentation** and **3.1.5 Reading Level**: real AAA criteria, and easy to fake. Don’t claim them for app chrome or for button text. Call them out only when the content is a page of prose and you can point at the specific requirement you met.

## Testing tools

Pin exact versions (install as `devDependencies` + lockfile). Pins were checked on 2026-10-01. They match the snippets in this skill. A newer major is named when it would change the snippet.

- **Lighthouse**: Chrome DevTools → Lighthouse → Accessibility. (Version tracks Chrome; note it in reports.)
- **axe**: `npm i -D @axe-core/cli@4.13.0 axe-core@4.13.0`; `npx axe <url>` or use the axe DevTools extension.
- **pa11y**: `npm i -D pa11y@10.0.0`; `npx pa11y <url>`. pa11y 10 needs Node `^22.13.0` or `>=24`. pa11y 9.1.1 is the same command on older Node.
- **ESLint**: `eslint-plugin-jsx-a11y@6.10.2` (React), `eslint-plugin-vuejs-accessibility@2.6.0` (Vue).
- **Contrast**: Chrome DevTools Inspect → Accessibility pane; or WebAIM Contrast Checker.

### Copy-paste audit scripts

There is no runner in this skill repo. Add this to the app you are auditing, install the devDependencies, start the app, then run the script. `@axe-core/cli --exit` returns non-zero when it finds violations.

```json
{
  "scripts": {
    "a11y:axe": "axe http://127.0.0.1:3000 --exit",
    "a11y:pa11y": "pa11y http://127.0.0.1:3000"
  },
    "devDependencies": {
    "@axe-core/cli": "4.13.0",
    "pa11y": "10.0.0"
  }
}
```

Change the URL to the page you are fixing. Component tests in [frameworks.md](frameworks.md#component-tests) cover what a URL scan cannot see.

## Automated testing in React

Vue and Angular axe examples are in [frameworks.md](frameworks.md#component-tests). Static linting (`eslint-plugin-jsx-a11y`) only catches a subset of issues; add runtime checks against the rendered DOM. Pins checked 2026-10-01.

- **Query by accessibility, not by test id**: Testing Library's role/name queries double as a11y assertions — if `getByRole('button', { name: 'Save' })` can't find it, neither can assistive tech. Prefer `getByRole` / `getByLabelText` over `getByTestId`. `npm i -D @testing-library/react@16.3.3 @testing-library/jest-dom@6.9.1`. jest-dom 7.0.1 peers with Vitest only, so this Jest example stays on 6.9.1.

```tsx
import { render, screen } from '@testing-library/react';

test('save button has an accessible name', () => {
  render(<Toolbar />);
  // Throws if no button is exposed with this accessible name/role.
  expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
});
```

- **Component-level axe (Jest)**: `npm i -D jest-axe@11.0.0`. jest-axe 11 depends on axe-core 4.12.1; the CLI pin above is 4.13.0. Register the matcher or `toHaveNoViolations` is not a function and the test is deleted instead of fixed.

```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('form has no a11y violations', async () => {
  const { container } = render(<SignupForm />);
  expect(await axe(container)).toHaveNoViolations();
});
```

- **Component-level axe (Vitest)**: `vitest-axe@0.1.0`. In the Vitest setup file: `import * as matchers from 'vitest-axe/matchers'` and `expect.extend(matchers)`. TypeScript setups import `vitest-axe/extend-expect` once so the matcher is on the types.
- **End-to-end axe**: run axe against the real running app in E2E, where routing, portals, and focus behave realistically.
  - Cypress: `npm i -D cypress-axe@1.7.0 axe-core@4.13.0` → `cy.injectAxe()` then `cy.checkA11y()`.
  - Playwright: `npm i -D @axe-core/playwright@4.13.0` → `new AxeBuilder({ page }).analyze()` and assert `results.violations` is empty.
- **Scope caveat**: axe finds ~30–50% of issues. Keep manual keyboard + screen-reader checks for focus order, live-region timing, and semantics that automation can't judge.

## React focus & routing

Route-change focus is only in [frameworks.md](frameworks.md#react-routing). Do not add a second snippet here.

Inside one page (a wizard step, not a URL change), focus a heading when that step's key changes. Give it `tabIndex={-1}`. Skip the focus on the first render, or it steals focus on load.

### Focus trap libraries

Don't hand-roll a trap. Pins checked 2026-10-01:

- `react-focus-lock@2.13.7` or `focus-trap-react@12.0.3` for a custom dialog. Prefer `<dialog>` and `showModal()` when you can.
- Primitives that already do roles, keyboard, and focus return: `react-aria@3.52.1`, Radix UI, `@headlessui/react@2.2.10`.
- Don't add `role`, `tabindex`, or `aria-*` that the primitive already sets. Duplicating them announces the control twice.

## Screen reader testing (manual)

Automated tools miss focus order, announcement timing, and whether the name is the one a person can use. After a fix, run this on the changed flow. A full-site pass is only when the user asks for one.

Listen for four things, in this order: **name**, **role**, **state** (expanded, selected, disabled, invalid), **value**. Then do the action and check that either focus moved to the new content or a live region spoke the result. Silence after "Save" is a failure.

| Screen reader | Where | Start | Move | Activate |
|---------------|--------|-------|------|----------|
| NVDA | Windows, browser in browse mode | Launch NVDA | `H` next heading, `B` button, `K` link, `F` form field; `Tab` for focus order | `Enter` |
| JAWS | Windows | Launch JAWS | Same idea: headings, links, form fields, then `Tab` | `Enter` |
| VoiceOver | macOS | Cmd+F5. VO is Control+Option | VO+Right / VO+Left. Rotor: VO+U, then headings or form controls | VO+Space |
| VoiceOver | iOS | Settings → Accessibility → VoiceOver | Swipe right / left | Double-tap |
| TalkBack | Android | Settings → Accessibility → TalkBack | Swipe right / left | Double-tap |
| VoiceView | Amazon Fire OS | Settings → Accessibility → VoiceView Screen Reader | Swipe right / left | Double-tap |

NVDA starts in browse mode on the web. If a widget never reaches forms mode, the keystrokes go to the page instead of the control. VoiceView is a screen reader. It is not speech input. Samsung’s screen reader is **Voice Assistant** (TalkBack-based), not VoiceView. Don’t mix the names up.

Pass when every control in the flow is reachable, the name matches the visible text (2.5.3), state changes are announced, and the result is announced or focused. Fail when a control is silent, an icon button reads "button", or focus stays on a control that unmounted.

### Screen reader corner cases

- **Visually hidden label**: Keep the text in the accessibility tree. Don’t use `display: none` or `visibility: hidden` for text that should be announced.

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

- **Tables**: Use `<th scope="col">` / `scope="row"` or `headers="id-of-th"` on `<td>` for complex tables. Add `<caption>` or `aria-labelledby` so the table has a name.
- **Live region timing**: Set `aria-live` and update content after a short delay if the SR might miss very fast updates. Use `aria-atomic="true"` when the whole region should be re-announced.
- **Iframe**: Always give `<iframe title="Description of content">` or `aria-label` so SR knows what the embedded content is.

## Voice control and VoiceView

- **Voice control** (Windows Voice Access, macOS Voice Control, Dragon) is speech input. The user says the visible label ("Click Submit"). That only works when the accessible name contains the visible text (2.5.3) and two controls don’t share it. Test by speaking the label, not by reading the accessibility tree.
- **VoiceView** (Fire OS) uses the same names, roles, and states as TalkBack. An unlabeled icon is skipped or announced as an unlabeled button. There is no separate VoiceView API. Fix the accessible name and retest with the gestures in the table above.

## Native mobile (brief)

Web patterns above do not transfer as HTML. The goal is the same: name, role, state, focus order, and text that scales.

- **React Native**
  - Name and role: `accessibilityLabel` is the purpose, not the control type. Set `accessibilityRole` and `accessibilityState`.
  - Decorative icons: `accessible={false}` on iOS and `importantForAccessibility="no"` on Android. `accessibilityElementsHidden` hides a whole group.
  - Modal: `accessibilityViewIsModal` on the iOS modal so VoiceOver cannot reach the screen behind it. On Android, set `importantForAccessibility="no-hide-descendants"` on the content the dialog covers.
  - Dynamic type: leave `allowFontScaling` at its default (`true`). Don't fix a height that clips when the system font grows. Test at the largest system size.
  - Test with VoiceOver (iOS) and TalkBack (Android).
- **iOS (Swift/UIKit)**: `accessibilityLabel`, `accessibilityTraits`, `isAccessibilityElement`. Set `accessibilityViewIsModal = true` on a modal. A decorative image is not an accessibility element.
- **Android**: `contentDescription` on meaningful images. `android:importantForAccessibility="no"` on decorative ones. `importantForAccessibility="noHideDescendants"` on the background while a dialog is open. Text size in `sp`, not `dp` or `px`.
- **Guidelines**: iOS HIG (Accessibility) and the Android accessibility guidance. WCAG describes the goal. The APIs above are how a native app meets it.
