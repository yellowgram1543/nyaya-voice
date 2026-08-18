# Nyaya Voice

Nyaya Voice is an AI-powered legal intake assistant that helps consumers describe disputes, collect key facts, and generate a legal notice PDF. It includes a FastAPI backend and a React + Vite frontend.

🌐 Live app: [https://nyaya-voice.vercel.app](https://nyaya-voice.vercel.app)

## Overview

Nyaya Voice is built for pre-litigation consumer complaint workflows:
- conversational intake through a legal assistant
- receipt/image fact extraction
- notice verification and download endpoints
- a B2B risk dashboard for completed notices
- optional WhatsApp webhook flow for chat intake

## Project Structure

```text
nyaya-voice/
├── backend/              # FastAPI app, AI agent flow, drafting + storage logic
│   ├── main.py
│   ├── requirements.txt
│   └── render.yaml
├── frontend/             # React + Vite client
│   ├── src/App.jsx
│   └── package.json
└── README.md
```

## Features

- AI-guided legal intake conversation (`/api/chat`)
- Receipt upload + fact extraction (`/api/upload_receipt`)
- Legal notice PDF generation (`/api/download_notice/{session_id}`)
- Notice authenticity verification (`/api/verify/{session_id}`)
- Corporate risk dashboard endpoints (`/api/b2b/*`)
- WhatsApp webhook integration (`/webhook`)

## Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- npm

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GEMINI_API_KEY=your_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
# Optional for WhatsApp integration:
WHATSAPP_TOKEN=
WHATSAPP_PHONE_ID=
WHATSAPP_VERIFY_TOKEN=
```

Run backend locally:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

By default, frontend API calls target the deployed backend (`https://nyaya-voice-backend.onrender.com`).

## Development

- Frontend app runs at `http://localhost:5173`
- Backend API runs at `http://localhost:8000`
- Frontend scripts:
  - `npm run dev` — start Vite dev server
  - `npm run build` — production build
  - `npm run preview` — preview built app
  - `npm run lint` — lint frontend code

## Deployment

- Frontend: Vercel (`nyaya-voice.vercel.app`)
- Backend: Render (`backend/render.yaml`, `uvicorn main:app`)

## Contributing

Contributions are welcome. Please:
1. open an issue describing the change
2. keep changes focused and well-scoped
3. run relevant checks before submitting a PR
