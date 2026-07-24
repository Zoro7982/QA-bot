from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os
import io

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(docs_url="/", redoc_url="/redoc")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    pdf = PdfReader(io.BytesIO(contents))
    
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    
    return {
        "filename": file.filename,
        "pages": len(pdf.pages),
        "text_preview": text[:500]
    }

@app.post("/ask")
async def ask_question(file: UploadFile = File(...), question: str = "summarize this document"):
    contents = await file.read()
    pdf = PdfReader(io.BytesIO(contents))
    
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on documents."
            },
            {
                "role": "user",
                "content": f"Based on this document, answer the question.\n\nDocument:\n{text[:10000]}\n\nQuestion: {question}"
            }
        ]
    )
@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):

    contents = await file.read()

    pdf = PdfReader(io.BytesIO(contents))

    text = ""
    for page in pdf.pages:
        text += page.extract_text()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this in one paragraph:\n{text[:10000]}"
            }
        ]
    )

    return {
        "summary":response.choices[0].message.content
    }
    
    return {
        "question": question,
        "answer": response.choices[0].message.content,
        "pages_read": len(pdf.pages)
    }