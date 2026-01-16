# FastAPI에서 라우터 생성을 위한 APIRouter import
from fastapi import APIRouter

# 클라이언트로부터 전달받는 게임 상태 데이터를 검증하기 위한 Pydantic 스키마
from app.models.schemas import GameState


# 해당 파일에서 사용할 API 라우터 객체 생성
router = APIRouter()


@router.post("/validate")
async def validate_state(state: GameState):
    """
    📌 API 엔드포인트 역할
    - 클라이언트가 전송한 게임 상태(state)를 수신
    - GameState 스키마를 통해 데이터 형식 및 타입을 자동 검증
    - 검증이 통과되면 요약 정보를 포함한 응답 반환
    """

    # FastAPI + Pydantic에 의해
    # 요청 본문(JSON)이 GameState 구조와 맞지 않으면
    # 이 함수에 도달하기 전에 자동으로 422 에러가 발생함

    # 검증이 정상적으로 끝났음을 의미하는 응답 반환
    return {
        "status": "valid",
        # 게임 진행 스테이지와 보유 골드를 요약 문자열로 제공
        "summary": f"{state.stage} 스테이지, {state.gold}골드 보유 확인"
    }
