from fastapi import FastAPI, UploadFile, File, Body
import os
from utils import parse_pdf, parse_txt
from summarize import summarize_text
from qa import QASystem
from database import SessionLocal
from models import Document, QuestionLog
import requests

app = FastAPI()
qa = QASystem()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded document text and chunk embeddings for each document
uploaded_docs = {}  # doc_id: {"text": ..., "chunks": [...], "embeddings": ...}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Parse document
    if file.filename.lower().endswith(".pdf"):
        text = parse_pdf(filepath)
    else:
        text = parse_txt(filepath)

    # Summarize document (≤150 words)
    summary = summarize_text(text)

    # Chunk for QA
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    qa.index_chunks(chunks)

    db = SessionLocal()
    doc = Document(filename=file.filename, summary=summary)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Store text and chunks for challenge and Q&A
    uploaded_docs[doc.id] = {"text": text, "chunks": chunks}

    return {"document_id": doc.id, "summary": summary}

# Helper to generate logic-based questions using llama3.2
def generate_logic_questions(text, model="llama3.2"):
    prompt = f"Generate 3 logic-based or comprehension-focused questions based on the following document. Return only the questions, numbered:\n\n{text[:3000]}"
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    questions = response.json()["response"].strip().split("\n")
    # Remove empty lines and keep only non-empty questions
    return [q.strip() for q in questions if q.strip()]

# Helper to evaluate user answers using llama3.2
def evaluate_answer(question, user_answer, doc_text, model="llama3.2"):
    prompt = f"Evaluate the following answer to the question, using the document below. State if the answer is correct, and provide a brief justification with a reference to the document (e.g., 'This is supported by paragraph 3...').\n\nQuestion: {question}\nUser Answer: {user_answer}\nDocument: {doc_text[:3000]}"
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

@app.post("/challenge/")
def challenge(document_id: int = Body(...), user_answers: list = Body(default=None)):
    """
    If user_answers is None, generate and return 3 logic-based questions.
    If user_answers is provided, evaluate and return feedback for each answer.
    """
    doc_info = uploaded_docs.get(document_id)
    if not doc_info:
        return {"error": "Document not found. Please upload first."}
    doc_text = doc_info["text"]
    if not user_answers:
        questions = generate_logic_questions(doc_text)
        return {"questions": questions[:3]}
    else:
        # Evaluate each answer
        questions = generate_logic_questions(doc_text)
        feedback = []
        for q, user_a in zip(questions[:3], user_answers):
            eval_result = evaluate_answer(q, user_a, doc_text)
            feedback.append({"question": q, "user_answer": user_a, "evaluation": eval_result})
        return {"feedback": feedback}

@app.post("/ask/")
def ask(document_id: int = Body(...), question: str = Body(...)):
    """
    Free-form Q&A: Uses LLM to answer with context and justification from the document.
    """
    doc_info = uploaded_docs.get(document_id)
    if not doc_info:
        return {"error": "Document not found. Please upload first."}
    doc_text = doc_info["text"]
    # Use LLM to answer and justify
    prompt = f"Answer the following question based only on the document below. Provide a concise answer and a brief justification with a reference to the document (e.g., 'This is supported by paragraph 3...').\n\nQuestion: {question}\nDocument: {doc_text[:3000]}"
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    result = response.json()["response"].strip()
    db = SessionLocal()
    log = QuestionLog(document_id=document_id, question=question, answer=result, justification=result)
    db.add(log)
    db.commit()
    return {"answer": result}
