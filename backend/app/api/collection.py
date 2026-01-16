from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.youtube_service import YouTubeService
from app.services.preprocess import Preprocessor
from app.database.vector_db import get_vector_db
from app.core.config import settings

router = APIRouter()

def run_pipeline(video_id: str, patch: str):
    # 1. 자막 수집
    raw_text = YouTubeService.get_transcript(video_id)
    if not raw_text:
        return
    
    # 2. 전처리
    cleaned_text = Preprocessor.clean_text(raw_text)
    
    # 3. 메타데이터 생성 (패치 버전, 출처 저장)
    metadata = {"video_id": video_id, "patch": patch}
    
    # 4. Chunking
    chunks = Preprocessor.create_chunks(cleaned_text, metadata)
    
    # 5. Vector DB 저장
    db = get_vector_db()
    db.add_documents(chunks)
    print(f"Video {video_id} processed and saved.")

@router.post("/{video_id}")
async def collect_video(video_id: str, background_tasks: BackgroundTasks, patch: str = settings.CURRENT_PATCH):
    """
    유튜브 영상 ID를 받아 백그라운드에서 자막 수집 -> 전처리 -> DB 저장을 수행합니다.
    """
    background_tasks.add_task(run_pipeline, video_id, patch)
    return {"status": "processing_started", "video_id": video_id, "patch": patch}
