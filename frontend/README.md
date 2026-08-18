# Nyaya Voice Frontend

React + Vite frontend for Nyaya Voice. It provides:
- consumer legal intake chat UI
- notice verification page (`/verify/:sessionId`)
- B2B dashboard view (`/b2b`)

## Scripts

```bash
npm install
npm run dev      # local dev server
npm run build    # production build
npm run preview  # preview production build
npm run lint     # eslint
```

## Backend Dependency

The frontend currently calls the hosted backend directly:
- `https://nyaya-voice-backend.onrender.com`

If you want to run fully local development, update API URLs in:
- `src/App.jsx`
- `src/VerifyPage.jsx`
- `src/B2BDashboard.jsx`

## Notes

- Main repository documentation: `../README.md`
- App entrypoint: `src/main.jsx`
