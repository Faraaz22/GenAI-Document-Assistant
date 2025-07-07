import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


class QASystem:
    def __init__(self):
        self.chunks = []
        self.embeddings = None
        self.index = None

    def index_chunks(self, chunks):
       self.chunks = chunks
       # Convert all chunks into vector representations
       self.embeddings = model.encode(chunks)
       # distance search
       self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
    # faiss now holds all vectorized chunks and can search through them quickl
       self.index.add(np.array(self.embeddings))

    def retrieve(self, question, top_k=3):
    # Turn the user's question into a vector using the same model.
       q_vec = model.encode([question])
    # faiss.index.search finds the top_k closest vectors to the question vector.
       _, indices = self.index.search(np.array(q_vec), top_k)
    # Use the indices to fetch and return the corresponding text chunks.
       return [self.chunks[i] for i in indices[0]]
    
qa = QASystem()

docs = [
    "The Eiffel Tower is in Paris.",
    "Cats are mammals.",
    "The capital of France is Paris.",
]

qa.index_chunks(docs)

query = "Where is the Eiffel Tower located?"
answers = qa.retrieve(query)

print(answers)


