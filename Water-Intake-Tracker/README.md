# AI Powered Water Intake Tracker

Track how much water you drink each day and get personalised hydration feedback from Google Gemini.

## Project goal

Most people don't drink enough water and don't notice until they feel tired or get a headache. This app makes it easy to:

- **Log** each glass or bottle of water you drink
- **See your progress** towards a daily goal (default 2000 ml)
- **Get AI feedback** on your hydration status, based on your total for the day
- **Review your history** as a table and a day-by-day chart

## Features

| Feature | Where |
|---|---|
| Web dashboard (log intake, progress bar, history chart, AI feedback) | `dashboard.py` (Streamlit) |
| REST API (log intake, get history) | `src/api.py` (FastAPI) |
| AI hydration analysis | `src/agent.py` (LangChain + Gemini) |
| Data storage | `src/database.py` (SQLite, `water_tracker.db`) |
| Logging | `src/logger.py` (writes to `app.log`) |

## Project structure

```
Water Intake Tracker/
├── dashboard.py        # Streamlit web app (main entry point)
├── requirements.txt    # Python dependencies
├── .env                # API keys and settings (not shared, see below)
└── src/
    ├── agent.py        # Gemini hydration agent
    ├── api.py          # FastAPI endpoints
    ├── database.py     # SQLite functions
    └── logger.py       # Log helpers
```

## Prerequisites

- Python 3.12 or newer
- A Google Gemini API key. Get one free at [Google AI Studio](https://aistudio.google.com) → **Get API key**.

## Setup

Run all commands from the project root folder (`Water Intake Tracker/`).

**1. Create and activate a virtual environment**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**2. Install dependencies**

```powershell
python -m pip install -r requirements.txt
python -m pip install langchain-google-genai
```

> Use `python -m pip` instead of `pip`. Some company laptops block `pip.exe`, `streamlit.exe` and `uvicorn.exe`, but `python -m ...` still works.

**3. Create a `.env` file** in the project root:

```
GOOGLE_API_KEY=your-gemini-api-key-here

# Optional: change the Gemini model (default: gemini-3.5-flash-lite)
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never share or commit this file. It contains your secret key.

## How to run

### Option 1: Web dashboard (recommended)

```powershell
python -m streamlit run dashboard.py
```

Your browser opens at http://localhost:8501. The first load can take a few seconds.

1. Click **Start Tracking**
2. In the sidebar, enter your **User ID**, the **Water Intake (ml)** you just drank, and your **Daily Goal**
3. Click **Submit** to save it and get AI feedback
4. Scroll down to see your history and chart

### Option 2: REST API

```powershell
python -m uvicorn src.api:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints in your browser:

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/log-intake` | Saves an intake and returns AI feedback. Body: `{"user_id": "user_03", "intake_ml": 250}` |
| `GET` | `/history/{user_id}` | Returns all saved intakes for a user |

### Option 3: Test the AI agent only

```powershell
python src/agent.py
```

Prints a hydration analysis for a sample intake of 1500 ml.


## Tech stack

Python · Streamlit · FastAPI · LangChain · Google Gemini · SQLite · pandas
