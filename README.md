# QA Bot — AI-Powered PDF Question Answering

Upload any PDF and ask questions about it. 
Get instant AI-powered answers.

## Tech Stack
- FastAPI
- Groq LLM (llama-3.3-70b)
- pypdf
- Python 3.12

## Endpoints
- `GET /` — Health check
- `POST /upload` — Upload PDF and extract text
- `POST /ask` — Upload PDF and ask a question

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
