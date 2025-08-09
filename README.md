# ✅ Compliance & Regulatory Testing Assistant Chatbot

A Streamlit-based assistant for BCBS 239, regulatory testing, and workpaper drafting. Ready to deploy on **Streamlit Cloud** for a public, shareable link.

## Features
- 🧭 **Risk Assessment** generator (inherent vs residual, RCM alignment)
- 🔍 **Test Script** builder with BCBS 239 mapping
- 📄 **Workpaper** templates (no fake results or audit opinions)
- 📊 **RCM** generator + sampling helper
- 📦 Export to `.md` and `.docx`
- 🔑 Optional LLM drafting via OpenAI (fallback works without a key)

## Quickstart (Local)
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here  # optional
streamlit run app.py
```

## Deploy (Streamlit Cloud — Free)
1. Push this folder to a GitHub repo.
2. Go to https://share.streamlit.io/ → **New app** → connect your repo and select `app.py`
3. (Optional) Add a secret `OPENAI_API_KEY` in **Settings → Secrets**
4. Click **Deploy**. You’ll get a public URL you can share.

## Deploy (Docker)
```bash
# Build
docker build -t compliance-assistant .
# Run
docker run -p 8501:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY compliance-assistant
# Open http://localhost:8501
```

## Project Structure
```
app.py
backend/
  bcbs239.py
  prompts.py
  generators.py
  sampling.py
  rcm.py
  export.py
  storage.py
assets/templates/
  workpaper.md
.streamlit/config.toml
requirements.txt
README.md
```

## Notes & Restrictions
- ❌ Do not fabricate sample results/findings.
- ❌ No legal advice. Provide operational/regulatory guidance only.
- ✅ Use BCBS 239 alignment and independent verification steps.
- ✅ Use risk-based sampling and clear evidence expectations.

---
