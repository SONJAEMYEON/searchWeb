import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일의 절대 경로 지정
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///news.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 실제 발급받은 API 키를 따옴표 안에 입력
    NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
    
    # 구글 API 설정
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
    
    # Claude API 설정
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')  # .env 파일에서 API 키 로드

    # Gemini API 설정
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    @classmethod
    def validate_config(cls):
        if not cls.NAVER_CLIENT_ID or not cls.NAVER_CLIENT_SECRET:
            raise ValueError("네이버 API 키가 설정되지 않았습니다.")