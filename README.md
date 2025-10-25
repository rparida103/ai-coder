# ai-coder

Modular multi-agent autonomous coding system (LangGraph + OpenAI + Streamlit) with a simple web UI.

Frontend: Streamlit  
Backend: LangGraph agents (dev lead, developer, test engineer, deployer)

## Quick start (local)

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Create virtualenv & install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt