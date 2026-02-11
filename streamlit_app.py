import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (최소화)
st.set_page_config(page_title="AI Assistant", page_icon="✝️", layout="wide")

# 2. 젠스파크 통합 디자인 (심플 & 모던)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 기본 배경 및 폰트 - 젠스파크와 일체화 */
    html, body, [class*="css"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #FFFFFF !important; 
        color: #1E293B;
    }
    
    /* 상단 여백 제거 (임베드 시 붕 뜨는 현상 방지) */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 100%;
    }

    /* 기본 헤더/푸터 숨김 (완전 심플하게) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* 탭 스타일 (깔끔한 라인 형태) */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: flex-start; /* 왼쪽 정렬로 변경하여 자연스럽게 */
        gap: 20px; 
        border-bottom: 1px solid #E2E8F0; 
        padding-bottom: 0px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-size: 1rem !important; 
        font-weight: 600; 
        color: #64748B; 
        padding: 10px 0px;
        background-color: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] { 
        color: #1E3A8A !important; 
        border-bottom: 2px solid #1E3A8A !important; 
    }

    /* 기능 버튼 그리드 */
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem !important; }
    
    /* 바로가기 버튼들 (카드 형태) */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; 
        background-color: #F8FAFC !important;
        border-radius: 8px !important; 
        font-size: 0.95rem !important;
        font-weight: 500 !important; 
        height: 3.2rem !important;
        border: 1px solid #E2E8F0 !important; 
        color: #334155 !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #1E3A8A !important;
        color: #1E3A8A !important;
        background-color: #EFF6FF !important;
    }

    /* 실행(Primary) 버튼 - CTS 블루 */
    .stButton>button[kind="primary"] {
        width: 100%; 
        border-radius: 8px; 
        background: #1E3A8A !important;
        color: white !important; 
        height: 3.5rem !important; 
        font-size: 1.1rem !important;
        font-weight: 700; 
        margin-top: 10px; 
        border: none;
    }

    /* 결과 박스 (종이 질감) */
    .result-box {
        background-color: #F8FAFC; 
        padding: 20px; 
        border-radius: 12px;
        border: 1px solid #E2E8F0; 
        color: #334155; 
        line-height: 1.7; 
        font-size: 1rem; 
        margin-top: 15px;
    }
    
    /* 프롬프트 박스 (강조) */
    .prompt-box {
        background-color: #FFF7ED; 
        padding: 15px; 
        border-radius: 8px;
        border: 1px solid #FED7AA; 
        color: #9A3412; 
        font-family: monospace; 
        font-size: 0.95rem;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정 (안정성 확보)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_best_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-2.0-flash-exp' in models: return 'models/gemini-2.0-flash-exp'
        if 'models/gemini-1.5-pro' in models: return 'models/gemini-1.5-pro'
        return 'models/gemini-1.5-flash'
    except:
        return 'gemini-pro'

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 앱 구성 (타이틀 제거, 탭 바로 시작)
tab1, tab2 = st.tabs(["📝 목회 원고 작성", "🎨 성화(이미지) 도안"])

# === TAB 1: 텍스트 생성 ===
with tab1:
    # 버튼 그리드 (3열 x 2행)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📖 설교 초안"): 
            st.session_state['p_input'] = "다음 정보를 바탕으로 3대지 설교 아웃라인을 작성해 주세요.\n\n- 본문: \n- 제목: \n- 청중: \n- 핵심 메시지: \n\n[구성 요청]\n1. 서론 (흥미로운 예화나 질문)\n2. 본론 (3가지 대지: 설명+예시+적용)\n3. 결론 (요약 및 결단 촉구)"
    with c2:
        if st.button("🙏 대표 기도"): 
            st.session_state['p_input'] = "다음 상황에 맞는 은혜롭고 간절한 대표기도문을 작성해 주세요.\n\n- 예배 종류(주일/수요/새벽): \n- 강조할 기도제목: \n- 시기(절기): \n\n*전통적인 한국 교회 기도 말투로 정중하게 작성해 주세요."
    with c3:
        if st.button("✍️ 목회 칼럼"): 
            st.session_state['p_input'] = "주보나 신문에 실을 따뜻한 목회 칼럼을 써주세요.\n\n- 주제: \n- 독자: 성도들\n- 분위기: 위로와 소망을 주는\n- 분량: 1000자 내외"

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🏠 심방 권면"): 
            st.session_state['p_input'] = "성도님 상황에 맞는 위로의 말씀과 권면의 말을 추천해 주세요.\n\n- 성도 상황: \n- 고민 내용: \n\n1. 적절한 성경 구절 3개\n2. 위로의 메시지\n3. 짧은 기도문"
    with c5:
        if st.button("📢 주보 광고"): 
            st.session_state['p_input'] = "- 교회명: \n- 날짜: \n- 주요 행사: \n\n위 내용을 바탕으로 주보에 들어갈 환영 인사말과 광고 문구를 다듬어 주세요."
    with c6:
        if st.button("🧐 성경 주석"): 
            st.session_state['p_input'] = "다음 성경 본문에 대한 신학적 배경과 주요 주석 내용을 요약해 주세요.\n\n- 본문: \n- 궁금한 점: "

    user_text = st.text_area("내용 입력", value=st.session_state['p_input'], height=180, label_visibility="collapsed", placeholder="원하는 버튼을 누르거나 내용을 직접 입력하세요.")

    if st.button("작성 요청하기", type="primary"):
        if user_text:
            with st.spinner("작성 중입니다..."):
                try:
                    model = genai.GenerativeModel(get_best_model())
                    full_prompt = f"당신은 신실하고 지혜로운 AI 목회 비서입니다. 한국 교회의 정서를 고려하여 다음 요청을 처리해 주세요:\n\n{user_text}"
                    response = model.generate_content(full_prompt)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류: {e}")
        else:
            st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state["res_txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button("💾 텍스트 저장", st.session_state['res_txt'], file_name="CTS_목회자료.txt", use_container_width=True)

# === TAB 2: 이미지 프롬프트 & 외부 링크 ===
with tab2:
    st.info("💡 **사용법:** ① 아이디어 입력 → ② 영어 명령어 생성 → ③ 아래 '나노바나나' 버튼 눌러 붙여넣기")
    
    img_idea = st.text_input("그림 아이디어 (한글)", placeholder="예: 갈릴리 호수 위를 걸으시는 예수님, 웅장한 유화 스타일")

    if st.button("최적의 영어 명령어(프롬프트) 만들기 ✨", type="primary"):
        if img_idea:
            with st.spinner("전문가 스타일로 변환 중..."):
                try:
                    planner = genai.GenerativeModel(get_best_model())
                    prompt_req = f"""
                    Role: Expert Christian Art Director.
                    Task: Convert user's idea into a highly detailed English image prompt.
                    User Input: "{img_idea}"
                    Requirements: Biblical accuracy, reverent atmosphere, Detailed lighting, High quality keywords.
                    Output ONLY the English prompt.
                    """
                    resp = planner.generate_content(prompt_req)
                    st.session_state['final_prompt'] = resp.text
                except Exception as e:
                    st.error(f"실패: {e}")

    if 'final_prompt' in st.session_state:
        st.markdown("👇 **생성된 명령어 (복사하세요)**")
        st.code(st.session_state['final_prompt'], language="text")
        
        st.markdown("---")
        st.markdown("👇 **복사한 명령어로 그림 그리기 (외부 도구 연결)**")
        
        # [나노바나나] 및 [ImageFX] 링크 버튼
        col_link1, col_link2 = st.columns(2)
        with col_link1:
            st.link_button("🍌 Gemini (나노바나나) 열기", "https://gemini.google.com/app", use_container_width=True)
            st.caption("채팅창에 붙여넣고 '그려줘'라고 하세요.")
        with col_link2:
            st.link_button("🎨 Google ImageFX 열기", "https://aitestkitchen.withgoogle.com/tools/image-fx", use_container_width=True)
            st.caption("구글의 이미지 전용 생성 도구입니다.")

# 푸터 제거됨 (깔끔한 마무리를 위해 빈 공간만 살짝 둠)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
