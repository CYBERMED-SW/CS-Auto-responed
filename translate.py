import openai
import smtplib
import imaplib
import email
import os
from dotenv import load_dotenv
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document


load_dotenv()
openai_api_key = os.getenv("openai_api_key")


embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("openai_api_key"))
vector_db_path = "vector_store"

if os.path.exists(vector_db_path):
    vector_db = FAISS.load_local(vector_db_path, embeddings)
else:
    vector_db = FAISS(embeddings)

imap_host = "imap.naver.com"
imap_user = "cybermed@gmail.com"
imap_password = "?????"

smtp_host = "smtp.naver.com"
smtp_port = 587
sender_email = imap_user
email_password = imap_password

def fetch_emails():
    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(imap_user, imap_password)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for email_id in email_ids[-5:]:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    sender = decode_header(msg["From"])[0][0]
                    if isinstance(sender, bytes):
                        sender = sender.decode()

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                process_email(subject, body, sender)
                    else:
                        body = msg.get_payload(decode=True).decode()
                        process_email(subject, body, sender)

        mail.logout()
    except Exception as e:
        print(f"Failed to fetch emails: {e}")

def store_email_in_vector_db(subject, body):
    document = Document(page_content=f"Subject: {subject}\n\n{body}")
    # document_ID
    vector_db.add_documents([document])
    vector_db.save_local(vector_db_path)
    print(f"Stored email: {subject}")

def process_email(subject, body, sender):
    store_email_in_vector_db(subject, body, sender)

    retriever = vector_db.as_retriever()
    relevant_docs = retriever.get_relevant_documents(body)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for drafting email responses."},
            {"role": "user", "content": f"Based on the following context:\n{context}\n\nDraft a response for this email:\nSubject: {subject}\nBody: {body}"}
        ],
        temperature=0.5,
        max_tokens=300
    )
    reply = response.choices[0].message['content']

    send_email(subject, reply, sender)

def send_email(subject, reply, receiver):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver  
        message["Subject"] = f"Re: {subject}"
        message.attach(MIMEText(reply, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver, message.as_string())
            print(f"Response email sent successfully to {receiver}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

        

if __name__ == "__main__":
    fetch_emails()
