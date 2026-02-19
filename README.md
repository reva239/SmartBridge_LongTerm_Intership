# Flavour Fusion – AI Recipe Blogging

Flavour Fusion is a Streamlit web app that generates detailed recipe blog posts using Google Gemini AI.
You provide a recipe topic, optional cuisine type, and word count, and the app creates a complete recipe article with ingredients, steps, tips, serving ideas, nutrition notes, and storage instructions.

## Project Structure

```text
sb_internship/
├── Document/
├── Project Files/
│   ├── app.py
│   ├── requirements.txt
│   ├── =1.28.0
│   ├── .env
│   └── .venv/
└── Video/
```

## Main Files

- `Project Files/app.py` – Streamlit application logic and UI.
- `Project Files/requirements.txt` – Python dependencies.
- `Project Files/.env` – Environment variables (store API keys here).

## Features

- AI-powered recipe blog generation via `gemini-2.5-flash`
- Configurable topic, cuisine type, and word count
- Clean Streamlit UI with styled sections
- Random food/programming joke before generation
- Download generated recipe as a `.txt` file
- In-session recipe history storage

## Requirements

- Python 3.10+ (recommended)
- A valid Google Gemini API key

## Setup

1. Go to the project folder:
   ```bash
   cd "Project Files"
   ```

2. Create and activate a virtual environment (if not already created):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your API key to `.env`:
   ```env
   GOOGLE_GEMINI_API_KEY=your_api_key_here
   ```

## Run the App

From inside `Project Files`:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Notes

- If `GOOGLE_GEMINI_API_KEY` is missing, the app stops and shows an error.
- Recipe history is stored in Streamlit session state and resets when the session ends.
