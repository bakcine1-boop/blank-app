import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 (모바일 최적화 및 와이드 레이아웃)
st.set_page_config(
    page_title="AI 목회비서", 
    page_icon="🙏", 
    layout="wide"
)

# 2. 젠스파크 스타일의 완성도 높은 CSS (네이비 & 화이트 톤)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA !important; /* 부드러운 배경색 */
    }

    /* 상단 여백 제거 */
    .block-container {
        padding-top: 1rem;
    }

    /* 메인 헤더: 깊이감 있는 네이비 그라데이션 */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #172554 100%);
        padding: 2rem 1rem;
        border-radius: 0 0 15px 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* 서비스 카드: 깨끗하고 정돈된 컨테이너 */
    .service-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem;
    }
    .template-label {
        font-size: 0.95rem;
        color: #4B5563;
        margin-bottom: 0.8rem;
        display: block;
    }

    /* 버튼 스타일: 신뢰감 있는 네이비색, 부드러운 호버 효과 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3rem;
        font-size: 1rem;
        font-weight: 500;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1e40af !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 템플릿 선택 버튼 (작은 사이즈) */
    .small-button>.stButton>button {
        height: 2.5rem;
        font-size: 0.9rem;
        background-color: #F3F4F6 !important; /* 연한 회색 배경 */
        color: #1E3A8A !important; /* 네이비 글씨 */
        border: 1px solid #D1D5DB !important;
    }
    .small-button>.stButton>button:hover {
        background-color: #E5E7EB !important;
        border-color: #1E3A8A !important;
    }

    /* 탭 디자인: 네이비톤 강조 */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 20px;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        height: 50px;
        color: #6B7280;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #1E3A8A !important;
        border-bottom-color: #1E3A8A !important;
        font-weight: 700;
    }
    
    /* 입력창 스타일 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
        padding: 0.8rem;
    }

    /* 모바일 최적화 */
    @media (max-width: 640px) {
        .main-header { padding: 1.5rem 1rem; margin-bottom: 1.5rem; }
        .main-header h1 { font-size: 1.6rem !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.95rem !important; padding: 0.5rem 0.8rem !important; }
        .service-card { padding: 1.2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API 보안 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("시스템 설정 오류: API 키를 찾을 수 없습니다.")
    st.stop()

# 4. 상단 헤더 (심플하고 강력하게)
st.markdown("""
    <div class="main-header">
        <h1 style='margin: 0; font-weight: 700;'>AI 목회비서</h1>
        <p style='margin-top: 0.5rem; opacity: 0.9; font-size: 1.05rem;'>CTS 미디어목회지원센터 제공</p>
    </div>
    """, unsafe_allow_html=True)

# --- 프롬프트 템플릿 및 상태 관리 ---
if 'user_topic' not in st.session_state:
    st.session_state['user_topic'] = ""

templates = {
    "📖 설교 초안": "이번 주일 설교 본문은 [본문 입력]입니다. 주제는 [주제 입력]이며, 청중이 이해하기 쉽고 은혜로운 3대지 설교 초안을 작성해 주세요. 예화와 적용점을 포함해 주세요.",
    "✍️ 목회 칼럼": "주보에 실을 목회 칼럼을 작성하려 합니다. 주제는 '감사'이며, 성도들에게 위로와 도전을 주는 따뜻한 어조로 A4 반 장 분량으로 작성해 주세요.",
    "🙏 대표 기도문": "이번 주일 예배 대표 기도문을 작성해 주세요. 나라와 민족, 교회와 환우들을 위한 중보 기도를 포함하여 간절한 마음을 담아 주세요."
}

def apply_template(text):
    st.session_state['user_topic'] = text

# 5. 메인 기능 탭
tab1, tab2 = st.tabs(["📝 설교 및 칼럼 작성", "🎨 이미지 생성"])

# --- 탭 1: 텍스트 작성 ---
with tab1:
    # 카드형 컨테이너 시작
    with st.container():
        st.markdown("""
            <div class="service-card">
                <strong style='color: #1E3A8A; font-size: 1.1rem;'>작성 요청</strong>
                <p style='color: #4B5563; font-size: 0.95rem; margin-top: 0.5rem;'>
                    원하시는 내용을 직접 입력하거나, 아래 <b>추천 양식</b>을 선택해 보세요.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 추천 양식 버튼 (카드 내부처럼 보이게 배치)
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("📖 설교 초안", key="t1"): apply_template(templates["📖 설교 초안"])
        with col_t2:
            if st.button("✍️ 목회 칼럼", key="t2"): apply_template(templates["✍️ 목회 칼럼"])
        with col_t3:
            if st.button("🙏 대표 기도문", key="t3"): apply_template(templates["🙏 대표 기도문"])
        
        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True) # 간격

        # 입력창 (세션 상태와 연결)
        user_topic_input = st.text_area(
            "내용 입력",
            value=st.session_state['user_topic'],
            height=280,
            label_visibility="collapsed",
            placeholder="여기에 주제나 본문을 입력하시면 AI가 초안을 작성해 드립니다."
        )
        
        # 작성 시작 버튼
        if st.button("작성 시작하기 (AI)"):
            if user_topic_input:
                with st.spinner("AI가 묵상하며 내용을 정리 중입니다..."):
                    try:
                        # 속도와 성능의 균형: Flash 모델 사용
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(user_topic_input)
                        st.session_state['generated_text'] = response.text
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
            else:
                st.warning("내용을 입력해 주세요.")

    # 결과 표시 영역
    if 'generated_text' in st.session_state:
        st.markdown("---")
        st.markdown("### 📖 작성 결과")
        
        # 결과 카드
        st.markdown(f"""
            <div class="service-card" style='background-color: #F8FAFC;'>
                {st.session_state['generated_text']}
            </div>
        """, unsafe_allow_html=True)
        
        # 하단 버튼 그룹
        col_copy, col_download = st.columns([1, 1])
        with col_copy:
            with st.expander("텍스트 복사하기"):
                st.code(st.session_state['generated_text'], language="markdown")
        with col_download:
            st.download_button(
                label="💾 텍스트 파일 저장 (.txt)",
                data=st.session_state['generated_text'],
                file_name="설교초안.txt",
                mime="text/plain"
            )

# --- 탭 2: 이미지 생성 (나노바나나 유지) ---
with tab2:
    # 카드형 컨테이너
    with st.container():
        st.markdown("""
            <div class="service-card">
                <strong style='color: #1E3A8A; font-size: 1.1rem;'>이미지 생성</strong>
                <p style='color: #4B5563; font-size: 0.95rem; margin-top: 0.5rem;'>
                    설교 화면에 사용할 이미지를 말하듯이 설명해 주세요.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
        img_prompt = st.text_input("그림 설명", placeholder="예: 거친 파도 위를 걸어가시는 예수님의 뒷모습, 웅장한 유화 스타일")
        
        if st.button("이미지 생성하기 (AI)"):
            if img_prompt:
                with st.spinner("AI 화가가 그림을 그리고 있습니다..."):
                    encoded = img_prompt.replace(" ", "%20")
                    # 나노바나나 (Pollinations) 엔진
                    img_url = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                    time.sleep(1.5)
                    st.session_state['generated_image'] = img_url
            else:
                st.warning("이미지에 대한 설명을 입력해 주세요.")

    # 결과 표시 영역
    if 'generated_image' in st.session_state:
         st.markdown("---")
         st.markdown("### 🎨 생성 결과")
         st.image(st.session_state['generated_image'], use_container_width=True, caption="결과 이미지 (우클릭하여 저장)")
         st.success("이미지가 완성되었습니다. 마우스 우클릭 또는 길게 눌러 저장하세요.")

# 6. 하단 푸터
st.markdown("<br><br><div style='text-align: center; color: #9CA3AF; font-size: 0.8rem;'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)
