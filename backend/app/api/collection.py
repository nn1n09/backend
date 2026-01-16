# FastAPI에서 라우터 구성, 백그라운드 작업 처리, 예외 처리를 위한 모듈 import
from fastapi import APIRouter, BackgroundTasks, HTTPException

# 유튜브 자막을 수집하는 서비스 로직
from app.services.youtube_service import YouTubeService

# 텍스트 전처리 및 청킹을 담당하는 모듈
from app.services.preprocess import Preprocessor

# 벡터 데이터베이스 인스턴스를 가져오는 함수
from app.database.vector_db import get_vector_db

# 전역 설정값(예: 현재 패치 버전)을 관리하는 설정 객체
from app.core.config import settings


# FastAPI 라우터 객체 생성
router = APIRouter()


def run_pipeline(video_id: str, patch: str):
    """
    유튜브 영상 하나에 대해
    자막 수집 → 전처리 → 청킹 → 벡터 DB 저장까지 수행하는 파이프라인 함수
    (백그라운드 태스크에서 실행됨)
    """

    # 1. 유튜브 영상 ID를 기반으로 자막 텍스트 수집
    raw_text = YouTubeService.get_transcript(video_id)

    # 자막이 없거나 수집 실패 시 파이프라인 종료
    if not raw_text:
        return
    
    # 2. 수집된 원본 자막 텍스트를 정제 (불필요한 문자 제거 등)
    cleaned_text = Preprocessor.clean_text(raw_text)
    
    # 3. 벡터 DB에 함께 저장할 메타데이터 구성
    # - video_id: 어떤 영상에서 왔는지
    # - patch: 어떤 데이터 패치 버전인지
    metadata = {"video_id": video_id, "patch": patch}
    
    # 4. 정제된 텍스트를 의미 단위로 분할(Chunking)
    # 각 chunk에는 위에서 만든 metadata가 함께 포함됨
    chunks = Preprocessor.create_chunks(cleaned_text, metadata)
    
    # 5. 벡터 DB 인스턴스를 가져와 문서(chunk) 저장
    db = get_vector_db()
    db.add_documents(chunks)

    # 처리 완료 로그 출력 (디버깅 / 모니터링용)
    print(f"Video {video_id} processed and saved.")


@router.post("/{video_id}")
async def collect_video(
    video_id: str,
    background_tasks: BackgroundTasks,
    patch: str = settings.CURRENT_PATCH
):
    """
    📌 API 엔드포인트 설명
    - 유튜브 영상 ID를 받아서
    - 실제 처리 로직(run_pipeline)은 백그라운드에서 실행
    - API 응답은 즉시 반환 (비동기 처리)
    """

    # FastAPI의 BackgroundTasks를 사용해
    # run_pipeline 함수를 백그라운드 작업으로 등록
    background_tasks.add_task(run_pipeline, video_id, patch)

    # 즉시 클라이언트에게 처리 시작 응답 반환
    return {
        "status": "processing_started",
        "video_id": video_id,
        "patch": patch
    }
