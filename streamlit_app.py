import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (모바일 최적화 레이아웃)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 모바일/반응형 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF !important;
    }

    /* 반응형 컨테이너 설정 */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 850px; 
    }
    
    /* 탭 메뉴: 모바일에서 글자가 잘리지 않도록 조정 */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: center; 
        gap: 10px; 
    }
    .stTabs [data-baseweb="tab"] { 
        font-size: 1rem !important; 
        padding: 8px 12px !important;
    }

    /* 템플릿 버튼: 모바일 터치 대응 */
    div[data-testid="column"] button {
        width: 100% !important;
        background-color: #F8FAFC !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        margin-bottom: 5px !important;
        height: 2.8rem !important;
    }
    
    /* 실행 버튼: 크고 명확하게 */
    .stButton>button[kind="primary"] {
        width: 100%;
        border-radius: 12px;
        background-color: #1E3A8A !important;
        height: 3.8rem !important;
        font-size: 1.2rem !important;
        font-weight: 700;
    }

    /* 모바일 결과창 가독성 */
    .result-card {
        background-color: #F1F5F9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* 모바일용 푸터 간격 */
    .footer {
        text-align: center; 
        color: #94A3B8; 
        font-size: 0.75rem; 
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.info("Secrets에서 API 키를 설정해주세요.")

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 메인 콘텐츠
st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>💡 AI 목회 지원 센터</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 설교/칼럼", "🎨 이미지 생성"])

with tab1:
    # 템플릿 버튼을 2열씩 배치 (모바일 가독성)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 설교 초안"): st.session_state['p_input'] = "오늘 본문은 [입력]입니다. 성도들을 위한 3대지 설교 개요를 작성해줘."
        if st.button("✍️ 목회 칼럼"): st.session_state['p_input'] = "[주제]를 바탕으로 따뜻한 격려가 담긴 목회 칼럼을 써줘."
    with col2:
        if st.button("🙏 중보 기도문"): st.session_state['p_input'] = "환우들과 지친 성도들을 위한 중보 기도문을 작성해줘."
        if st.button("📢 주보 소식"): st.session_state['p_input'] = "이번 주 사역 소식을 주보용 문구로 요약해줘."

    user_text = st.text_area("input", value=st.session_state['p_input'], height=180, label_visibility="collapsed", placeholder="내용을 입력하세요.")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("생성 중..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e: st.error(f"오류: {e}")

    if 'res_txt' in st.session_state:
        st.markdown(f'<div class="result-card">{st.session_state["res_txt"].replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        st.download_button("💾 결과물 저장", st.session_state['res_txt'], file_name="CTS_AI_목회자료.txt", use_container_width=True)

with tab2:
    img_in = st.text_input("img", placeholder="예: 평화로운 숲속 교회, 수채화풍", label_visibility="collapsed")
    if st.button("이미지 생성 시작", type="primary"):
        if img_in:
            with st.spinner("그리는 중..."):
                encoded = img_in.replace(" ", "%20")
                st.session_state['res_img'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true&width=1024&height=1024"

    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True, caption="길게 눌러 이미지 저장 가능")

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)
