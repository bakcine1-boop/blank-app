import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 (모바일 최적화 및 와이드 레이아웃)
st.set_page_config(
    page_title="AI 목회비서", 
    page_icon="🙏", 
    layout="wide"
)

# 2. 젠스파크 스타일의 정갈한 디자인 (네이비 & 화이트)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF;
    }

    /* 상단 헤더: 깔끔하고 신뢰감 있는 톤 */
    .main-header {
        background-color: #1E3A8A;
        padding: 2.5rem 1rem;
        border-radius: 0 0 15px 15px;
        color: white;
        text-align: center;
        margin-top: -6rem;
        margin-bottom: 2rem;
    }

    /* 카드형 디자인: 목사님들이 읽기 편한 넉넉한 여백 */
    .service-card {
        background-color: #F9FAFB;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }

    /* 버튼 스타일: 직관적이고 정중한 색상 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 500;
        border: none;
    }

    /* 탭 디자인: 선명하고 단순하게 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 30px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; height: 50px; }
    
    /* 모바일 글자 크기 조정 */
    @media (max-width: 640px) {
        .main-header h1 { font-size: 1.8rem !important; }
        .stTabs [data-baseweb="tab"] { font-size: 1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API 보안 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("시스템 설정에서 API 키를 찾을 수 없습니다. (Secrets 설정을 확인해주세요)")
    st.stop()

# 4. 상단 헤더 (불필요한 문구 삭제)
st.markdown("""
    <div class="main-header">
        <h1 style='color: white; margin: 0; font-weight: 700;'>AI 목회비서</h1>
        <p style='margin-top: 0.5rem; opacity: 0.9;'>말씀 묵상과 사역의 도구</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 기능 (탭으로 분리하여 한 화면에서 해결)
tab1, tab2 = st.tabs(["📝 설교 및 칼럼 작성", "🎨 나노바나나 이미지 생성"])

with tab1:
    st.markdown('<div class="service-card"><strong>묵상하신 주제나 성경 본문을 아래에 적어주세요.</strong></div>', unsafe_allow_html=True)
    
    # 입력과 결과창을 세로로 배치하여 모바일 직관성 향상
    user_topic = st.text_area(
        "내용 입력",
        height=200,
        label_visibility="collapsed",
        placeholder="예: 마태복음 5:13-16을 본문으로 '세상의 소금과 빛' 설교 초안을 작성해줘."
    )
    
    if st.button("설교 초안 작성하기"):
        if user_topic:
            with st.spinner("AI 비서가 내용을 정리하고 있습니다..."):
                try:
                    # 빠른 응답을 위해 1.5 Flash 모델 사용
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_topic)
                    
                    st.markdown("---")
                    st.markdown("### 📖 작성된 결과")
                    st.write(response.text)
                    st.divider()
                    with st.expander("내용 복사하기"):
                        st.code(response.text, language="markdown")
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("먼저 내용을 입력해 주세요.")

with tab2:
    st.markdown('<div class="service-card"><strong>설교 화면에 사용할 이미지를 설명해 주세요.</strong></div>', unsafe_allow_html=True)
    
    img_prompt = st.text_input("그림 설명", placeholder="예: 평화로운 호숫가에서 기도하는 모습, 유화 스타일")
    
    if st.button("이미지 생성하기"):
        if img_prompt:
            with st.spinner("이미지를 생성하는 중입니다..."):
                # 나노바나나(Pollinations 기반) 엔진 유지
                encoded = img_prompt.replace(" ", "%20")
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                
                time.sleep(1) # 부드러운 전환을 위한 지연
                st.image(img_url, use_container_width=True)
                st.success("이미지가 완성되었습니다. 마우스 우클릭으로 저장해 주세요.")
        else:
            st.warning("이미지에 대한 설명을 입력해 주세요.")

# 6. 하단 푸터 (깔끔하게 정돈)
st.markdown("<br><br><div style='text-align: center; color: #9CA3AF; font-size: 0.8rem;'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)
