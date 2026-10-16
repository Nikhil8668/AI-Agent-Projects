# AI-Powered Book Summary Generator

Upload a book (PDF) through a simple web page and get an AI-generated summary saved to Google Drive.

## How it works

1. **Flask web app** – you upload a PDF; the app saves it to a Google Drive folder (OAuth, your own Drive).
2. **n8n workflow** – a Google Drive trigger detects the new file, downloads it, extracts the text, summarizes it with **Google Gemini** (Basic LLM Chain), and uploads the summary back to Drive.

```
Web app ──upload PDF──▶ Google Drive ──trigger──▶ n8n ──▶ Gemini ──▶ summary file in Drive
```

## Tech stack

- Python, Flask
- Google Drive API (OAuth 2.0)
- n8n (workflow automation)
- Google Gemini

## Setup

1. Install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```
2. In Google Cloud Console, enable the **Google Drive API** and create an **OAuth client ID (Desktop app)**. Download it as `oauth_client.json` into the project folder.
3. Copy `.env.example` to `.env` and fill in your Drive folder ID.
4. Run the app:
   ```bash
   python app.py
   ```
   Open http://127.0.0.1:5000. The first upload opens a browser for Google login and saves `token.json`.
5. In n8n, build (or import) the workflow: Google Drive Trigger (File Created, same folder) → Download file → Extract From PDF → Basic LLM Chain + Google Gemini Chat Model → Upload file. Make sure the workflow is **published/active**.

> Tip: have n8n upload summaries to a **different folder** than the one it watches, to avoid re-triggering itself.
