import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (반응형 최적화)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="🙏", layout="wide")

# 2. 모바일/반응형 최적화 CSS (젠스파크 스타일 통합)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF !important;
    }

    /* 컨테이너 설정: 모바일 여백 최소화 */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 850px; 
    }
    
    /* 탭 메뉴: 터치 친화적 디자인 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 10px; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem !important; padding: 10px 15px !important; }

    /* 템플릿 버튼: 모바일에서 큼직하게 정렬 */
    div[data-testid="column"] button {
        width: 100% !important;
        background-color: #F8FAFC !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        margin-bottom: 8px !important;
        height: 3rem !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* 메인 실행 버튼: CTS 브랜드 네이비 */
    .stButton>button[kind="primary"] {
        width: 100%;
        border-radius: 12px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3.8rem !important;
        font-size: 1.2rem !important;
        font-weight: 700;
        border: none;
    }

    /* 결과창 카드: 가독성 중심 */
    .result-card {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #1E3A8A;
        font-size: 1rem;
        line-height: 1.8;
        color: #1E293B;
        margin-top: 1rem;
    }

    .footer {
        text-align: center; 
        color: #94A3B8; 
        font-size: 0.8rem; 
        margin-top: 3rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 모델 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.warning("⚠️ Streamlit Cloud의 Secrets 설정에서 'GOOGLE_API_KEY'를 입력해 주세요.")

# 세션 상태 초기화 (입력값 유지용)
if 'p_input' not in st.session_state: st.session_state['p_input'] = ""

# 4. 메인 콘텐츠 상단
st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-bottom: 20px;'>💡 AI 목회 지원 센터</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 설교/칼럼 작성", "🎨 이미지 생성"])

with tab1:
    # 템플릿 버튼 배치
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 설교 초안"): st.session_state['p_input'] = "오늘 본문은 [성경구절]입니다. 성도들이 큰 은혜를 받을 수 있는 3대지 설교 개요와 핵심 메시지를 작성해줘."
        if st.button("✍️ 목회 칼럼"): st.session_state['p_input'] = "[주제]를 바탕으로 성도들에게 따뜻한 위로와 격려를 전하는 목회 칼럼을 정성껏 써줘."
    with col2:
        if st.button("🙏 중보 기도문"): st.session_state['p_input'] = "질병으로 고통받는 환우들과 경제적으로 어려운 성도들을 위한 간절한 중보 기도문을 작성해줘."
        if st.button("📢 주보 소식"): st.session_state['p_input'] = "이번 주 우리 교회의 주요 사역 소식을 성도들이 읽기 편하게 주보용 문구로 요약해줘."

    # 입력창
    user_text = st.text_area("input", value=st.session_state['p_input'], height=200, label_visibility="collapsed", placeholder="여기에 직접 사역 내용을 입력하셔도 됩니다.")
    
    if st.button("AI 비서에게 요청하기", type="primary"):
        if user_text:
            with st.spinner("AI가 내용을 정성껏 구성하고 있습니다..."):
                try:
                    # 제미나이 1.5 플래시 모델 사용
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_text)
                    st.session_state['res_txt'] = response.text
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("내용을 입력해 주세요.")

    # 결과 출력 (SyntaxError 해결: 변수 선언 후 HTML 출력)
    if 'res_txt' in st.session_state:
        # 줄바꿈 문자를 HTML 태그로 변환 (f-string 에러 방지를 위해 변수로 따로 처리)
        processed_text = st.session_state['res_txt'].replace("\n", "<br>")
        st.markdown(f'<div class="result-card">{processed_text}</div>', unsafe_allow_html=True)
        
        # 다운로드 버튼
        st.download_button(
            label="💾 결과물 텍스트 저장하기",
            data=st.session_state['res_txt'],
            file_name="CTS_AI_목회지원자료.txt",
            mime="text/plain",
            use_container_width=True
        )

with tab2:
    st.markdown("<p style='font-weight: 600; color: #334155;'>생성할 이미지에 대한 설명을 입력하세요.</p>", unsafe_allow_html=True)
    img_in = st.text_input("img", placeholder="예: 평화로운 호숫가에서 기도하는 예수님, 부드러운 수채화 스타일", label_visibility="collapsed")
    
    if st.button("이미지 생성 시작", type="primary"):
        if img_in:
            with st.spinner("이미지를 그리는 중입니다..."):
                # URL 인코딩 처리
                encoded_prompt = img_in.replace(" ", "%20")
                st.session_state['res_img'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&width=1024&height=1024"
        else:
            st.warning("이미지 설명을 입력해 주세요.")

    if 'res_img' in st.session_state:
        st.image(st.session_state['res_img'], use_container_width=True, caption="마우스 우클릭 혹은 길게 눌러 이미지 저장 가능")

# 푸터 (CTS 정체성 반영)
st.markdown("<div class='footer'>CTS Media Ministry Center © 2026 | 콘텐츠지원국</div>", unsafe_allow_html=True)
