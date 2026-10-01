# Framework patterns

Shared rules stay in [SKILL.md](SKILL.md): native `<button>` vs `<a>`, no `<div onClick>`, an accessible name on icon-only controls, and `<dialog>` (or a real focus trap) for modals. This file is only how React, Vue, and Angular implement those rules. Do not copy the full checklist into a framework.

Runtime axe examples for React also live in [reference.md](reference.md#automated-testing-in-react).

## React

### Labels and IDs

`useId()` (React 18+) is stable across server and client. Don’t build ids from `Math.random()` or the array index.

```tsx
const id = useId();
return (
  <>
    <label htmlFor={id}>Email</label>
    <input id={id} type="email" autoComplete="email" />
  </>
);
```

### Buttons vs links

```tsx
<button type="button" onClick={onDelete}>Delete</button>
<a href="/settings">Settings</a>
```

`type="button"` matters inside a `<form>`, or the control submits. A `<div onClick>` is not a button.

### Modals

Prefer `<dialog>` and `showModal()`. If the dialog must render at the document root, `createPortal` does not move focus or trap it for you. Use `react-focus-lock` or `focus-trap-react` (versions in [reference.md](reference.md#focus-trap-libraries)), or a primitive from React Aria, Radix, or Headless UI. Don’t add a second `role` on top of theirs.

### React routing

One `<main id="main" tabIndex={-1}>` lives in the app shell, with the skip link. A page component does not render another main. Vue and Angular follow the same rule: [Vue routing](#vue-routing), [Angular routing](#angular-routing).

```tsx
function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <a href="#main">Skip to main content</a>
      <main id="main" tabIndex={-1}>{children}</main>
    </>
  );
}
```

Move focus after a client navigation, not on the first load. `useLocation` comes from `react-router`. Checked 2026-10-01: `react-router@8.4.0` needs React >=19.2.7. The same call exists on 7.x.

```tsx
function FocusMainOnNavigate() {
  const { pathname } = useLocation();
  const isFirst = useRef(true);
  useEffect(() => {
    if (isFirst.current) {
      isFirst.current = false;
      return;
    }
    document.getElementById('main')?.focus();
  }, [pathname]);
  return null;
}
```

Put `FocusMainOnNavigate` in the shell. The page sets `document.title`. `useEffect` runs after the new route commits. Next.js App Router sets the title with `metadata` / `generateMetadata`, and the same focus helper can read `usePathname()` from `next/navigation`. Pages Router sets the title with `next/head`.

## Vue

### Labels and IDs

```vue
<script setup>
import { useId } from 'vue';
const id = useId();
</script>
<template>
  <label :for="id">Email</label>
  <input :id="id" type="email" autocomplete="email" />
</template>
```

`useId` needs Vue 3.5+. On older Vue 3, one `ref` created when the component is set up is enough. Don’t use the `v-for` index.

### Buttons vs links

```vue
<button type="button" @click="onDelete">Delete</button>
<RouterLink to="/settings">Settings</RouterLink>
```

Use a native `<button>`, not `<div @click>`.

### Modals

Render with `<Teleport to="body">`. Teleport does not trap focus. Put a `<dialog>` inside it and call `showModal()`, or use the focus trap from the component library you already ship (Headless UI, PrimeVue, Vuetify).

### Vue routing

`<main id="main" tabindex="-1">` is in the shell once, not in each view. Skip the first navigation so the load does not steal focus. `nextTick` waits until the new view is in the DOM.

```js
let skipFirst = true;
router.afterEach((to) => {
  if (skipFirst) {
    skipFirst = false;
    return;
  }
  document.title = String(to.meta.title ?? document.title);
  nextTick(() => document.getElementById('main')?.focus());
});
```

## Angular

### Labels and IDs

```html
<label [attr.for]="emailId">Email</label>
<input [id]="emailId" type="email" autocomplete="email" />
```

```ts
export class EmailFieldComponent {
  private static nextId = 0;
  readonly emailId = `email-${EmailFieldComponent.nextId++}`;
}
```

Bind `[attr.for]` and `[id]` to that field. The DOM property is `htmlFor`, so `[attr.for]` is the reliable binding. Don’t interpolate `$index`. A static counter can mismatch server and client markup. When the component is server-rendered, pass the id in instead of incrementing one.

### Buttons vs links

```html
<button type="button" (click)="onDelete()">Delete</button>
<a routerLink="/settings">Settings</a>
```

`(click)` on a `<div>` is not a button. On a native `<button>`, set `type="button"` when it should not submit.

### Modals

Use Angular CDK or Angular Material rather than a hand-rolled trap.

- `cdkTrapFocus` from `@angular/cdk/a11y` keeps Tab inside the panel.
- `Dialog` from `@angular/cdk/dialog`, or `MatDialog` from Angular Material, already traps focus, restores it, and sets the dialog role. Open it with the service. Don’t also set `role="dialog"` on the template.
- `@angular/cdk` pin checked 2026-10-01: `22.2.1`.

### Angular routing

`<main id="main" tabindex="-1">` is in the shell once, outside each routed component. `NavigationEnd` can fire before the new view is in the DOM, so focus on the next turn. `skip(1)` leaves the first load alone.

```ts
import { filter, skip } from 'rxjs';
import { NavigationEnd, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

// `router` and `title` are injected on the component
this.router.events.pipe(
  filter((event): event is NavigationEnd => event instanceof NavigationEnd),
  skip(1),
).subscribe(() => {
  this.title.setTitle('Inbox');
  setTimeout(() => document.getElementById('main')?.focus());
});
```

The skip link points at that same main. Set the title from the route data instead of a hard-coded string when the route carries one.

## Component tests

Lint is not a test. After a fix, re-run the framework plugin and one axe test on the rendered component. Query by role and name. If `getByRole` cannot find it, assistive tech cannot either.

| Stack | Lint | Test |
|-------|------|------|
| React | `eslint-plugin-jsx-a11y@6.10.2` | `jest-axe` or `vitest-axe` + Testing Library `getByRole` |
| Vue | `eslint-plugin-vuejs-accessibility@2.6.0` | `vitest-axe` + `@testing-library/vue` `getByRole` |
| Angular | `@angular-eslint/eslint-plugin-template` accessibility rules | `jest-axe` + Angular Testing Library `getByRole` |

Angular template rules to turn on: `alt-text`, `click-events-have-key-events`, `interactive-supports-focus`, `label-has-associated-control`, `valid-aria`. Package pin checked 2026-10-01: `@angular-eslint/eslint-plugin-template@22.5.0`.

Vue example (the React axe example is in reference.md):

```ts
import { expect, test } from 'vitest';
import { render, screen } from '@testing-library/vue';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import EmailField from './EmailField.vue';

expect.extend(matchers);

test('email field is named and has no axe violations', async () => {
  const { container } = render(EmailField);
  expect(screen.getByRole('textbox', { name: /email/i })).toBeTruthy();
  expect(await axe(container)).toHaveNoViolations();
});
```

`expect.extend` belongs in the Vitest setup file in a real project. It is inline here so a pasted test does not call a matcher that was never registered. For TypeScript, also import `vitest-axe/extend-expect` once.

Angular example:

```ts
import { render, screen } from '@testing-library/angular';
import { axe, toHaveNoViolations } from 'jest-axe';
import { EmailFieldComponent } from './email-field.component';

expect.extend(toHaveNoViolations);

it('email field is named and has no axe violations', async () => {
  const { container } = await render(EmailFieldComponent);
  expect(screen.getByRole('textbox', { name: /email/i })).toBeTruthy();
  expect(await axe(container)).toHaveNoViolations();
});
```

Verify loop: audit → fix → ESLint a11y plugin → component axe test → keyboard check on the same flow.
