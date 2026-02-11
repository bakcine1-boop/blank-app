import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (모바일 및 PC 반응형 최적화)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 디자인 최적화 CSS (젠스파크 스타일과 일치)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF !important;
    }

    /* 상단 여백 제거 및 컨테이너 폭 조절 */
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

    /* 가로 3단 버튼 스타일 (글자 크기 동일화) */
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
    
    /* 실행 버튼: CTS 네이비 색상 */
    .stButton>button[kind="primary"] {
        width: 100%;
        border-radius: 10px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3.8rem !important;
        font-size: 1.2rem !important;
        font-weight: 700;
        margin-top: 15px;
        border: none;
    }

    /* 결과 출력창 */
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

# 3. 모델 설정 및 보안 확인
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.warning("⚠️ Streamlit 설정(Secrets)에서 GOOGLE_API_KEY를 입력해주세요.")
except Exception as e:
    st.error("API 설정 중 오류가 발생했습니다: " + str(e))

# 입력값 저장용 세션 상태 초기화
if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 메인 화면 (타이틀 없이 탭으로 깔끔하게 구성)
tab1, tab2 = st.tabs(["📝 목회 원고 작성", "🎨 이미지 생성"])

with tab1:
    # 설교, 기도, 주보 가로 3열 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 설교"): 
            st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 설교 아웃라인을 만들어 주세요.\n\n아웃라인 형식:\n1. 서론 (도입 질문 또는 이야기)\n2. 본론 (3개 포인트, 각 포인트에 설명+예시+적용)\n3. 결론 (요약 + 삶의 적용 + 기도)"
    with col2:
        if st.button("🙏 기도"): 
            st.session_state['p_input'] = "- 기도 상황: \n- 기도 주제: \n- 기도 시간: 약 2분\n\n위 상황에 맞는 기도문을 작성해 주세요. 한국 교회 전통에 맞는 경건한 어투로 작성해 주세요."
    with col3:
        if st.button("📢 주보"): 
            st.session_state['p_input'] = "- 교회명: \n- 이번 주일 날짜: \n- 설교 제목: \n- 본문 말씀: \n- 교회 행사/광고: \n\n위 정보를 바탕으로 이번 주일 주보에 들어갈 문구를 작성해 주세요.\n\n포함할 항목:\n1. 환영 인사\n2. 금주 말씀 묵상 가이드(3줄)\n3. 교회 소식/광고\n4. 이번 주 기도제목(3개)"

    # 입력 텍스트 영역
    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed", placeholder="버튼을 눌러 템플릿을 불러오거나 직접 입력하세요.")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 원고를 작성하고 있습니다..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error("AI 요청 중 오류가 발생했습니다: " + str(e))
        else:
            st.warning("내용을 먼저 입력해 주세요.")

    # 결과창 (SyntaxError를 피하기 위한 원시적 결합 방식)
    if 'res_txt' in st.session_state:
        st.markdown("<p style='font-weight:700; color:#1E3A8A; margin-top:20px; font-size:1.1rem;'>🖋️ 작성 결과</p>", unsafe_allow_html=True)
        
        # 줄바꿈 처리 후 HTML 결합 (f-string 대신 '+' 연산자 사용으로 에러 방지)
        p_text = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown('<div class="result-box">' + p_text + '</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="💾 작성된 원고 파일로 저장하기",
            data=st.session_state['res_txt'],
            file_name="CTS_AI_목회원고.txt",
            use_container_width=True
        )

with tab2:
    st.markdown("<p style='font-weight: 600; color: #334155;'>이미지 생성 설명을 입력하세요.</p>", unsafe_allow_html=True)
    img_in = st.text_input("img", placeholder="예: 평화로운 호숫가에서 기도하는 예수님, 부드러운 유화 스타일", label_visibility="collapsed")
    
    if st.button("이미지 생성 시작", type="primary"):
        if img_in:
            with st.spinner("이미지를 생성 중입니다..."):
                # 공백 처리 로직
                encoded = img_in.replace(" ", "%20")
                st.session_state['res_img'] = "https://image.pollinations.ai/prompt/" + encoded + "?nologo=true&width=1024&height=1024"
        else:
            st.warning("설명을 입력해 주세요.")

    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True, caption="이미지를 길게 누르거나 우클릭하여 저장하세요.")

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
