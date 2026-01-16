from fastapi import FastAPI
from app.api import collection, strategy, game_state
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# 라우터 등록
app.include_router(collection.router, prefix="/api/v1/collect", tags=["Collection"])
app.include_router(strategy.router, prefix="/api/v1/strategy", tags=["Strategy"])
app.include_router(game_state.router, prefix="/api/v1/game", tags=["Game State"])

@app.get("/")
def root():
    return {"message": "TFT Strategy Backend is Running", "patch": settings.CURRENT_PATCH}
