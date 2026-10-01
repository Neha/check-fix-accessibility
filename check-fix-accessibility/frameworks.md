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

Prefer `<dialog>` and `showModal()`. If the dialog must render at the document root, `createPortal` does not move focus or trap it for you. Use `react-focus-lock` or `focus-trap-react` (versions in [reference.md](reference.md#react-focus--routing)), or a primitive from React Aria, Radix, or Headless UI. Don’t add a second `role` on top of theirs.

### React routing

Client navigation does not reset focus or the title. Keep a skip link that targets `<main id="main">`, and move focus there (or announce the new title). Vue and Angular are the same idea: [Vue routing](#vue-routing), [Angular routing](#angular-routing).

React Router:

```tsx
const title = 'Inbox';
const { pathname } = useLocation();
const mainRef = useRef<HTMLElement>(null);
useEffect(() => {
  document.title = title;
  mainRef.current?.focus();
}, [pathname, title]);
return <main id="main" ref={mainRef} tabIndex={-1}>{children}</main>;
```

Next.js App Router: set the title with the `metadata` / `generateMetadata` export. In a client component, focus `<main>` from `usePathname()` in `next/navigation`. Pages Router: set the title with `next/head`.

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

```js
router.afterEach((to) => {
  document.title = to.meta.title ?? 'App';
  nextTick(() => document.getElementById('main')?.focus());
});
```

`<main id="main" tabindex="-1">` is the skip-link target. `nextTick` waits until the new view is in the DOM.

## Angular

### Labels and IDs

```html
<label [attr.for]="emailId">Email</label>
<input [id]="emailId" type="email" autocomplete="email" />
```

```ts
readonly emailId = 'email-field';
```

Bind `[attr.for]` and `[id]` to the same field, set when the class is constructed. The DOM property is `htmlFor`, so `[attr.for]` is the reliable binding. If a page can show two of the component, append a counter you own. Don’t interpolate `$index`.

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

```ts
import { filter } from 'rxjs';
import { NavigationEnd, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

// `router` and `title` are injected on the component
this.router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
  this.title.setTitle('Inbox');
  document.getElementById('main')?.focus();
});
```

`NavigationEnd` fires after the `router-outlet` has rendered. The skip link points at `<main id="main" tabindex="-1">`.

## Component tests

Lint is not a test. After a fix, re-run the framework plugin and one axe test on the rendered component. Query by role and name. If `getByRole` cannot find it, assistive tech cannot either.

| Stack | Lint | Test |
|-------|------|------|
| React | `eslint-plugin-jsx-a11y@6.10.2` | `jest-axe` or `vitest-axe` + Testing Library `getByRole` |
| Vue | `eslint-plugin-vuejs-accessibility@2.5.0` | `vitest-axe` + `@testing-library/vue` `getByRole` |
| Angular | `@angular-eslint/eslint-plugin-template` accessibility rules | `jest-axe` + Angular Testing Library `getByRole` |

Angular template rules to turn on: `alt-text`, `click-events-have-key-events`, `interactive-supports-focus`, `label-has-associated-control`, `valid-aria`. Package pin checked 2026-10-01: `@angular-eslint/eslint-plugin-template@22.5.0`.

Vue example (the React axe example is in reference.md):

```ts
import { render, screen } from '@testing-library/vue';
import { axe } from 'vitest-axe';
import EmailField from './EmailField.vue';

test('email field is named and has no axe violations', async () => {
  const { container } = render(EmailField);
  expect(screen.getByRole('textbox', { name: /email/i })).toBeTruthy();
  expect(await axe(container)).toHaveNoViolations();
});
```

Angular example:

```ts
import { render, screen } from '@testing-library/angular';
import { axe } from 'jest-axe';
import { EmailFieldComponent } from './email-field.component';

it('email field is named and has no axe violations', async () => {
  const { container } = await render(EmailFieldComponent);
  expect(screen.getByRole('textbox', { name: /email/i })).toBeTruthy();
  expect(await axe(container)).toHaveNoViolations();
});
```

Verify loop: audit → fix → ESLint a11y plugin → component axe test → keyboard check on the same flow.
