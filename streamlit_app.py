import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (공간 효율 극대화)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 젠스파크 일체형 커스텀 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    /* 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF !important;
    }

    /* 젠스파크 임베드 최적화: 상단 여백 완전 제거 */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 2rem !important; 
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 900px; 
    }
    
    /* 탭 메뉴 디자인: 심플한 언더라인 스타일 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; border-bottom: 1px solid #F1F5F9; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem !important; font-weight: 500; color: #64748B; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 2px solid #1E3A8A !important; font-weight: 700; }

    /* 가로형 버튼 툴바 스타일 */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important;
        background-color: #F8FAFC !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        height: 3.2rem !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
        padding: 0px !important;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #1E3A8A !important;
        color: #1E3A8A !important;
        background-color: #F1F5F9 !important;
    }
    
    /* 메인 실행 버튼: 젠스파크 포인트 컬러 매칭 */
    .stButton>button[kind="primary"] {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A !important;
        height: 3.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 700;
        margin-top: 10px;
    }

    /* 결과 출력 카드 */
    .result-box {
        background-color: #F9FBFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E0E7FF;
        color: #1E293B;
        line-height: 1.8;
        font-size: 1rem;
        margin-bottom: 15px;
    }

    /* 푸터 스타일 */
    .footer { text-align: center; color: #CBD5E1; font-size: 0.75rem; margin-top: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. AI 모델 로드
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.warning("환경 설정에서 API 키를 확인해 주세요.")

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성 (타이틀 제거 후 바로 탭 시작)
tab1, tab2 = st.tabs(["📄 목회 원고 작성", "🎨 성화 이미지 생성"])

with tab1:
    # 가로 4열 버튼 구성 (심플 라벨링)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📖 설교 초안"): st.session_state['p_input'] = "[본문 입력]: \n성도들의 삶에 적용할 수 있는 3대지 설교 개요를 작성해줘."
    with col2:
        if st.button("✍️ 목회 칼럼"): st.session_state['p_input'] = "[주제 입력]: \n따뜻하고 감동적인 목회 칼럼 한 페이지 분량을 작성해줘."
    with col3:
        if st.button("🙏 기도문"): st.session_state['p_input'] = "[대상/상황]: \n마음을 울리는 간절한 중보 기도문을 작성해줘."
    with col4:
        if st.button("📢 주보"): st.session_state['p_input'] = "[사역 내용]: \n성도들이 이해하기 쉽게 주보용 공지 문구로 요약해줘."

    # 입력창 (라벨 없이 심플하게)
    user_text = st.text_area("input", value=st.session_state['p_input'], height=180, label_visibility="collapsed", placeholder="여기에 내용을 상세히 적을수록 정확한 결과가 나옵니다.")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 원고를 작성 중입니다..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e: st.error(f"오류: {e}")
        else:
            st.warning("먼저 내용을 입력하거나 템플릿 버튼을 눌러주세요.")

    # 결과창 (SyntaxError 방지 로직 적용)
    if 'res_txt' in st.session_state:
        st.markdown("<p style='font-weight:700; color:#1E3A8A; margin-top:20px;'>🖋️ 작성 결과</p>", unsafe_allow_html=True)
        # 안전한 HTML 변환 처리
        display_html = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown(f'<div class="result-box">{display_html}</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="💾 PC/모바일에 파일로 저장하기",
            data=st.session_state['res_txt'],
            file_name="CTS_목회지원자료.txt",
            use_container_width=True
        )

with tab2:
    img_in = st.text_input("img", placeholder="예: 기도하는 손, 은혜로운 빛의 질감, 유화 스타일", label_visibility="collapsed")
    if st.button("AI 성화 생성 시작", type="primary"):
        if img_in:
            with st.spinner("이미지를 그리는 중입니다..."):
                encoded = img_in.replace(" ", "%20")
                st.session_state['res_img'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true&width=1024&height=1024"

    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True, caption="이미지를 길게 누르거나 우클릭하여 저장하세요.")

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
