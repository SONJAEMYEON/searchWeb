import requests
from datetime import datetime
import html
from config import Config
import urllib3
import json

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SearchService:
    def __init__(self):
        # 초기화 시점에 설정 유효성 검사
        Config.validate_config()
        self.naver_headers = {
            "X-Naver-Client-Id": Config.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": Config.NAVER_CLIENT_SECRET
        }

    def search_news(self, keyword, page=1, source="naver"):
        try:
            if source.lower() == "naver":
                return self._search_naver_news(keyword, page)
            else:
                return self._search_google_news(keyword, page)
        except Exception as e:
            raise Exception(f"{source} 검색 중 오류 발생: {str(e)}")

    def _search_naver_news(self, keyword, page):
        try:
            params = {
                "query": keyword,
                "display": 10,
                "start": (page - 1) * 10 + 1,
                "sort": "date"
            }
            
            response = requests.get(
                "https://openapi.naver.com/v1/search/news.json",
                headers=self.naver_headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                news_list = []
                
                for item in data.get('items', []):
                    news_list.append({
                        'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),
                        'content': item.get('description', '').replace('<b>', '').replace('</b>', ''),
                        'url': item.get('link', ''),
                        'pub_date': item.get('pubDate', ''),
                        'category': '네이버 뉴스'
                    })
                
                return {
                    'news_list': news_list,
                    'total_count': data.get('total', 0)
                }
            else:
                raise Exception(f"네이버 API 오류: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"네이버 뉴스 검색 중 오류: {str(e)}")

    def _search_google_news(self, keyword, page):
        try:
            params = {
                "key": Config.GOOGLE_API_KEY,
                "cx": Config.GOOGLE_CSE_ID,
                "q": keyword,
                "start": (page - 1) * 10 + 1
            }
            
            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                news_list = []
                
                for item in data.get('items', []):
                    news_list.append({
                        'title': item.get('title', ''),
                        'content': item.get('snippet', ''),
                        'url': item.get('link', ''),
                        'pub_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '구글 뉴스'
                    })
                
                return {
                    'news_list': news_list,
                    'total_count': data.get('searchInformation', {}).get('totalResults', 0)
                }
            else:
                raise Exception(f"구글 API 오류: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"구글 뉴스 검색 중 오류: {str(e)}") 