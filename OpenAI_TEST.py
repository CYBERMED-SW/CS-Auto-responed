import openai
import os
from dotenv import load_dotenv
# OpenAI API 키 설정
openai.api_key = os.getenv("openai_api_key")

try:
    # 모델 목록 가져오기
    response = openai.Model.list()
    print("OpenAI API is working!")
except openai.error.AuthenticationError:
    print("Invalid API Key. Please check your OpenAI API Key.")