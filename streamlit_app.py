import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정: 젠스파크처럼 넓고 깨끗한 레이아웃
st.set_page_config(
    page_title="CTS 미디어목회지원센터", 
    page_icon="✝️", 
    layout="wide"
)

# 2. 젠스파크 스타일의 커스텀 CSS (신뢰감 있는 네이비 & 그레이)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFFFFF;
    }

    /* 상단 헤더: 깊은 네이비색으로 무게감 부여 */
    .main-header {
        background-color: #1E3A8A;
        padding: 2.5rem 1rem;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-top: -6rem;
        margin-bottom: 2rem;
    }

    /* 탭 디자인: 차분한 텍스트 중심 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 40px;
        justify-content: center;
        border-bottom: 1px solid #E5E7EB;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        font-weight: 500;
        font-size: 1.1rem;
        color: #6B7280;
    }
    .stTabs [aria-selected="true"] {
        color: #1E3A8A !important;
        border-bottom-color: #1E3A8A !important;
    }

    /* 버튼 디자인: 빨간색/이모티콘 제거, 전문적인 네이비 톤 */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        background-color: #1E3A8A !important;
        color: white !important;
        border: none;
        height: 3rem;
        font-size: 1rem;
        font-weight: 500;
    }

    /* 카드 스타일 레이아웃 */
    .content-box {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API 키 설정 (구글 제미나이 전용)
# Secrets 탭에 GOOGLE_API_KEY = "AIza..." 형식으로 입력되어야 합니다.
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ 설정(Secrets)에서 GOOGLE_API_KEY를 찾을 수 없습니다.")
    st.stop()

# 4. 상단 브랜딩 영역
st.markdown("""
    <div class="main-header">
        <h2 style='color: white; margin: 0; font-weight: 600; letter-spacing: -0.05em;'>CTS 미디어목회지원센터</h2>
        <p style='font-size: 1rem; opacity: 0.8; margin-top: 0.4rem;'>콘텐츠지원국 전용 AI 목회 지원 솔루션</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 기능 탭
tab_text, tab_image = st.tabs(["설교 및 칼럼 구성", "목회 이미지 생성"])

# --- 탭 1: 설교 및 칼럼 작성 ---
with tab_text:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    
    with col_in:
        st.markdown('<div class="content-box"><strong>작성 요청</strong><br><small>주제나 성경 본문을 입력해 주세요.</small></div>', unsafe_allow_html=True)
        user_input = st.text_area(
            "입력창",
            height=350,
            label_visibility="collapsed",
            placeholder="예: 마태복음 5:13-16을 본문으로 '세상의 소금과 빛' 설교 초안을 작성해 주세요."
        )
        
        if st.button("내용 생성"):
            if user_input:
                with st.spinner("내용을 구성 중입니다..."):
                    try:
                        # 제미나이 1.5 Pro 모델 사용
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content(user_input)
                        st.session_state['gemini_res'] = response.text
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
            else:
                st.warning("내용을 입력해 주세요.")

    with col_out:
        if 'gemini_res' in st.session_state:
            st.markdown("### 생성 결과")
            st.write(st.session_state['gemini_res'])
            st.divider()
            with st.expander("텍스트 복사"):
                st.code(st.session_state['gemini_res'], language="markdown")
        else:
            st.markdown("<div style='text-align: center; color: #94A3B8; padding-top: 10rem;'>결과가 여기에 표시됩니다.</div>", unsafe_allow_html=True)

# --- 탭 2: 이미지 생성 ---
with tab_image:
    col_img_in, col_img_out = st.columns([1, 1.2], gap="large")
    
    with col_img_in:
        st.markdown('<div class="content-box"><strong>이미지 생성</strong><br><small>설교 배경 등을 설명해 주세요.</small></div>', unsafe_allow_html=True)
        img_prompt = st.text_input("그림 설명", placeholder="예: 평화로운 들판을 걷는 목자, 수채화 스타일")
        img_style = st.selectbox("스타일", ["유화", "수채화", "시네마틱", "일러스트", "실사"])
        
        if st.button("이미지 생성 실행"):
            if img_prompt:
                with st.spinner("이미지를 생성 중입니다..."):
                    # 텍스트와 스타일 조합
                    combined_prompt = f"{img_prompt}, {img_style} style"
                    encoded_prompt = combined_prompt.replace(" ", "%20")
                    st.session_state['img_url'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
                    time.sleep(2)
            else:
                st.warning("설명을 입력해 주세요.")

    with col_img_out:
        if 'img_url' in st.session_state:
            st.image(st.session_state['img_url'], use_container_width=True)
            st.success("이미지 생성이 완료되었습니다.")
        else:
            st.markdown("<div style='text-align: center; color: #94A3B8; padding-top: 10rem;'>생성된 이미지가 여기에 표시됩니다.</div>", unsafe_allow_html=True)

# 하단 푸터
st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.8rem; margin-bottom: 2rem;'>CTS Media Ministry Center | 콘텐츠지원국 © 2026</div>", unsafe_allow_html=True)
