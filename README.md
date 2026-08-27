# Nyaya-Voice ⚖️🎙️

Nyaya-Voice is an AI-driven, pro-bono legal intake agent designed to democratize access to justice in India. It acts as an automated paralegal that can listen to consumer complaints via native Indic voice inputs, perform intelligent gap-analysis using a LangGraph reasoning engine, and autonomously draft formal legal notices (complete with statutory citations and precedents) ready for court submission.

## 🚀 Features
- **Voice-First Indic Intake**: Native voice recording in the browser, processed via Sarvam AI's Saaras v3 for highly accurate Indic-to-English translation.
- **Agentic Gap-Analysis**: Built with LangGraph and Gemini, the agent maintains state across conversations and surgically extracts exactly 9 mandatory facts required for a consumer complaint.
- **Multimodal Evidence Processing**: OCR capabilities using Gemini Vision to instantly extract transaction dates, merchant names, and dispute amounts from uploaded receipts.
- **Retrieval-Augmented Generation (RAG)**: Automatically searches a ChromaDB vector store of Indian Consumer Protection Act (2019) statutes and precedents to ground the generated legal notice.
- **Automated Legal Drafting**: Generates a strictly-formatted, downloadable PDF court notice using `reportlab`.
- **Resilient Architecture**: Built with FastAPI and a hybrid state persistence model (Supabase with an automated local SQLite fallback).

## 🛠️ Tech Stack
- **Frontend**: React 19, Vite, Tailwind CSS
- **Backend**: FastAPI, Python 3.13, SQLite/Supabase
- **AI & NLP**: LangGraph, Google Gemini (Flash-latest), Sarvam AI (STT)
- **Vector Search**: ChromaDB

## 💻 Local Setup
1. Clone the repository and install backend dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .\.venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
   ```
2. Set up environment variables by copying `.env.example` to `.env` and adding your `GEMINI_API_KEY` and `SARVAM_API_KEY`.
3. Run the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
4. Run the frontend server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
