import openai
import smtplib
import imaplib
import email
from dotenv import load_dotenv
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
import os
import logging

load_dotenv()
openai_api_key = os.getenv("openai_api_key")
if not openai_api_key:
    raise ValueError("API KEY ERROR.")

embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("openai_api_key"))

vector_db_path = "vector_store"
if os.path.exists(vector_db_path):
    vector_db = FAISS.load_local(vector_db_path, embeddings)
else:
    vector_db = FAISS(embeddings)


imap_host = "imap.naver.com"
imap_user = os.getenv("imap_user_ID")
imap_password = os.getenv("imap_user_PW")


smtp_host = "smtp.naver.com"
smtp_port = 587
sender_email = imap_user
email_password = imap_password

if not imap_user or not imap_password or not openai_api_key:
    print("Missing environment variables.")
    raise ValueError(".env file ERROR.")
else:
    print("Loaded successfully.")

loader = PyPDFLoader("C:\Users\cybermed\Downloads\SPRI_AI_Brief_2023년12월호_F.pdf")
documents = loader.load()

vector_db = FAISS.from_documents(documents, embeddings)
vector_db.save_local("vector_store")

retriever = vector_db.as_retriever()

query = "Explain the main concept in the document."
relevant_docs = retriever.get_relevant_documents(query)
context = "\n".join([doc.page_content for doc in relevant_docs])

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Using the following context:\n{context}\nAnswer the query: {query}"}
    ],
    temperature=0.5,
    max_tokens=300
)

print("response:", response.choices[0].message['content'])

def fetch_emails():
    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(imap_user, imap_password)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} unseen emails.") #미확인 메일 로그

        for email_id in email_ids[-5:]: # 5개 메일 우선적 vectordb에 저장장 추후 UNSEEN기준 background check로 수정 예정 
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    sender_email = decode_header(msg["From"])[0][0]
                    if isinstance(sender_email, bytes):
                        sender_email = sender_email.decode()
                    print(f"Subject: {subject}")
                    print(f"Sender: {sender_email}")
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                print(f"Body: {body}")
                                process_email(subject, body, sender_email)
                    else:
                        body = msg.get_payload(decode=True).decode()
                        print(f"Body: {body}")
                        process_email(subject, body, sender_email)
        mail.logout()
    except Exception as e:
        print(f"Failed to fetch emails: {e}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": f"email:\nSubject: {subject}\nBody: {body}"}
        ],
        temperature=0.5,
        max_tokens=300
    )
    reply = response.choices[0].message['content']
    print(f"Generated Reply: {reply}")

    send_email(subject, reply)

def process_email(subject, body):
    print(f"Processing email: {subject}")
    document = Document(page_content=f"Subject: {subject}\n\n{body}")
    vector_db.add_documents([document])
    vector_db.save_local(vector_db_path)
    print(f"Stored email: {subject}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": f"email:\nSubject: {subject}\nBody: {body}"}
        ],
        temperature=0.5,
        max_tokens=300
    )
    reply = response.choices[0].message['content']
    print(f"Generated Reply: {reply}")
    send_email(subject, reply)

def send_email(subject, reply, receiver_email):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"Re: {subject}"
        message.attach(MIMEText(reply, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Response email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    fetch_emails()


