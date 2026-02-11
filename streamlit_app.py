import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (최적화 레이아웃)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 젠스파크 커스텀 디자인 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF !important;
    }

    /* 상단 여백 제거 및 컨테이너 너비 조절 */
    .block-container { 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 900px; 
    }
    
    /* 탭 메뉴 디자인 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; border-bottom: 1px solid #F1F5F9; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem !important; font-weight: 600; color: #64748B; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 2px solid #1E3A8A !important; }

    /* 가로 버튼 툴바 스타일 (폰트 크기 통일) */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important;
        background-color: #F8FAFC !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        height: 3.5rem !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    
    /* 메인 실행 버튼 */
    .stButton>button[kind="primary"] {
        width: 100%;
        border-radius: 10px;
        background-color: #1E3A8A !important;
        height: 3.8rem !important;
        font-size: 1.2rem !important;
        font-weight: 700;
        margin-top: 15px;
    }

    /* 결과 출력 상자 */
    .result-box {
        background-color: #F9FBFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E0E7FF;
        color: #1E293B;
        line-height: 1.8;
        font-size: 1.05rem;
        margin-top: 20px;
    }

    .footer { text-align: center; color: #CBD5E1; font-size: 0.8rem; margin-top: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. AI 모델 로드
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.info("환경 설정(Secrets)에서 API 키를 먼저 입력해 주세요.")

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성 (타이틀 없이 탭으로 시작)
tab1, tab2 = st.tabs(["📄 목회 원고 작성", "🎨 이미지 생성"])

with tab1:
    # 요청하신 3단 가로 버튼 구성
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 설교"): 
            st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 설교 아웃라인을 만들어 주세요.\n\n아웃라인 형식:\n1. 서론 (도입 질문 또는 이야기)\n2. 본론 (3개 포인트, 각 포인트에 설명+예시+적용)\n3. 결론 (요약 + 삶의 적용 + 기도)"
    with col2:
        if st.button("🙏 기도"): 
            st.session_state['p_input'] = "- 기도 상황: [예: 주일예배 대표기도 / 새벽기도 / 심방기도 / 장례식]\n- 기도 주제: [예: 교회 부흥 / 병 치유 / 감사 / 회개]\n- 기도 시간: 약 2분\n\n위 상황에 맞는 기도문을 작성해 주세요. 한국 교회 전통에 맞는 경건한 어투로 작성해 주세요."
    with col3:
        if st.button("📢 주보"): 
            st.session_state['p_input'] = "- 교회명: [예: 사랑의교회]\n- 이번 주일 날짜: \n- 설교 제목: \n- 본문 말씀: \n- 교회 행사/광고: [예: 수요예배, 금요기도회, 성경통독 등]\n\n위 정보를 바탕으로 이번 주일 주보에 들어갈 문구를 작성해 주세요.\n\n포함할 항목:\n1. 환영 인사 (따뜻하고 간결하게)\n2. 금주 말씀 묵상 가이드 (3줄)\n3. 교회 소식/광고 (깔끔한 정리)\n4. 이번 주 기도제목 (3개)"

    # 입력창
    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed", placeholder="버튼을 누르거나 내용을 직접 입력해 주세요.")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 원고를 작성하고 있습니다..."):
                try:
                    model = genai.GenerativeModel('gem
