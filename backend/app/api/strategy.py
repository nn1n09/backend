# FastAPI에서 API 라우터 생성을 위한 APIRouter import
from fastapi import APIRouter

# 전략 요청(Request)과 응답(Response)에 사용되는 Pydantic 스키마
from app.models.schemas import StrategyRequest, StrategyResponse

# RAG(Retrieval-Augmented Generation) 기반 전략 생성 서비스
from app.services.rag_service import RAGService


# 이 파일에서 사용할 API 라우터 객체 생성
router = APIRouter()


@router.post("/ask", response_model=StrategyResponse)
async def ask_strategy(request: StrategyRequest):
    """
    📌 API 엔드포인트 역할
    - 사용자의 질문(question)과 현재 게임 상태(game_state)를 입력으로 받음
    - RAG 기반 전략 엔진을 통해 상황에 맞는 조언 생성
    - 생성된 결과를 StrategyResponse 형식으로 반환
    """

    # RAG 전략 엔진 인스턴스 생성
    # (내부적으로 벡터 DB 검색 + LLM 응답 생성 로직을 포함할 것으로 예상됨)
    rag_engine = RAGService()

    # 사용자의 질문과 게임 상태를 전달하여 전략적 조언 생성
    response = rag_engine.get_advice(
        request.question,
        request.game_state
    )

    # StrategyResponse 스키마에 맞는 응답 반환
    # response_model 옵션에 의해 출력 형식이 자동 검증/직렬화됨
    return response
