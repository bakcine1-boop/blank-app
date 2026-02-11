import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="CTS AI 목회비서 (Premium)", page_icon="🙏", layout="wide")

# 2. 디자인 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #FFFFFF !important; }
    .block-container { padding-top: 0rem !important; padding-bottom: 2rem !important; max-width: 900px; }
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.15rem !important; font-weight: 700; color: #94A3B8; border: none !important; background-color: transparent !important; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 3px solid #1E3A8A !important; }
    /* 버튼 스타일 */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; background-color: #F8FAFC !important;
        border-radius: 12px !important; font-size: 1.1rem !important;
        font-weight: 600 !important; height: 3.8rem !important;
        border: 1px solid #E2E8F0 !important; color: #475569 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button[kind="primary"] {
        width: 100%; border-radius: 12px; background-color: #1E3A8A !important;
        color: white !important; height: 4rem !important; font-size: 1.3rem !important;
        font-weight: 700; margin-top: 20px; border: none; box-shadow: 0 4px 6px rgba(30, 58, 138, 0.2);
    }
    /* 결과 박스 스타일 */
    .result-box {
        background-color: #FFFFFF; padding: 30px; border-radius: 16px;
        border: 1px solid #E2E8F0; color: #334155; line-height: 1.9; font-size: 1.08rem; margin-top: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .footer { text-align: center; color: #CBD5E1; font-size: 0.85rem; margin-top: 4rem; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets에서 GOOGLE_API_KEY를 설정해주세요.")

# 텍스트 모델 우선순위 선택 함수
def get_best_text_model():
    try:
        # 사용 가능한 모델 리스트 확인
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 1순위: 나노바나나 (Gemini 2.0 Flash Exp)
        if 'models/gemini-2.0-flash-exp' in available_models:
            return 'models/gemini-2.0-flash-exp', "나노바나나(Gemini 2.0)"
        # 2순위: 프로 버전 (Gemini 1.5 Pro - 고성능)
        elif 'models/gemini-1.5-pro' in available_models:
            return 'models/gemini-1.5-pro', "Gemini 1.5 Pro"
        # 3순위: 플래시 버전 (Gemini 1.5 Flash - 빠름)
        else:
            return 'models/gemini-1.5-flash', "Gemini 1.5 Flash"
    except:
        # API 호출 실패 시 기본값
        return 'models/gemini-1.5-flash', "Gemini 1.5 Flash (기본)"

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성
tab1, tab2 = st.tabs(["📝 목회 원고 작성", "🎨 프리미엄 이미지 생성"])

# === TAB 1: 텍스트 생성 ===
with tab1:
    model_id, model_name = get_best_text_model()
    st.markdown(f"<p style='font-weight: 600; color: #64748B; margin-bottom: 10px;'>현재 적용 모델: <span style='color: #1E3A8A;'>{model_name}</span></p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 설교"): st.session_state['p_input'] = "- 본문 말씀: \n- 설교 주제: \n- 대상 청중: \n- 설교 시간: 약 30분\n\n위 정보를 바탕으로 설교 아웃라인을 만들어 주세요."
    with col2:
        if st.button("🙏 기도"): st.session_state['p_input'] = "- 기도 상황: \n- 기도 주제: \n\n위 상황에 맞는 경건한 기도문을 작성해 주세요."
    with col3:
        if st.button("📢 주보"): st.session_state['p_input'] = "- 교회명: \n- 날짜: \n\n주보에 들어갈 환영 인사와 광고 문구를 작성해 주세요."

    user_text = st.text_area("input", value=st.session_state['p_input'], height=250, label_visibility="collapsed")

    if st.button("AI 비서에게 요청하기", type="primary", key="text_btn"):
        if user_text:
            with st.spinner(f"{model_name}가 생각 중입니다..."):
                try:
                    model = genai.GenerativeModel(model_id)
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류 발생: {e}")
                    st.warning("잠시 후 다시 시도하거나, API 키를 확인해주세요.")
        else: st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown("<div class='result-box'>" + st.session_state['res_txt'].replace("\n", "<br>") + "</div>", unsafe_allow_html=True)

# === TAB 2: 프리미엄 이미지 생성 (나노바나나 기획 + Imagen3 채색) ===
with tab2:
    st.markdown("""
    <p style='font-weight: 600; color: #334155; font-size: 1.1rem;'>
    ✨ <span style='color: #1E3A8A;'>나노바나나의 기획</span>과 <span style='color: #1E3A8A;'>Imagen 3의 화풍</span>을 결합합니다.
    </p>
    <p style='color: #64748B; font-size: 0.95rem; margin-bottom: 20px;'>입력하신 내용을 바탕으로 최적의 프롬프트를 자동으로 생성하여 고품질 이미지를 만듭니다.</p>
    """, unsafe_allow_html=True)
    
    img_in = st.text_input("이미지 설명", placeholder="예: 따뜻한 햇살이 드는 시골 교회 풍경, 수채화 스타일", label_visibility="collapsed")

    if st.button("프리미엄 이미지 생성 시작 🎨", type="primary", key="img_btn"):
        if img_in:
            # 1단계: 프롬프트 엔지니어링 (나노바나나 또는 고성능 모델 사용)
            with st.spinner("1단계: 나노바나나가 멋진 그림 아이디어를 구상 중입니다... 🧠"):
                try:
                    planner_id, planner_name = get_best_text_model()
                    planner_model = genai.GenerativeModel(planner_id)
                    
                    # 나노바나나에게 상세한 영어 프롬프트 작성을 요청
                    prompt_request = f"""
                    너는 세계 최고의 AI 아트 디렉터야. 사용자의 요청을 바탕으로 Imagen 3 모델이 최상의 이미지를 생성할 수 있도록 아주 상세하고 묘사적인 영어 프롬프트를 작성해줘.
                    
                    사용자 요청: "{img_in}"
                    
                    필수 포함 요소:
                    1. 주요 피사체에 대한 아주 구체적인 묘사
                    2. 분위기, 조명, 색감에 대한 상세한 설명
                    3. 예술 스타일 (예: oil painting, cinematic photo, watercolor 등) 명시
                    4. 최고의 퀄리티를 위한 키워드 (예: masterpiece, highly detailed, 8k resolution)

                    오직 영어 프롬프트 문장만 출력해.
                    """
                    enhanced_prompt_resp = planner_model.generate_content(prompt_request)
                    enhanced_prompt = enhanced_prompt_resp.text
                    st.toast(f"✅ {planner_name}가 프롬프트 기획을 완료했습니다!", icon="🎉")
                    # (디버깅용) 실제 생성된 프롬프트 확인
                    # st.write(f"Debug (생성된 프롬프트): {enhanced_prompt}") 

                except Exception as e:
                    st.warning(f"기획 단계에서 문제가 발생하여 기본 입력으로 진행합니다. ({e})")
                    enhanced_prompt = img_in

            # 2단계: 이미지 생성 (Imagen 3 정식 모델 사용)
            with st.spinner("2단계: Imagen 3가 화폭에 그림을 담아내는 중입니다... 🖌️"):
                try:
                    imagen_model = genai.GenerativeModel("imagen-3.0-generate-001")
                    if hasattr(imagen_model, 'generate_images'):
                        result = imagen_model.generate_images(prompt=enhanced_prompt, number_of_images=1)
                        if result.images:
                            st.session_state['res_img_bytes'] = result.images[0].image_bytes
                            st.session_state['img_caption'] = f"Generated by Imagen 3 (Directed by {planner_name})"
                        else: raise Exception("이미지 생성 결과 없음")
                    else: raise Exception("Imagen 3 라이브러리 호환 문제")
                except Exception as e:
                     st.error(f"이미지 생성 실패: {e}")
                     st.info("잠시 후 다시 시도해주세요.")

    # 결과 표시
    if 'res_img_bytes' in st.session_state:
        st.image(st.session_state['res_img_bytes'], use_container_width=True, caption=st.session_state.get('img_caption', ''))

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
