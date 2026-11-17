# LPU Timetable Assistant — Streamlit

A Streamlit web-app version of the supplied Gemini chatbot.

## 1. Requirements
- Python 3.9 or newer
- A Gemini API key

## 2. Install dependencies
Open a terminal in this project folder and run:

```bash
pip install -r requirements.txt
```

## 3. Add your Gemini API key securely

Create `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "YOUR_NEW_GEMINI_API_KEY"
```

Do not upload or share `secrets.toml`. It is excluded from this ZIP through
`.gitignore`.

Alternatively, set the `GEMINI_API_KEY` environment variable.

## 4. Run the app

```bash
streamlit run app.py
```

Streamlit will display a local address, usually http://localhost:8501.

## 5. Deploy on Streamlit Community Cloud
1. Upload the project files (except `secrets.toml`) to a GitHub repository.
2. Create a new app on Streamlit Community Cloud and select `app.py`.
3. Open the app's Settings / Secrets section.
4. Add `GEMINI_API_KEY = "your-key"` to Secrets.
5. Deploy the app.

## Features
- Chat-style interface
- Gemini 2.5 Flash responses
- Uses the supplied LPU knowledge manual
- Clear chat button
- Type `exit` to close the chat session
- API key is read from Streamlit secrets or an environment variable

## Important
The timetable is the static data supplied in the original code. Update the
`MANUAL` section in `app.py` whenever your timetable changes. The chatbot
does not access LPU UMS or live university timetable records.
