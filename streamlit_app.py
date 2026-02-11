import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 디자인 CSS (젠스파크 스타일 통합)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #FFFFFF !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 2rem !important; max-width: 900px; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; border-bottom: 1px solid #F1F5F9; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem !important; font-weight: 600; color: #64748B; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 3px solid #1E3A8A !important; }

    /* 가로 3단 버튼 스타일 (폰트 크기 통일) */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; background-color: #F8FAFC !important;
        border-radius: 10px !important; font-size: 1.1rem !important;
        font-weight: 600 !important; height: 3.5rem !important;
        border: 1px solid #E2E8F0 !important; color: #334155 !important;
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

# 3. 모델 설정 및 안전한 모델 감지 로직 (업그레이드 됨)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.info("Secrets에서 API 키를 먼저 확인해 주세요.")

def get_workable_model():
    """
    사용 가능한 모델 중 가장 고성능 모델을 우선순위로 선택합니다.
    1순위: Gemini 2.0 Flash (NanoBanana - 최신/고성능)
    2순위: Gemini 1.5 Pro (안정적 고성능)
    3순위: Gemini 1.5 Flash (빠름)
    """
    try:
        # 현재 API 키로 사용 가능한 모델 리스트 조회
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 우선순위 설정
        priority_models = [
            'models/gemini-2.0-flash-exp', # 나노바나나 (최신)
            'models/gemini-1.5-pro',       # 프로 (고성능)
            'models/gemini-1.5-flash'      # 플래시 (기존)
        ]
        
        for target in priority_models:
            if target in models: return target
            
        # 리스트에 없으면 첫 번째 모델 반환
        return models[0] if models else "gemini-2.0-flash-exp"
    except:
        # 조회 실패 시 최신 모델 강제 지정
        return "gemini-2.0-flash-exp"

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성
tab1, tab2 = st.tabs(["📝 목회 원고 작성", "🎨 이미지 생성"])

# === TAB 1: 텍스트 생성 (Gemini 2.0 적용) ===
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 설교"):
            st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 설교 아웃라인을 만들어 주세요.\n\n아웃라인 형식:\n1. 서론 (도입 질문 또는 이야기)\n2. 본론 (3개 포인트, 각 포인트에 설명+예시+적용)\n3. 결론 (요약 + 삶의 적용 + 기도)"
    with col2:
        if st.button("🙏 기도"):
            st.session_state['p_input'] = "- 기도 상황: \n- 기도 주제: \n- 기도 시간: 약 2분\n\n위 상황에 맞는 기도문을 작성해 주세요. 한국 교회 전통에 맞는 경건한 어투로 작성해 주세요."
    with col3:
        if st.button("📢 주보"):
            st.session_state['p_input'] = "- 교회명: \n- 이번 주일 날짜: \n- 설교 제목: \n- 본문 말씀: \n- 교회 행사/광고: \n\n위 정보를 바탕으로 주보 문구를 작성해 주세요.\n\n포함할 항목:\n1. 환영 인사\n2. 금주 말씀 묵상 가이드(3줄)\n3. 교회 소식/광고\n4. 이번 주 기도제목(3개)"

    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed")

    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("Gemini 2.0이 원고를 작성 중입니다..."):
                try:
                    model_name = get_workable_model()
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e: st.error(f"연결 오류: {e}")
        else: st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown("<p style='font-weight:700; color:#1E3A8A; margin-top:20px;'>🖋️ 작성 결과</p>", unsafe_allow_html=True)
        p_text = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown('<div class="result-box">' + p_text + '</div>', unsafe_allow_html=True)
        st.download_button("💾 파일로 저장", st.session_state['res_txt'], file_name="CTS_AI_원고.txt", use_container_width=True)


# === TAB 2: 이미지 생성 (나노바나나 적용) ===
with tab2:
    st.markdown("<p style='font-weight: 600; color: #334155;'>최신 Gemini (나노바나나) 모델이 이미지를 생성합니다.</p>", unsafe_allow_html=True)
    img_in = st.text_input("이미지 설명", placeholder="예: 평화로운 예배당, 따뜻한 수채화 스타일", label_visibility="collapsed")

    if st.button("이미지 생성 시작 🎨", type="primary"):
        if img_in:
            with st.spinner("나노바나나가 이미지를 그리는 중입니다... 🍌"):
                try:
                    # 1. 나노바나나 (Gemini 2.0 Flash Exp) 모델 설정
                    nano_model = genai.GenerativeModel("gemini-2.0-flash-exp")

                    # 2. 콘텐츠 생성 요청 (Gemini는 통합 모델이라 generate_content 사용)
                    response = nano_model.generate_content(img_in)

                    # 3. 응답에서 이미지 데이터 추출
                    image_found = False
                    if response.parts:
                        for part in response.parts:
                            # 인라인 데이터가 있고, 마임타입이 이미지인 경우
                            if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                                st.session_state['res_img_bytes'] = part.inline_data.data
                                # 이전 URL 방식 세션 정보 삭제 (충돌 방지)
                                if 'res_img_url' in st.session_state: del st.session_state['res_img_url']
                                image_found = True
                                break # 첫 번째 이미지만 사용

                    if not image_found:
                         # 모델이 텍스트만 반환하거나 이미지를 생성하지 못한 경우 예외 처리하여 대체 엔진으로 넘김
                         raise Exception("모델이 이미지를 반환하지 않았습니다.")

                except Exception as e:
                    # 4. 나노바나나 실패 시 대체 엔진 (Pollinations.ai)
                    st.warning(f"나노바나나 연결 불안정 ({e}). 대체 엔진을 사용합니다.")
                    encoded = img_in.replace(" ", "%20")
                    st.session_state['res_img_url'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                    # 이전 바이트 방식 세션 정보 삭제
                    if 'res_img_bytes' in st.session_state: del st.session_state['res_img_bytes']

    # 결과 표시 영역
    if 'res_img_bytes' in st.session_state:
        st.image(st.session_state['res_img_bytes'], use_container_width=True, caption="Gemini (NanoBanana) Generated Image")
    elif 'res_img_url' in st.session_state:
        st.image(st.session_state['res_img_url'], use_container_width=True, caption="[대체 엔진 사용] Pollinations AI")

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
