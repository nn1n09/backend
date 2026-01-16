from typing import List, Optional
from pydantic import BaseModel

# 게임 상태 입력 데이터 모델
class GameState(BaseModel):
    stage: str          # 예: "3-2"
    gold: int           # 예: 50
    hp: int             # 예: 88
    level: int          # 예: 6
    board_units: List[str] # 예: ["아리", "가렌"]
    items: List[str]       # 예: ["BF대검", "곡궁"]
    synergies: List[str]   # 예: ["KDA(3)"]
    win_streak: bool       # 연승 여부

# 전략 검색 요청
class StrategyRequest(BaseModel):
    question: str
    game_state: Optional[GameState] = None 

# 전략 응답 (요약 및 출처 포함)
class StrategyResponse(BaseModel):
    summary: str        # 한 줄 요약
    detail: str         # 상세 운영법
    sources: List[str]  # 출처 영상 ID 목록
