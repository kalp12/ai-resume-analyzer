import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_DB_PATH = "resume_index.pkl"

class ResumeVectorDB:
    def __init__(self):
        self.embeddings = SentenceTransformer("all-MiniLM-L6-v2")  
        self.index = None   
        self.resume_texts = []

        if os.path.exists(VECTOR_DB_PATH):
            self._load_index()
        else:
            self._initialize_index()

    def _initialize_index(self):
        self.index = faiss.IndexFlatL2(384)  # 384-dimensional vectors (MiniLM)
        self.resume_texts = []
    
    def _load_index(self):
        with open(VECTOR_DB_PATH, "rb") as f:
            data = pickle.load(f)
        self.index = data["index"]
        self.resume_texts = data["texts"]

    def _save_index(self):
        with open(VECTOR_DB_PATH, "wb") as f:
            pickle.dump({"index": self.index, "texts": self.resume_texts}, f)

    def add_resume(self, text):
        """Embeds and stores resume"""
        vector = self.embeddings.encode([text], convert_to_numpy=True)
        self.index.add(vector)
        self.resume_texts.append(text)
        self._save_index()

    def search_resumes(self, query, top_k=3):
        """Finds relevant resumes"""
        query_vector = self.embeddings.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i in indices[0]:
            if i < len(self.resume_texts):
                results.append(self.resume_texts[i])
        return results
