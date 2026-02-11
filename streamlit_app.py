import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (최대한 깔끔하게)
st.set_page_config(page_title="AI 목회지원", layout="wide")

# 2. 미니멀 CSS (젠스파크 내부에서 이질감이 없도록 배경색과 여백 제거)
st.markdown("""
    <style>
    /* 불필요한 상단 여백 제거 */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    /* 배경을 흰색으로 통일하여 프레임 느낌 제거 */
    .stApp { background-color: #FFFFFF; }
    /* 버튼 디자인: 신뢰감 있는 짙은 회색/네이비 */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        background-color: #374151 !important;
        color: white !important;
        border: none;
        height: 3rem;
    }
    /* 안내 문구 스타일 */
    .guide-text { font-size: 0.9rem; color: #6B7280; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. API 설정 (속도가 빠른 Flash 모델로 변경)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API 키 설정이 필요합니다.")
    st.stop()

# 4. 상단 타이틀 제거 (젠스파크 헤더와 중복되므로 한 줄 안내만 남김)
st.markdown("<p class='guide-text'>본문이나 주제를 입력하시면 AI가 설교 및 칼럼 초안을 구성해 드립니다.</p>", unsafe_allow_html=True)

# 5. 메인 기능 (탭 제거하고 바로 보여주기)
col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    user_input = st.text_area(
        "작성할 내용", 
        height=300, 
        placeholder="예: 마태복음 5:13-16 '세상의 소금과 빛' 설교 초안 작성",
        label_visibility="collapsed" # 라벨 숨김으로 더 직관적으로
    )
    
    if st.button("AI 초안 작성하기"):
        if user_input:
            with st.spinner("작성 중입니다..."):
                try:
                    # 속도 최적화를 위해 Flash 모델 사용
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_input)
                    st.session_state['quick_res'] = response.text
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

with col_out:
    if 'quick_res' in st.session_state:
        st.markdown("### 작성 결과")
        st.write(st.session_state['quick_res'])
        st.divider()
        st.caption("결과물을 복사하여 사용하세요.")
    else:
        st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; color: #D1D5DB; border: 1px dashed #D1D5DB; border-radius: 8px;'>결과가 여기에 표시됩니다.</div>", unsafe_allow_html=True)

# 푸터 생략 또는 아주 작게 처리
st.markdown("<div style='text-align: right; font-size: 0.7rem; color: #E5E7EB; margin-top: 5rem;'>CTS Media</div>", unsafe_allow_html=True)
