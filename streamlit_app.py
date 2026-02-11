import streamlit as st
import google.generativeai as genai

# 1. 페이지 및 레이아웃 설정
st.set_page_config(page_title="CTS AI 목회비서 Pro", page_icon="✝️", layout="wide")

# 2. 젠스파크(GenSpark) 스타일 & 모바일 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700&display=swap');
    
    /* 전체 기본 폰트 및 배경 */
    html, body, [class*="css"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        background-color: #FFFFFF !important; 
        color: #334155;
    }
    
    /* 컨테이너 중앙 정렬 (모바일 가독성 위함) */
    .block-container { 
        padding-top: 1.5rem !important; 
        padding-bottom: 3rem !important; 
        max-width: 800px; 
    }

    /* 탭 스타일링 */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: center; 
        gap: 10px; 
        border-bottom: 2px solid #F1F5F9; 
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] { 
        font-size: 1.1rem !important; 
        font-weight: 600; 
        color: #94A3B8; 
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        color: #1E3A8A !important; 
        border-bottom: 3px solid #1E3A8A !important; 
    }

    /* 버튼 스타일 공통 */
    div[data-testid="stHorizontalBlock"] button {
        width: 100% !important; 
        background-color: #F8FAFC !important;
        border-radius: 12px !important; 
        font-size: 1rem !important;
        font-weight: 600 !important; 
        height: 3.5rem !important;
        border: 1px solid #E2E8F0 !important; 
        color: #475569 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #1E3A8A !important;
        color: #1E3A8A !important;
        background-color: #EFF6FF !important;
    }

    /* 실행(Primary) 버튼 */
    .stButton>button[kind="primary"] {
        width: 100%; 
        border-radius: 12px; 
        background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%) !important;
        color: white !important; 
        height: 4rem !important; 
        font-size: 1.2rem !important;
        font-weight: 700; 
        margin-top: 20px; 
        border: none;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.2);
    }
    
    /* 링크 버튼 스타일 (2차 버튼) */
    a[kind="secondary"] {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 0.75rem;
        border-radius: 12px;
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FCD34D;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 10px;
        transition: all 0.2s;
    }
    a[kind="secondary"]:hover {
        background-color: #FEF3C7;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* 결과 박스 */
    .result-box {
        background-color: #F8FAFC; 
        padding: 25px; 
        border-radius: 16px;
        border: 1px solid #E2E8F0; 
        color: #334155; 
        line-height: 1.8; 
        font-size: 1.05rem; 
        margin-top: 25px;
    }
    
    /* 프롬프트 박스 */
    .prompt-box {
        background-color: #FFFBEB; 
        padding: 20px; 
        border-radius: 10px;
        border: 1px solid #FCD34D; 
        color: #92400E; 
        font-family: monospace; 
        font-size: 1rem;
        margin-bottom: 15px;
    }

    .footer { 
        text-align: center; 
        color: #CBD5E1; 
        font-size: 0.8rem; 
        margin-top: 4rem; 
        border-top: 1px solid #F1F5F9;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("설정(Secrets) 메뉴에서 GOOGLE_API_KEY를 입력해주세요.")

def get_best_model():
    """안정적인 모델 자동 선택"""
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-2.0-flash-exp' in models: return 'models/gemini-2.0-flash-exp' # 최신
        if 'models/gemini-1.5-pro' in models: return 'models/gemini-1.5-pro' # 고성능
        return 'models/gemini-1.5-flash' # 안정성
    except:
        return 'gemini-pro'

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 헤더
st.markdown("<h3 style='text-align: center; color: #1E3A8A; font-weight:800; margin-bottom:0;'>CTS AI 목회비서</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.9rem; margin-top:5px;'>콘텐츠지원국 제공 | Powered by Google Gemini</p>", unsafe_allow_html=True)

# 5. 메인 기능 탭
tab1, tab2 = st.tabs(["📝 목회 원고 작성", "🎨 AI 성화 도안(프롬프트)"])

# === TAB 1: 텍스트 생성 ===
with tab1:
    st.markdown("##### 📌 원하시는 작업을 선택하세요")
    
    # [Row 1]
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 설교 초안"): 
            st.session_state['p_input'] = "다음 정보를 바탕으로 3대지 설교 아웃라인을 작성해 주세요.\n\n- 본문: \n- 제목: \n- 청중: \n- 핵심 메시지: \n\n[구성 요청]\n1. 서론 (흥미로운 예화나 질문)\n2. 본론 (3가지 대지: 설명+예시+적용)\n3. 결론 (요약 및 결단 촉구)"
    with col2:
        if st.button("🙏 대표 기도"): 
            st.session_state['p_input'] = "다음 상황에 맞는 은혜롭고 간절한 대표기도문을 작성해 주세요.\n\n- 예배 종류(주일/수요/새벽): \n- 강조할 기도제목: \n- 시기(절기): \n\n*전통적인 한국 교회 기도 말투로 정중하게 작성해 주세요."
    with col3:
        if st.button("✍️ 목회 칼럼"): 
            st.session_state['p_input'] = "주보나 신문에 실을 따뜻한 목회 칼럼을 써주세요.\n\n- 주제: \n- 독자: 성도들\n- 분위기: 위로와 소망을 주는\n- 분량: 1000자 내외"

    # [Row 2]
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🏠 심방/상담"): 
            st.session_state['p_input'] = "성도님 상황에 맞는 위로의 말씀과 권면의 말을 추천해 주세요.\n\n- 성도 상황: \n- 고민 내용: \n\n1. 적절한 성경 구절 3개\n2. 위로의 메시지\n3. 짧은 기도문"
    with col5:
        if st.button("📢 주보/광고"): 
            st.session_state['p_input'] = "- 교회명: \n- 날짜: \n- 주요 행사: \n\n위 내용을 바탕으로 주보에 들어갈 환영 인사말과 광고 문구를 다듬어 주세요."
    with col6:
        if st.button("🧐 성경 연구"): 
            st.session_state['p_input'] = "다음 성경 본문에 대한 신학적 배경과 주요 주석 내용을 요약해 주세요.\n\n- 본문: \n- 궁금한 점: "

    user_text = st.text_area("내용을 입력하거나 수정하세요", value=st.session_state['p_input'], height=200)

    if st.button("AI 비서에게 요청하기 (작성 시작)", type="primary"):
        if user_text:
            with st.spinner("목사님의 의도를 파악하고 글을 작성 중입니다..."):
                try:
                    model = genai.GenerativeModel(get_best_model())
                    full_prompt = f"당신은 신실하고 지혜로운 AI 목회 비서입니다. 한국 교회의 정서를 고려하여 다음 요청을 처리해 주세요:\n\n{user_text}"
                    response = model.generate_content(full_prompt)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("내용을 입력해 주세요.")

    if 'res_txt' in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state["res_txt"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.download_button("💾 결과 저장하기", st.session_state['res_txt'], file_name="CTS_목회자료.txt", use_container_width=True)

# === TAB 2: 이미지 프롬프트 (나노바나나 연동) ===
with tab2:
    st.markdown("""
    <div style='background-color:#F0F9FF; padding:15px; border-radius:10px; border-left:5px solid #1E3A8A; margin-bottom:20px;'>
        <strong>💡 고품질 성화 제작 팁</strong><br>
        여기서 <strong>영어 명령어(프롬프트)</strong>를 받은 후, 아래 <strong>[나노바나나 프로]</strong> 버튼을 눌러 붙여넣으세요.
        훨씬 더 아름다운 그림이 나옵니다.
    </div>
    """, unsafe_allow_html=True)
    
    img_idea = st.text_input("어떤 그림이 필요하신가요?", placeholder="예: 갈릴리 호수 위를 걸으시는 예수님, 웅장한 유화 스타일")

    if st.button("최적의 영어 명령어 생성하기 ✨", type="primary", key="prompt_btn"):
        if img_idea:
            with st.spinner("전문 화가 스타일로 명령어를 변환 중입니다..."):
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
                    st.error(f"생성 실패: {e}")

    if 'final_prompt' in st.session_state:
        st.markdown("👇 **아래 영어 내용을 복사하세요**")
        st.code(st.session_state['final_prompt'], language="text")
        
        st.markdown("👇 **복사한 내용을 붙여넣으러 가기**")
        
        # 외부 링크 버튼 배치
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("🍌 나노바나나 프로 (Gemini) 실행", "https://gemini.google.com/", use_container_width=True)
        with c2:
            st.link_button("🎨 Google ImageFX 실행", "https://aitestkitchen.withgoogle.com/tools/image-fx", use_container_width=True)

st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
