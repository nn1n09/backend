from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

# 임베딩 모델
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

# DB 인스턴스 생성 함수
def get_vector_db():
    return Chroma(
        collection_name="tft_strategies",
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_DB_DIR
    )
