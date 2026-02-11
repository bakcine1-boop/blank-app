import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (모바일 최적화)
st.set_page_config(page_title="AI 목회비서", page_icon="✝️", layout="wide")

# 2. 디자인 CSS (모바일 UI 강화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #FFFFFF !important; 
        color: #1E293B;
    }
    
    /* 헤더, 푸터, 메뉴 등 불필요한 요소 전면 숨김 */
    header, footer, #MainMenu, .stDeployButton {visibility: hidden !important;}

    /* 모바일 좌우 여백 확보 */
    .block-container { 
        padding: 1rem !important; 
        max-width: 100%;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: center; 
        gap: 15px; 
        border-bottom: 1px solid #E2E8F0; 
    }
    .stTabs [data-baseweb="tab"] { 
        font-size: 1rem !important; 
        font-weight: 600; 
        color: #64748B; 
        padding: 10px;
    }
    .stTabs [aria-selected="true"] { 
        color: #1E3A8A !important; 
        border-bottom: 2px solid #1E3A8A !important; 
    }

    /* 버튼 스타일 (터치하기 편하게) */
    .stButton>button[kind="primary"] {
        width: 100%; 
        border-radius: 12px; 
        background: #1E3A8A !important;
        color: white !important; 
        height: 3.5rem !important; 
        font-size: 1.1rem !important;
        font-weight: 700; 
        margin-top: 15px; 
        border: none;
    }
    
    /* 선택 상자 (Selectbox) 스타일 */
    div[data-baseweb="select"] { border-radius: 10px !important; }

    /* 결과 박스 */
    .result-box {
        background-color: #F8FAFC; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #E2E8F0; 
        color: #334155; 
        line-height: 1.7; 
        font-size: 1rem; 
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정 (핵심 수정: 무조건 작동하는 모델 자동 납치)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_surviving_model():
    """
    오류를 낼 바에야, 현재 서버 목록에 있는 아무 모델이나 잡아옵니다.
    """
    try:
        # 1. 서버가 가진 모델 리스트를 조회합니다.
        for m in genai.list_models():
            # 2. 'generateContent'(글쓰기) 기능이 있는 첫 번째 모델을 발견하면
            if 'generateContent' in m.supported_generation_methods:
                # 3. 그 녀석을 바로 반환하고 함수 종료 (이름을 따지지 않음)
                return m.name
        
        # 4. 만약 조회조차 안 되면 구버전의 왕 'gemini-pro'를 강제 호출
        return 'gemini-pro'
    except:
        return 'gemini-pro'

# 세션 상태 초기화
if 'p_input' not in st.session_state: st.session_state['p_input'] = ""
if 'last_mode' not in st.session_state: st.session_state['last_mode'] = ""

# 4. 앱 구성
tab1, tab2 = st.tabs(["📝 목회 원고", "🎨 성화 도안"])

# === TAB 1: 텍스트 생성 (드롭다운 메뉴 방식) ===
with tab1:
    menu = {
        "✨ 작업을 선택하세요": "",
        "📖 설교 초안": "다음 정보를 바탕으로 3대지 설교 아웃라인을 작성해 주세요.\n\n- 본문: \n- 제목: \n- 청중: \n- 핵심 메시지: \n\n[구성 요청]\n1. 서론 (예화/질문)\n2. 본론 (3대지: 설명+예시+적용)\n3. 결론 (요약+결단)",
        "🙏 대표 기도": "다음 상황에 맞는 은혜로운 대표기도문을 작성해 주세요.\n\n- 예배(주일/수요/새벽): \n- 기도제목: \n- 절기: \n\n*전통적이고 경건한 말투로 작성해 주세요.",
        "✍️ 목회 칼럼": "주보나 신문에 실을 목회 칼럼을 써주세요.\n\n- 주제: \n- 독자: \n- 분위기: 위로와 소망\n- 분량: 1000자 내외",
        "🏠 심방 권면": "심방 상황에 맞는 권면의 말씀과 기도를 작성해 주세요.\n\n- 성도 상황: \n- 고민: \n\n1. 성경구절 3개\n2. 권면 메시지\n3. 축복 기도",
        "📢 주보 광고": "- 교회명: \n- 날짜: \n- 행사: \n\n위 내용을 바탕으로 주보 환영 인사와 광고 문구를 작성해 주세요.",
        "🧐 성경 주석": "다음 본문의 신학적 배경과 주석을 요약해 주세요.\n\n- 본문: \n- 궁금한 점: "
    }

    mode = st.selectbox("작업 선택", list(menu.keys()), label_visibility="collapsed")

    if mode != st.session_state['last_mode']:
        if menu[mode]: st.session_state['p_input'] = menu[mode]
        st.session_state['last_mode'] = mode

    user_text = st.text_area("내용 입력", value=st.session_state['p_input'], height=200, placeholder="메뉴를 선택하거나 직접 입력하세요.")

    if st.button("AI 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 작성 중입니다..."):
                try:
                    # 여기서 '생존 모델'을 가져옵니다.
                    model_name = get_surviving_model()
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(f"당신은 목회 비서입니다.\n{user_text}")
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류: {e}")
                    st.caption("서버 연결이 불안정합니다. 잠시 후 다시 시도해주세요.")
        else: st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state["res_txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button("💾 저장하기", st.session_state['res_txt'], file_name="CTS_AI_Result.txt")

# === TAB 2: 성화 도안 ===
with tab2:
    st.info("💡 **팁:** 여기서 '영어 도안'을 만든 뒤, 아래 [Gemini 열기] 버튼을 눌러 붙여넣으세요.")
    idea = st.text_input("그림 아이디어 (한글)", placeholder="예: 갈릴리 호수 위를 걸으시는 예수님")
    
    if st.button("최적 도안 생성", type="primary"):
        if idea:
            with st.spinner("도안 생성 중..."):
                try:
                    planner = genai.GenerativeModel(get_surviving_model())
                    res = planner.generate_content(f"Role: Christian Art Director. Task: Convert '{idea}' to detailed English prompt. Output ONLY prompt.")
                    st.session_state['final_prompt'] = res.text
                except Exception as e: st.error(f"실패: {e}")

    if 'final_prompt' in st.session_state:
        st.code(st.session_state['final_prompt'], language="text")
        c1, c2 = st.columns(2)
        with c1: st.link_button("🍌 Gemini 열기", "https://gemini.google.com/app", use_container_width=True)
        with c2: st.link_button("🎨 ImageFX 열기", "https://aitestkitchen.withgoogle.com/tools/image-fx", use_container_width=True)

# 하단 여백
st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
