import os
import time
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def clean_up_old_vectors(vector_store_path, max_age_days=30):
    current_time = time.time()
    for root, dirs, files in os.walk(vector_store_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_age = (current_time - os.path.getmtime(file_path)) / (60 * 60 * 24)
            if file_age > max_age_days:
                os.remove(file_path)
                print(f"Deleted old vector store file: {file_path}")

vector_store_path = "vector_store"
clean_up_old_vectors(vector_store_path, max_age_days=30)
