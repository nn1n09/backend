import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class Preprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        # 잡담 제거 (구독, 좋아요 등)
        text = re.sub(r'(구독|좋아요|알림|댓글).*', '', text)
        # 불필요한 공백 제거
        return text.strip()

    @staticmethod
    def create_chunks(text: str, meta: dict) -> list[Document]:
        # 전략 단위 분리 (Chunking)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        texts = splitter.split_text(text)
        
        # 메타데이터 부착 (패치 버전, 비디오 ID 등)
        docs = [Document(page_content=t, metadata=meta) for t in texts]
        return docs
