# FastAPI 애플리케이션 생성을 위한 클래스 import
from fastapi import FastAPI

# 기능별로 분리된 API 라우터 모듈 import
# - collection: 데이터 수집 및 벡터 DB 적재
# - strategy: RAG 기반 전략 질의
# - game_state: 게임 상태 검증
from app.api import collection, strategy, game_state

# 프로젝트 전역 설정값(프로젝트명, 패치 버전 등)
from app.core.config import settings


# FastAPI 애플리케이션 인스턴스 생성
# title 값은 Swagger 문서 상단에 표시됨
app = FastAPI(title=settings.PROJECT_NAME)


# =====================
# 라우터 등록 영역
# =====================

# 유튜브 등 외부 데이터 수집 관련 API
app.include_router(
    collection.router,
    prefix="/api/v1/collect",   # API 버전 및 도메인 분리
    tags=["Collection"]         # Swagger 문서에서의 그룹명
)

# 전략 질문 및 RAG 응답을 담당하는 API
app.include_router(
    strategy.router,
    prefix="/api/v1/strategy",
    tags=["Strategy"]
)

# 게임 상태 검증 및 관련 API
app.include_router(
    game_state.router,
    prefix="/api/v1/game",
    tags=["Game State"]
)


# =====================
# 기본 헬스 체크 엔드포인트
# =====================

@app.get("/")
def root():
    """
    📌 서버 상태 확인용 엔드포인트
    - 서버가 정상 실행 중인지 확인
    - 현재 적용 중인 게임 패치 버전 정보 제공
    """

    return {
        "message": "TFT Strategy Backend is Running",
        "patch": settings.CURRENT_PATCH
    }
