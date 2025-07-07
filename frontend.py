import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

def upload_file(file):
    if file is None:
        return "No file uploaded.", None
    # file is a path-like object (str or NamedString)
    file_path = file.name if hasattr(file, "name") else file
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        response = requests.post(f"{API_URL}/upload/", files=files)
    if response.status_code == 200:
        data = response.json()
        return f"Summary:\n{data['summary']}", data['document_id']
    else:
        return f"Upload failed: {response.text}", None

def ask_anything(document_id, question):
    payload = {"document_id": int(document_id), "question": question}
    response = requests.post(f"{API_URL}/ask/", json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("answer", "No answer returned.")
    else:
        return f"Error: {response.text}"

challenge_questions = {}

def get_challenge_questions(document_id):
    response = requests.post(f"{API_URL}/challenge/", json={"document_id": int(document_id)})
    if response.status_code != 200:
        return ["", "", "", "Error fetching questions."]
    questions = response.json().get("questions", [])
    challenge_questions[str(document_id)] = questions
    # Pad to always return 3
    while len(questions) < 3:
        questions.append("")
    return [questions[0], questions[1], questions[2], "Questions loaded. Enter your answers and click Evaluate."]

def evaluate_challenge(document_id, a1, a2, a3):
    questions = challenge_questions.get(str(document_id), [])
    if not questions or len(questions) < 3:
        return "Please fetch questions first."
    answers = [a1, a2, a3]
    payload = {"document_id": int(document_id), "user_answers": answers}
    response = requests.post(f"{API_URL}/challenge/", json=payload)
    if response.status_code == 200:
        feedback = response.json().get("feedback", [])
        return "\n\n".join([f"Q: {f['question']}\nYour answer: {f['user_answer']}\nEvaluation: {f['evaluation']}" for f in feedback])
    else:
        return f"Error: {response.text}"

def gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# GenAI Document Assistant\nUpload a PDF or TXT, get a summary, ask questions, or try 'Challenge Me' mode!")
        with gr.Row():
            file = gr.File(label="Upload PDF or TXT")
            upload_btn = gr.Button("Upload")
        upload_output = gr.Textbox(label="Summary")
        doc_id_box = gr.Textbox(label="Document ID ")
        upload_btn.click(upload_file, inputs=[file], outputs=[upload_output, doc_id_box])

        gr.Markdown("## Ask Anything")
        question = gr.Textbox(label="Your Question")
        ask_btn = gr.Button("Ask")
        answer_box = gr.Textbox(label="Answer")
        ask_btn.click(ask_anything, inputs=[doc_id_box, question], outputs=answer_box)

        gr.Markdown("## Challenge Me")
        with gr.Row():
            get_q_btn = gr.Button("Get Questions")
            q1 = gr.Textbox(label="Question 1", interactive=False)
            q2 = gr.Textbox(label="Question 2", interactive=False)
            q3 = gr.Textbox(label="Question 3", interactive=False)
        get_q_status = gr.Textbox(label="Status", interactive=False)
        get_q_btn.click(get_challenge_questions, inputs=[doc_id_box], outputs=[q1, q2, q3, get_q_status])

        answer1 = gr.Textbox(label="Answer 1")
        answer2 = gr.Textbox(label="Answer 2")
        answer3 = gr.Textbox(label="Answer 3")
        eval_btn = gr.Button("Evaluate Answers")
        challenge_output = gr.Textbox(label="Challenge Evaluation Result")
        eval_btn.click(evaluate_challenge, inputs=[doc_id_box, answer1, answer2, answer3], outputs=challenge_output)
    return demo

if __name__ == "__main__":
    gradio_ui().launch()
