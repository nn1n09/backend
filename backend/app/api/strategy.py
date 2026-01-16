from fastapi import APIRouter
from app.models.schemas import StrategyRequest, StrategyResponse
from app.services.rag_service import RAGService

router = APIRouter()

@router.post("/ask", response_model=StrategyResponse)
async def ask_strategy(request: StrategyRequest):
    """
    사용자의 질문과 게임 상태를 받아 전략적인 조언을 반환합니다.
    """
    rag_engine = RAGService()
    response = rag_engine.get_advice(request.question, request.game_state)
    return response
