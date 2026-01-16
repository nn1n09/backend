# LangChain 커뮤니티 패키지에서 Chroma 벡터스토어 import
from langchain_community.vectorstores import Chroma

# OpenAI 임베딩 모델을 사용하기 위한 클래스 import
from langchain_openai import OpenAIEmbeddings

# 프로젝트 전역 설정값(API Key, DB 경로 등)을 담고 있는 설정 객체
from app.core.config import settings


# 임베딩 모델 인스턴스 생성
# - 텍스트를 벡터로 변환하는 역할
# - OpenAI API Key는 설정 파일에서 불러옴
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


# 벡터 데이터베이스 인스턴스를 생성하여 반환하는 함수
def get_vector_db():
    """
    📌 역할
    - Chroma 벡터 DB 인스턴스를 생성
    - 동일한 설정으로 여러 곳에서 재사용 가능하도록 함수 형태로 제공
    """

    return Chroma(
        # 벡터 컬렉션 이름
        # (TFT 전략 데이터만 저장되는 논리적 단위)
        collection_name="tft_strategies",

        # 텍스트 → 벡터 변환에 사용할 임베딩 함수
        embedding_function=embeddings,

        # 벡터 데이터가 디스크에 영구 저장될 위치
        persist_directory=settings.CHROMA_DB_DIR
    )
