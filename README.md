# GenAI Document Assistant

A local AI-powered assistant for document understanding, Q&A, and logic-based challenge questions using Llama 3.2 (Ollama), FAISS, and FastAPI/Gradio.

Link to the Postman Dump- https://web.postman.co/workspace/My-Workspace~aed8e94b-bbcd-41f4-8f4e-dcdf06fd6342/collection/36223447-cbc292e3-da12-4574-a045-1039b993068e?action=share&source=copy-link&creator=36223447

## Features
- **Upload** PDF or TXT documents
- **Auto-summary** (≤150 words) using Llama 3.2
- **Ask Anything**: Free-form Q&A grounded in the document
- **Challenge Me**: Generates 3 logic-based questions, lets you answer, and evaluates your answers with justification
- **All answers are justified with references to the document**

---

## Setup Instructions

### 1. Clone the repository
```
git clone <your-repo-url>
cd doc_assistant
```

### 2. Create and activate a Python virtual environment
On **Windows**:
```
python -m venv venv
venv\Scripts\activate
```
On **Linux/Mac**:
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Install and run Ollama
- Download and install Ollama: https://ollama.com/download
- Pull and run the Llama 3.2 model:
```
ollama pull llama3
ollama run llama3
```

### 5. Set up MySQL
- Install MySQL and start the server
- Create a database:
```
CREATE DATABASE doc_assistant;
```
- Update your MySQL username/password in `database.py` if needed.
- Create tables:
```
python create_tables.py
```

### 6. Start the backend (FastAPI)
```
uvicorn app:app --reload
```
- The API docs will be at http://127.0.0.1:8000/docs

### 7. Start the frontend (Gradio)
```
python frontend.py
```
- The UI will be at http://127.0.0.1:7860

---

## Usage
1. Upload a PDF or TXT file.
2. View the summary and document ID.
3. Use "Ask Anything" for Q&A.
4. Use "Challenge Me" to get logic questions, answer, and evaluate.

---

## License
MIT
