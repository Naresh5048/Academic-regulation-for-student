# Campus Notice Agent - LBRCE

A RAG-based AI agent to help students retrieve information from campus notices (PDFs).

## Tech Stack
- **Frontend**: React, Tailwind CSS, Vite, Axios, Lucide React
- **Backend**: FastAPI, LangChain, Google Gemini 1.5 Flash
- **Database**: ChromaDB (Vector Store)

## Getting Started

### 1. Prerequisites
- Python 3.9+
- Node.js & npm (for frontend)
- Google API Key (for Gemini)

### 2. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Google API Key:
   ```env
   GOOGLE_API_KEY=your_actual_key_here
   ```
4. Place your campus PDFs in the `backend/data` folder.
5. Start the server:
   ```bash
   python main.py
   ```

### 3. Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

### 4. Usage
- Open the frontend in your browser (usually `http://localhost:5173`).
- Click **"Sync Now"** in the sidebar to index your PDFs.
- Start chatting with the **Official LBRCE Assistant**.

---

**Note**: If a year is missing in a PDF, the AI assumes the current year is **2026**.
