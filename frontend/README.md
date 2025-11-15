# Frontend (Clooney Asana Clone)

React + Tailwind (Vite) frontend that approximates Asana's Home, Projects and Tasks UI.

## Setup

```bash
cd frontend
npm install
```

Run dev server:

```bash
npm run dev
```

Run visual + CSS tests (requires dev server running on port 5173):

```bash
npm run dev
# in another terminal
npm run test:e2e
```

The tests use Playwright screenshots with masked dynamic elements (`data-dynamic` attributes) and explicit CSS assertions for the primary CTA color (`#3a258e`).
