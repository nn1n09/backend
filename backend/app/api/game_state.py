from fastapi import APIRouter
from app.models.schemas import GameState

router = APIRouter()

@router.post("/validate")
async def validate_state(state: GameState):
    """
    클라이언트가 보내는 게임 상태 데이터가 형식이 맞는지 검증합니다.
    """
    return {"status": "valid", "summary": f"{state.stage} 스테이지, {state.gold}골드 보유 확인"}
