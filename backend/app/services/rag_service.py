from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.database.vector_db import get_vector_db
from app.models.schemas import GameState, StrategyResponse
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.vector_db = get_vector_db()
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=settings.OPENAI_API_KEY)

    def get_advice(self, question: str, game_state: GameState = None) -> StrategyResponse:
        # 1. 검색 필터링 (기능 5 & 7: 최신 패치만 검색)
        filter_criteria = {"patch": settings.CURRENT_PATCH}
        
        # 2. 관련 전략 Chunk 검색 (Top-k)
        docs = self.vector_db.similarity_search(question, k=3, filter=filter_criteria)
        if not docs:
            return StrategyResponse(
                summary="관련 전략을 찾을  수 없습니다.",
                detail="현재 패치에 대한 데이터가 없습니다. 영상을 먼저 수집해주세요.",
                sources=[]
            )
        context_text = "\n\n".join([d.page_content for d in docs])
        source_ids = list(set([d.metadata.get('video_id') for d in docs]))

        # 3. 게임 상태 텍스트화 (기능 4)
        state_text = "정보 없음"
        if game_state:
            state_text = (
                f"현재 스테이지: {game_state.stage}, 레벨: {game_state.level}, "
                f"골드: {game_state.gold}, 체력: {game_state.hp}, "
                f"보유 기물: {', '.join(game_state.board_units)}, "
                f"아이템: {', '.join(game_state.items)}"
            )

        # 4. 프롬프트 구성 (기능 6: 요약 & 상세 분리 요청)
        prompt_template = """
        당신은 TFT(롤토체스) 전문가 김지아입니다. 
        사용자의 [게임 상태]와 [참고 전략 데이터]를 기반으로 최적의 판단을 내려주세요.

        [참고 전략 데이터]
        {context}

        [사용자 게임 상태]
        {state}

        [사용자 질문]
        {question}

        응답 형식 지침:
        1. SUMMARY: 맨 첫 줄에 바쁜 사용자를 위한 한 줄 요약(명령조)을 작성하세요.
        2. DETAIL: 그 아래에 구체적인 이유와 행동 지침(레벨업 타이밍, 리롤 여부 등)을 설명하세요.
        """
        
        prompt = PromptTemplate.from_template(prompt_template)
        formatted_prompt = prompt.format(context=context_text, state=state_text, question=question)
        
        # 5. LLM 호출
        response_text = self.llm.predict(formatted_prompt)

        # 6. 결과 파싱 (Summary / Detail 분리)
        summary = "요약을 생성할 수 없습니다."
        detail = response_text
        
        if "SUMMARY:" in response_text and "DETAIL:" in response_text:
            parts = response_text.split("DETAIL:")
            summary = parts[0].replace("SUMMARY:", "").strip()
            detail = parts[1].strip()

        return StrategyResponse(
            summary=summary,
            detail=detail,
            sources=source_ids # 기능 8: 출처 반환
        )
