import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 (브라우저 탭 이름 및 레이아웃)
st.set_page_config(
    page_title="CTS 미디어목회지원센터 | AI 비서", 
    page_icon="✝️", 
    layout="wide"
)

# 2. 젠스파크(Genspark)의 세련된 디자인을 그대로 재현하는 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 전체 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA !important;
        color: #1F2937;
    }

    /* 상단 헤더: 젠스파크의 깊고 신뢰감 있는 네이비 */
    .stApp header { background-color: rgba(0,0,0,0); }
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
        padding: 3rem 1rem;
        border-radius: 0 0 24px 24px;
        color: white;
        text-align: center;
        margin-top: -6rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.2);
    }

    /* 모바일 반응형 디자인 미세 조정 */
    @media (max-width: 768px) {
        .main-header { padding: 2rem 1rem; border-radius: 0 0 15px 15px; }
        .main-header h2 { font-size: 1.5rem !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.9rem !important; padding: 10px 15px !important; }
    }

    /* 카드형 컨테이너 스타일 */
    .content-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }

    /* 탭 스타일 최적화 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom-color: #1E3A8A !important; font-weight: 700; }

    /* 버튼: 젠스파크 버튼 톤으로 통일 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A !important;
        color: white !important;
        border: none;
        height: 3.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #172554 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 입력창 디자인 */
    .stTextArea textarea { border-radius: 8px; border: 1px solid #D1D5DB; }
    .stTextInput input { border-radius: 8px; border: 1px solid #D1D5DB; }
    </style>
    """, unsafe_allow_html=True)

# 3. API 키 설정 (보안)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ 설정(Secrets)에서 GOOGLE_API_KEY를 확인해 주세요.")
    st.stop()

# 4. 상단 브랜딩 영역
st.markdown("""
    <div class="main-header">
        <h2 style='color: white; margin: 0; font-weight: 700; letter-spacing: -0.03em;'>CTS 미디어목회지원센터</h2>
        <p style='margin-top: 0.6rem; opacity: 0.85; font-size: 1.1rem;'>콘텐츠지원국 전용 AI 목회 지원 시스템</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 레이아웃
tab1, tab2 = st.tabs(["📄 설교 및 칼럼 구성", "🖼️ 목회 시각자료 생성"])

# --- 탭 1: 텍스트 생성 ---
with tab1:
    col_in, col_out = st.columns([1, 1], gap="large")
    
    with col_in:
        st.markdown('<div class="content-card"><strong>📝 작성 요청</strong><br><small style="color: #6B7280;">성경 본문이나 주제를 자유롭게 입력해 주세요.</small></div>', unsafe_allow_html=True)
        user_input = st.text_area("input", height=300, label_visibility="collapsed", placeholder="예: 마태복음 5:13-16을 본문으로 '세상의 소금과 빛' 설교 초안을 작성해 주세요.")
        
        if st.button("내용 구성 시작"):
            if user_input:
                with st.spinner("내용을 구성하고 있습니다..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content(user_input)
                        st.session_state['text_res'] = response.text
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
            else:
                st.warning("작성할 내용을 먼저 입력해 주세요.")

    with col_out:
        if 'text_res' in st.session_state:
            st.markdown("### 생성 결과")
            st.write(st.session_state['text_res'])
            st.divider()
            with st.expander("결과 텍스트 복사"):
                st.code(st.session_state['text_res'], language="markdown")
        else:
            st.markdown("<div style='text-align: center; color: #9CA3AF; padding-top: 10rem;'>왼쪽에서 입력 후 버튼을 누르면 결과가 표시됩니다.</div>", unsafe_allow_html=True)

# --- 탭 2: 이미지 생성 ---
with tab2:
    col_img_in, col_img_out = st.columns([1, 1], gap="large")
    
    with col_img_in:
        st.markdown('<div class="content-card"><strong>🎨 이미지 생성</strong><br><small style="color: #6B7280;">설교 배경이나 예화 이미지를 설명해 주세요.</small></div>', unsafe_allow_html=True)
        img_prompt = st.text_input("설명", placeholder="예: 평화로운 호숫가에서 기도하는 모습")
        img_style = st.selectbox("스타일 선택", ["유화", "수채화", "일러스트", "시네마틱", "실사"])
        
        if st.button("이미지 생성 실행"):
            if img_prompt:
                with st.spinner("이미지를 그리는 중입니다..."):
                    encoded_prompt = f"{img_prompt}, {img_style} style".replace(" ", "%20")
                    st.session_state['img_res'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
                    time.sleep(1)

    with col_img_out:
        if 'img_res' in st.session_state:
            st.image(st.session_state['img_res'], use_container_width=True, caption="생성된 이미지")
            st.success("이미지가 생성되었습니다. 마우스 우클릭으로 저장하실 수 있습니다.")
        else:
            st.markdown("<div style='text-align: center; color: #9CA3AF; padding-top: 10rem;'>생성된 이미지가 여기에 표시됩니다.</div>", unsafe_allow_html=True)

# 6. 하단 푸터 (젠스파크 하단과 유사하게 정돈)
st.markdown("""
    <br><br><hr>
    <div style='text-align: center; color: #6B7280; font-size: 0.85rem; padding-bottom: 2rem;'>
        CTS Media Ministry Center | 콘텐츠지원국 국장 전용 시스템<br>
        © 2026 Christian Television System. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

# 6. 하단
