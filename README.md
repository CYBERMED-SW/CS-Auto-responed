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

주요 구성 요소

IMAP:

이메일 데이터를 수집합니다. 고객이 보낸 이메일을 서버에서 확인하고 다운로드합니다.

SMTP:

생성된 응답 이메일을 고객에게 전송합니다.

VLM (GPT):

GPT 모델을 사용하여 이메일 내용을 분석하고 분류합니다.

각 이메일의 주제에 따라 적합한 응답 초안을 생성합니다.

RAG (Retriever-Augmented Generation):

LangChain 라이브러리를 활용하여 메뉴얼 및 외부 데이터를 검색하여 GPT에 추가적인 정보를 제공합니다.

Vector DB (FAISS):

이메일 데이터를 벡터화하여 저장합니다.

RAG에서 검색 가능한 형태로 관리합니다.

RT (Background Server):

위의 모든 프로세스를 서버에서 자동으로 실행합니다.

서버 PC는 지속적으로 IMAP 및 SMTP와 상호작용하며 시스템을 유지합니다.

이메일 데이터 수집

IMAP 프로토콜을 사용하여 서버에서 이메일을 가져옵니다.

이메일 제목, 본문, 발신자 정보를 추출하여 처리합니다.

이메일 분류 및 응답 생성

분류:

VLM(GPT)을 사용하여 이메일을 카테고리별로 분류합니다.

예: "구매 PO", "신규 License 발급", "Rehost 요청", "제품 사용설명" 등.

응답 생성:

RAG를 활용하여 메뉴얼 데이터 및 벡터 DB에 저장된 이메일 데이터를 참조하여 GPT 기반으로 응답을 생성합니다.

생성된 응답은 고객의 요청에 맞게 자동으로 SMTP를 통해 전송됩니다.

데이터 저장

**FAISS(Vector DB)**를 사용하여 이메일 데이터를 벡터화하고 저장합니다.

데이터는 일정 기간(예: 30일) 이후 자동으로 삭제되도록 관리됩니다.



-------------------Library------------------
-openai

-langchain

-faiss-cpu

-python-dotenv