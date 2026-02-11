import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (모바일 친화적 설정)
st.set_page_config(page_title="AI 목회비서", page_icon="✝️", layout="wide")

# 2. 디자인 CSS (젠스파크 통합 & 모바일 최적화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #FFFFFF !important; 
        color: #1E293B;
    }
    
    /* 불필요한 헤더/푸터/메뉴 숨김 (앱처럼 보이게) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 모바일에서 좌우 여백 확보 */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100%;
    }

    /* 탭 스타일 (심플하게) */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: center; 
        gap: 15px; 
        border-bottom: 1px solid #E2E8F0; 
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-size: 1rem !important; 
        font-weight: 600; 
        color: #64748B; 
        padding: 10px 10px;
    }
    .stTabs [aria-selected="true"] { 
        color: #1E3A8A !important; 
        border-bottom: 2px solid #1E3A8A !important; 
    }

    /* 실행 버튼 (Primary) - 모바일 터치하기 좋게 높이 조정 */
    .stButton>button[kind="primary"] {
        width: 100%; 
        border-radius: 12px; 
        background: #1E3A8A !important;
        color: white !important; 
        height: 3.8rem !important; 
        font-size: 1.1rem !important;
        font-weight: 700; 
        margin-top: 15px; 
        border: none;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.2);
    }
    
    /* 선택 상자(Selectbox) 스타일링 */
    div[data-baseweb="select"] {
        border-radius: 10px !important;
    }

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
    
    /* 링크 버튼 스타일 */
    a { text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정 (안정성 최우선 로직)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_working_model():
    """
    서버 환경에 맞춰 작동 가능한 모델을 자동으로 찾아냅니다.
    최신(1.5 Flash)을 먼저 시도하고, 안 되면 표준(Pro)으로 연결합니다.
    """
    try:
        # 라이브러리에서 지원하는 모델 목록 조회
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 1순위: 1.5 Flash (최신/빠름)
        if 'models/gemini-1.5-flash' in available_models: return 'models/gemini-1.5-flash'
        # 2순위: 1.5 Pro (고성능)
        if 'models/gemini-1.5-pro' in available_models: return 'models/gemini-1.5-pro'
        # 3순위: Gemini Pro (가장 호환성 높음 - 404 에러 해결사)
        return 'gemini-pro'
    except:
        # 목록 조회조차 안 될 경우 가장 기본 이름 사용
        return 'gemini-pro'

# 세션 상태 초기화
if 'p_input' not in st.session_state: st.session_state['p_input'] = ""
if 'last_selected_mode' not in st.session_state: st.session_state['last_selected_mode'] = "직접 입력"

# 4. 앱 구성
tab1, tab2 = st.tabs(["📝 목회 원고", "🎨 성화 도안"])

# === TAB 1: 텍스트 생성 (모바일 최적화: 드롭다운 메뉴 방식) ===
with tab1:
    # 메뉴 데이터
    menu_options = {
        "✨ 작업을 선택하세요 (터치)": "",
        "📖 설교 초안 작성": "다음 정보를 바탕으로 3대지 설교 아웃라인을 작성해 주세요.\n\n- 본문: \n- 제목: \n- 청중: \n- 핵심 메시지: \n\n[구성 요청]\n1. 서론 (흥미로운 예화나 질문)\n2. 본론 (3가지 대지: 설명+예시+적용)\n3. 결론 (요약 및 결단 촉구)",
        "🙏 대표 기도문 작성": "다음 상황에 맞는 은혜롭고 간절한 대표기도문을 작성해 주세요.\n\n- 예배 종류(주일/수요/새벽): \n- 강조할 기도제목: \n- 시기(절기): \n\n*전통적인 한국 교회 기도 말투로 정중하게 작성해 주세요.",
        "✍️ 목회 칼럼 작성": "주보나 신문에 실을 따뜻한 목회 칼럼을 써주세요.\n\n- 주제: \n- 독자: 성도들\n- 분위기: 위로와 소망을 주는\n- 분량: 1000자 내외",
        "🏠 심방/상담 권면": "성도님 상황에 맞는 위로의 말씀과 권면의 말을 추천해 주세요.\n\n- 성도 상황: \n- 고민 내용: \n\n1. 적절한 성경 구절 3개\n2. 위로의 메시지\n3. 짧은 기도문",
        "📢 주보 광고 문구": "- 교회명: \n- 날짜: \n- 주요 행사: \n\n위 내용을 바탕으로 주보에 들어갈 환영 인사말과 광고 문구를 다듬어 주세요.",
        "🧐 성경 주석/해석": "다음 성경 본문에 대한 신학적 배경과 주요 주석 내용을 요약해 주세요.\n\n- 본문: \n- 궁금한 점: "
    }

    # 모바일에서 버튼 나열보다 훨씬 깔끔한 Selectbox 사용
    selected_mode = st.selectbox(
        "어떤 도움이 필요하신가요?", 
        list(menu_options.keys()),
        label_visibility="collapsed"
    )

    # 모드 변경 시 입력창 내용 업데이트
    if selected_mode != st.session_state['last_selected_mode']:
        if menu_options[selected_mode]: # 빈 값이 아닐 때만 업데이트
            st.session_state['p_input'] = menu_options[selected_mode]
        st.session_state['last_selected_mode'] = selected_mode

    # 입력창
    user_text = st.text_area(
        "내용을 입력해주세요", 
        value=st.session_state['p_input'], 
        height=200, 
        placeholder="위 메뉴에서 작업을 선택하면 서식이 자동으로 입력됩니다."
    )

    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("작성 중입니다..."):
                try:
                    # 스마트 모델 연결 (에러 자동 방지)
                    model_name = get_working_model()
                    model = genai.GenerativeModel(model_name)
                    
                    full_prompt = f"당신은 신실하고 지혜로운 AI 목회 비서입니다. 한국 교회의 정서를 고려하여 다음 요청을 처리해 주세요:\n\n{user_text}"
                    response = model.generate_content(full_prompt)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
                    st.caption("서버의 접속량이 많거나 일시적인 문제입니다. 잠시 후 다시 시도해주세요.")
        else:
            st.warning("내용을 입력해 주세요.")

    # 결과 출력
    if 'res_txt' in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state["res_txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button("💾 내용 저장하기", st.session_state['res_txt'], file_name="CTS_목회자료.txt", use_container_width=True)


# === TAB 2: 성화 도안 (모바일 최적화) ===
with tab2:
    st.info("💡 **사용법:** ① 아이디어 입력 → ② 영어 도안 생성 → ③ 아래 버튼 눌러서 그림 그리기")
    
    img_idea = st.text_input("그림 아이디어 (한글)", placeholder="예: 갈릴리 호수 위를 걸으시는 예수님")

    if st.button("최적의 도안(프롬프트) 생성", type="primary"):
        if img_idea:
            with st.spinner("전문가 스타일로 변환 중..."):
                try:
                    model_name = get_working_model()
                    planner = genai.GenerativeModel(model_name)
                    prompt_req = f"Role: Expert Christian Art Director. Task: Convert '{img_idea}' into a highly detailed English image prompt. Output ONLY the English prompt."
                    resp = planner.generate_content(prompt_req)
                    st.session_state['final_prompt'] = resp.text
                except Exception as e:
                    st.error(f"실패: {e}")

    if 'final_prompt' in st.session_state:
        st.markdown("👇 **생성된 영어 도안 (복사하세요)**")
        st.code(st.session_state['final_prompt'], language="text")
        
        st.markdown("👇 **그림 도구 열기**")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🍌 Gemini 열기", "https://gemini.google.com/app", use_container_width=True)
        with col2:
            st.link_button("🎨 ImageFX 열기", "https://aitestkitchen.withgoogle.com/tools/image-fx", use_container_width=True)

# 하단 여백 확보
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
