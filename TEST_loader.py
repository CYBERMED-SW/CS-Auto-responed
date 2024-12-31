from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.schema import document
import os

load_dotenv()
embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("openai_api_key"))

FILE_PATH = "C:\Users\cybermed\Downloads\SPRI_AI_Brief_2023년12월호_F.pdf"

loader = PyPDFLoader(FILE_PATH)
docs = loader.load()
docs: list[document] = loader.load()

print(f"Number of documents loaded: {len(docs)}")


if not docs:
    print("No documents loaded. Check the PDF file path or format.")
else:
    print(f"First 300 characters of page 10: {docs[10].page_content[:300]}")

def show_metadata(docs):
    if docs and hasattr(docs[0], 'metadata') and docs[0].metadata:
        print("[metadata]")
        print(list(docs[0].metadata.keys()))
        print("\n[examples]")
        max_key_length = max(len(k) for k in docs[0].metadata.keys())
        for k, v in docs[0].metadata.items():
            print(f"{k:<{max_key_length}} : {v}")
    else:
        print("No metadata found in the loaded documents.")

show_metadata(docs)


file_path = "C:\Users\cybermed\Downloads\SPRI_AI_Brief_2023년12월호_F.pdf"

reader = PdfReader(file_path)

if reader.metadata:
    print("[PDF Metadata]")
    for key, value in reader.metadata.items():
        print(f"{key}: {value}")
else:
    print("No metadata found in the PDF.")



# 추가해야할 사항
# retreiver를 이용해서 RAG로 정형화된 데이터들을 text화시켜서 학습하게 만들어야함
# def vectordb initialize제작 RAG가 학습하기 위한 함수
# similarity_search > agent에서도 사용 유사도를 이용해서 vectorDB에서 데이터 parsing (오타같은 부류)
# request에 의한 순차처리 방향 고려


