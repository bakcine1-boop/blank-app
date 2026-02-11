import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (반응형 최적화)
st.set_page_config(page_title="AI 목회비서", page_icon="🙏", layout="wide")

# 2. 젠스파크의 '타이트한 여백'과 '세련된 네이비'를 구현하는 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 전체 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8FAFC !important;
    }

    /* 젠스파크 스타일: 상단 및 요소 간 여백 강제 축소 */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important; 
        max-width: 900px; /* 너무 퍼지지 않게 폭 제한 */
    }
    
    /* 카드 디자인: 아주 얇은 테두리와 정갈한 여백 */
    .st-emotion-cache-12w0qpk, .service-card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    /* 탭 디자인: 젠스파크 네비게이션 스타일 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 500; color: #64748B; border: none; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom: 2px solid #1E3A8A !important; font-weight: 700; }

    /* 수평 버튼(템플릿) 스타일: 알약 모양(Pill) */
    div[data-testid="column"] button {
        background-color: #F1F5F9 !important;
        color: #1E3A8A !important;
        border: 1px solid #E2E8F0 !important;
        height: 2.2rem !important;
        font-size: 0.85rem !important;
        border-radius: 20px !important;
        margin-bottom: 0px !important;
    }
    
    /* 메인 실행 버튼 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3rem;
        font-weight: 600;
        border: none;
        margin-top: 0.5rem;
    }

    /* 여백 조절용 */
    .tight-text { margin-bottom: -1rem; font-weight: 700; color: #1E3A8A; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 및 상태 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets 설정에서 API 키를 확인해 주세요.")
    st.stop()

if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 메인 탭 구성
tab1, tab2 = st.tabs(["📄 설교 및 칼럼 작성", "🖼️ 이미지 생성"])

with tab1:
    # 젠스파크의 컴팩트한 레이아웃 재현
    st.markdown('<p class="tight-text">사역 요청 내용을 선택하거나 입력해 주세요.</p>', unsafe_allow_html=True)
    
    # [변경 사항] 템플릿 버튼을 가로로 3등분 배치
    c1, c2, c3 = st.columns(3)
    if c1.button("📖 설교 초안"): st.session_state['p_input'] = "마태복음 5:13-16 본문의 설교 초안을 작성해줘."
    if c2.button("✍️ 목회 칼럼"): st.session_state['p_input'] = "'진정한 감사'를 주제로 성도들을 위한 칼럼을 작성해줘."
    if c3.button("🙏 중보 기도문"): st.session_state['p_input'] = "고난받는 환우들을 위한 위로의 기도문을 작성해줘."

    user_text = st.text_area("input", value=st.session_state['p_input'], height=200, label_visibility="collapsed", placeholder="여기에 직접 내용을 입력하실 수도 있습니다.")
    
    if st.button("AI 비서에게 요청하기"):
        if user_text:
            with st.spinner("내용 구성 중..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_text)
                st.session_state['res_txt'] = response.text
        else:
            st.warning("내용을 입력해 주세요.")

    # 결과창 및 다운로드 기능 (편의 기능 유지)
    if 'res_txt' in st.session_state:
        st.markdown('<div class="service-card">' + st.session_state['res_txt'] + '</div>', unsafe_allow_html=True)
        st.download_button("💾 결과물 파일 저장", st.session_state['res_txt'], file_name="목회지원자료.txt")

with tab2:
    st.markdown('<p class="tight-text">이미지 생성 설명</p>', unsafe_allow_html=True)
    img_in = st.text_input("img", placeholder="예: 평화로운 호숫가에서 기도하는 예수님, 수채화풍", label_visibility="collapsed")
    
    if st.button("이미지 생성 시작"):
        if img_in:
            with st.spinner("그리는 중..."):
                encoded = img_in.replace(" ", "%20")
                st.session_state['res_img'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
        else:
            st.warning("설명을 입력해 주세요.")

    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True, caption="마우스 우클릭으로 저장 가능")

# 5. 미니멀 푸터
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.75rem; margin-top: 2rem;'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)
