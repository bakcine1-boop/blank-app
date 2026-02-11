import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 디자인 CSS (젠스파크 스타일)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #FFFFFF !important; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; max-width: 900px; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; background-color: #F8FAFC !important;
        border-radius: 10px !important; font-size: 1.1rem !important;
        font-weight: 600 !important; height: 3.5rem !important; border: 1px solid #E2E8F0 !important;
    }
    .stButton>button[kind="primary"] {
        width: 100%; border-radius: 10px; background-color: #1E3A8A !important;
        color: white !important; height: 3.8rem !important; font-size: 1.2rem !important;
        font-weight: 700; margin-top: 15px; border: none;
    }
    .result-box {
        background-color: #F9FBFF; padding: 24px; border-radius: 12px;
        border: 1px solid #E0E7FF; color: #1E293B; line-height: 1.8; font-size: 1.05rem; margin-top: 20px;
    }
    .footer { text-align: center; color: #CBD5E1; font-size: 0.8rem; margin-top: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정 (API 키 보안 확인)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets 설정에서 GOOGLE_API_KEY를 확인해주세요.")

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성
tab1, tab2 = st.tabs(["📄 목회 원고 작성", "🎨 이미지 생성"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 설교"): 
            st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 설교 아웃라인을 만들어 주세요."
    with col2:
        if st.button("🙏 기도"): 
            st.session_state['p_input'] = "- 기도 상황: \n- 기도 주제: \n- 기도 시간: 약 2분\n\n위 상황에 맞는 경건한 기도문을 작성해 주세요."
    with col3:
        if st.button("📢 주보"): 
            st.session_state['p_input'] = "- 교회명: \n- 이번 주일 날짜: \n- 설교 제목: \n- 본문 말씀: \n- 교회 행사/광고: \n\n위 정보를 바탕으로 주보 문구를 작성해 주세요."

    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 원고를 작성 중입니다..."):
                try:
                    # [수정포인트] 가장 범용적인 모델 이름으로 호출
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    # 만약 위 모델이 안되면 구버전인 'gemini-pro'로 한 번 더 시도
                    try:
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(user_text)
                        st.session_state['res_txt'] = response.text
                    except Exception as e2:
                        st.error(f"모델 연결 오류: {e2}")

    if 'res_txt' in st.session_state:
        st.markdown("<p style='font-weight:700; color:#1E3A8A; margin-top:20px;'>🖋️ 작성 결과</p>", unsafe_allow_html=True)
        p_text = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown('<div class="result-box">' + p_text + '</div>', unsafe_allow_html=True)
        st.download_button("💾 파일로 저장", st.session_state['res_txt'], file_name="CTS_AI_원고.txt", use_container_width=True)

with tab2:
    img_in = st.text_input("img", placeholder="그림 설명을 입력하세요", label_visibility="collapsed")
    if st.button("이미지 생성 시작 🎨", type="primary"):
        if img_in:
            with st.spinner("그리는 중..."):
                encoded = img_in.replace(" ", "%20")
                st.session_state['res_img'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True)

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
