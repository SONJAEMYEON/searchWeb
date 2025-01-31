import os
from dotenv import load_dotenv
import streamlit as st
from config import Config
# 나머지 코드... 
import requests
from datetime import datetime
from services.search_service import SearchService
from services.counsel_service import CounselService

# .env 파일 로드
load_dotenv()

# 페이지 설정이 가장 먼저 와야 합니다
st.set_page_config(
    page_title="이 세상의 모든 검색과 상담",
    page_icon="🔍",
    layout="wide"
)

# CSS 파일 로드
def load_css(css_file):
    with open(css_file, 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# CSS 로드
load_css('static/css/style.css')

# 그 다음에 다른 import문들
import requests
from datetime import datetime
from services.search_service import SearchService
from services.counsel_service import CounselService
from config import Config

# 세션 상태 초기화
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# 타이틀
st.title("이 세상의 모든 검색과 상담")
st.markdown("---")

# 탭 생성
search_tab, counsel_tab = st.tabs(["📰 검색", "💬 상담"])

# 검색 탭
with search_tab:
    st.header("이 세상의 모든 검색")
    
    # 검색 컨테이너 생성
    with st.container():
        # 컬럼 비율 조정
        cols = st.columns([1.2, 5, 1.3])
        
        with cols[0]:
            search_source = st.selectbox(
                label="검색 소스 선택",  # 접근성을 위한 라벨 추가
                options=["네이버", "구글"],
                key="search_source",
                label_visibility="collapsed"  # 라벨 시각적으로 숨김
            )
        
        with cols[1]:
            search_keyword = st.text_input(
                label="검색어 입력",  # 접근성을 위한 라벨 추가
                placeholder="검색어를 입력하세요",
                label_visibility="collapsed"  # 라벨 시각적으로 숨김
            )
            
        with cols[2]:
            search_button = st.button(
                "검색하기",
                key="search_button",
                use_container_width=True
            )
    
    # 검색 로직
    if search_button:
        if search_keyword:
            try:
                with st.spinner("검색 중..."):
                    search_service = SearchService()
                    results = search_service.search_news(
                        keyword=search_keyword,
                        page=1,
                        source=search_source.lower()
                    )
                    
                    # 검색 결과 표시
                    for news in results['news_list']:
                        with st.container():
                            st.markdown(f"""
                                <div class="news-card">
                                    <h4 class="news-title">{news['title']}</h4>
                                    <p class="news-content">{news['content']}</p>
                                    <div class="news-meta">
                                        <span>출처: {news['category']}</span>
                                        <span>날짜: {news['pub_date']}</span>
                                    </div>
                                    <a href="{news['url']}" target="_blank" class="news-link">
                                        기사 보기 →
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"검색 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("검색어를 입력해주세요.")

# 상담 탭
with counsel_tab:
    counsel_type = st.radio(
        "상담 유형을 선택하세요",
        ["입시 상담", "심리 상담"],
        horizontal=True
    )
    
    counsel_query = st.text_area("상담 내용을 입력하세요", height=150, placeholder="고민이나 궁금한 점을 자유롭게 작성해주세요.")
    
    # 상담하기 버튼을 누를 때마다 새로운 대화 시작
    if st.button("상담하기", key="counsel_button"):
        if counsel_query:
            try:
                # 대화 기록 초기화
                st.session_state.conversation_history = []
                
                counsel_service = CounselService()
                
                # 현재 질문 추가
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": counsel_query
                })
                
                # 상담 처리
                with st.spinner('상담 답변을 생성하고 있습니다...'):
                    if counsel_type == "입시 상담":
                        result = counsel_service.get_entrance_exam_counsel(
                            st.session_state.conversation_history
                        )
                    else:
                        result = counsel_service.get_psychology_counsel(
                            st.session_state.conversation_history
                        )
                    
                    if result['success']:
                        # 답변 추가
                        st.session_state.conversation_history.append({
                            "role": "assistant",
                            "content": result['response']
                        })
                        
                        # 대화 내용 표시
                        st.markdown("### 상담 내역")
                        for msg in st.session_state.conversation_history:
                            if msg["role"] == "user":
                                st.markdown(f"""
                                    <div class='chat-message user-message'>
                                        <strong>🙋‍♂️ 질문:</strong><br>{msg["content"]}
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                    <div class='chat-message assistant-message'>
                                        <strong>👩‍⚕️ 답변:</strong><br>{msg["content"]}
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error(result['error'])
                        
            except Exception as e:
                st.error(f"상담 처리 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("상담 내용을 입력해주세요.")
