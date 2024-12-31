시스템 아키텍처

IMAP (Sender)

   └─ e-mail

SMTP (Receiver)

   └─ respond (separate for each category)

VLM (GPT)

   └─ RAG (LangChain)
          └─ External Source (CyberMed Manual)

Vector DB (FAISS)

   └─ Mail Data

RT (Background Server PC)


-------------------Library------------------

-openai

-langchain

-faiss-cpu

-python-dotenv
