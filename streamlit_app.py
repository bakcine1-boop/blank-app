import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (공간 효율 및 반응형 최적화)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 디자인 CSS (젠스파크 스타일 + 모바일 최적화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #FFFFFF !important; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; max-width: 900px; }
    
    /* 탭 메뉴 디자인 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; border-bottom: 1px solid #F1F5F9; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem !important; font-weight: 600; color: #64748B; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 3px solid #1E3A8A !important; }

    /* 가로형 3단 버튼 (설교, 기도, 주보) */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; background-color: #F8FAFC !important;
        border-radius: 10px !important; font-size: 1.1rem !important;
        font-weight: 600 !important; height: 3.5rem !important; border: 1px solid #E2E8F0 !important;
    }
    
    /* 메인 실행 버튼 */
    .stButton>button[kind="primary"] {
        width: 100%; border-radius: 10px; background-color: #1E3A8A !important;
        color: white !important; height: 3.8rem !important; font-size: 1.2rem !important;
        font-weight: 700; margin-top: 15px; border: none;
    }

    /* 결과창 디자인 */
    .result-box {
        background-color: #F9FBFF; padding: 24px; border-radius: 12px;
        border: 1px solid #E0E7FF; color: #1E293B; line-height: 1.8; font-size: 1.05rem; margin-top: 20px;
    }
    .footer { text-align: center; color: #CBD5E1; font-size: 0.8rem; margin-top: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정 및 보안 확인
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.info("환경 설정(Secrets)에서 API 키를 먼저 입력해 주세요.")

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성
tab1, tab2 = st.tabs(["📝 최신형 목회 원고 작성 (Gemini 1.5 Pro)", "🎨 고품질 이미지 생성 (Imagen 3)"])

with tab1:
    # 가로 3단 버튼 구성
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 설교"): 
            st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 깊이 있는 설교 아웃라인을 만들어 주세요."
    with col2:
        if st.button("🙏 기도"): 
            st.session_state['p_input'] = "- 기도 상황: \n- 기도 주제: \n- 기도 시간: 약 2분\n\n위 상황에 맞는 경건한 기도문을 작성해 주세요. 한국 교회 전통에 맞는 어투를 사용해 줘."
    with col3:
        if st.button("📢 주보"): 
            st.session_state['p_input'] = "- 교회명: \n- 설교 제목 및 본문: \n- 광고 및 소식: \n\n위 정보를 바탕으로 따뜻한 주보 문구와 소식을 정리해 주세요."

    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("가장 똑똑한 Gemini 1.5 Pro 모델이 원고를 집필 중입니다..."):
                try:
                    # [업그레이드!] 1.5 Pro 모델 호출
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e: st.error(f"AI 응답 오류: {e}")
        else:
            st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown("<p style='font-weight:700; color:#1E3A8A; margin-top:20px;'>🖋️ 작성된 원고 내용</p>", unsafe_allow_html=True)
        # 줄바꿈 처리
        processed_text = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown('<div class="result-box">' + processed_text + '</div>', unsafe_allow_html=True)
        st.download_button("💾 원고 파일로 저장", st.session_state['res_txt'], file_name="CTS_AI_원고.txt", use_container_width=True)

with tab2:
    st.markdown("<p style='font-weight: 600; color: #334155;'>구글 최신 Imagen 3 모델이 고화질 이미지를 생성합니다.</p>", unsafe_allow_html=True)
    img_in = st.text_input("img", placeholder="예: 평화로운 숲속 예배당, 유화 스타일, 따뜻한 햇살", label_visibility="collapsed")
    
    if st.button("고품질 이미지 생성 시작 🎨", type="primary"):
        if img_in:
            with st.spinner("Imagen 3가 그림을 그리는 중입니다..."):
                try:
                    # 이미지 모델 호출
                    imagen_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    result = imagen_model.generate_images(prompt=img_in, number_of_images=1)
                    if result.images:
                        st.session_state['res_img_bytes'] = result.images[0].image_bytes
                except Exception as e: st.error(f"이미지 생성 실패: {e}")

    if 'res_img_bytes' in st.session_state:
        st.image(st.session_state['res_img_bytes'], use_container_width=True)
        st.download_button("💾 이미지 저장", st.session_state['res_img_bytes'], file_name="CTS_AI_이미지.png", mime="image/png", use_container_width=True)

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
