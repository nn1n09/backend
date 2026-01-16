from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeService:
    @staticmethod
    def get_transcript(video_id: str):
        try:
            # 한국어 자막 우선, 없으면 자동 생성 자막 시도
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            
            # 텍스트만 합치기 (타임스탬프 제거)
            full_text = " ".join([t['text'] for t in transcript_list])
            return full_text
        except Exception as e:
            print(f"Error fetching transcript for {video_id}: {e}")
            return None
