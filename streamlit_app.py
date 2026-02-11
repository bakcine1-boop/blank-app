import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 (반응형 및 와이드 모드)
st.set_page_config(page_title="AI 목회비서", page_icon="🙏", layout="wide")

# 2. 젠스파크(Genspark) 최적화 고품격 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8FAFC !important;
    }

    /* 메인 카드 디자인: 깊은 곡선과 그림자 */
    .service-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }

    /* 버튼 스타일: 젠스파크 정체성 반영 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #1E3A8A !important;
        color: white !important;
        height: 3.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2); }

    /* 결과창 텍스트 박스 */
    .result-box {
        background-color: #F1F5F9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1E3A8A;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* 탭 및 모바일 최적화 */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 30px; }
    .stTabs [aria-selected="true"] { color: #1E3A8A !important; border-bottom-color: #1E3A8A !important; font-weight: 700; }
    
    @media (max-width: 640px) {
        .block-container { padding: 1rem; }
        .stTabs [data-baseweb="tab"] { font-size: 1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API 보안 설정 (비용 효율적인 Gemini 1.5 Flash 사용)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("설정(Secrets)에서 GOOGLE_API_KEY를 등록해 주세요.")
    st.stop()

# 4. 상태 관리 (자동 프롬프트 기능)
if 'input_val' not in st.session_state: st.session_state['input_val'] = ""

# 5. 메인 레이아웃 (중복 헤더 제거)
tab1, tab2 = st.tabs(["📝 설교 및 칼럼 작성", "🎨 이미지 생성"])

# --- 탭 1: 설교/칼럼 및 저장 기능 ---
with tab1:
    st.markdown('<div class="service-card"><strong>원하시는 사역 주제를 선택하거나 입력해 주세요.</strong></div>', unsafe_allow_html=True)
    
    # [자동 프롬프트 기능] 버튼 클릭 시 입력창 자동 완성
    col_p1, col_p2, col_p3 = st.columns(3)
    if col_p1.button("📖 설교 초안"): st.session_state['input_val'] = "마태복음 5:13-16 본문을 바탕으로 '세상의 소금과 빛' 설교 초안을 작성해줘."
    if col_p2.button("✍️ 목회 칼럼"): st.session_state['input_val'] = "'감사'를 주제로 성도들에게 위로를 주는 목회 칼럼을 작성해줘."
    if col_p3.button("🙏 중보 기도문"): st.session_state['input_val'] = "환우들과 교회를 위한 대표 기도문을 작성해줘."

    user_text = st.text_area("input", value=st.session_state['input_val'], height=250, label_visibility="collapsed")
    
    if st.button("AI 비서에게 작성 요청하기"):
        if user_text:
            with st.spinner("내용을 구성 중입니다..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_text)
                st.session_state['txt_res'] = response.text
        else:
            st.warning("내용을 먼저 입력해 주세요.")

    # [저장 및 복사 기능] 결과가 나왔을 때만 표시
    if 'txt_res' in st.session_state:
        st.markdown(f'<div class="result-box">{st.session_state["txt_res"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # 텍스트 파일로 즉시 저장하는 버튼
            st.download_button(
                label="💾 파일로 저장하기 (.txt)",
                data=st.session_state['txt_res'],
                file_name="목회자료.txt",
                mime="text/plain"
            )
        with c2:
            with st.expander("결과 전체 복사"):
                st.code(st.session_state['txt_res'])

# --- 탭 2: 이미지 생성 및 결과 확인 ---
with tab2:
    st.markdown('<div class="service-card"><strong>설교 배경이나 예화 이미지를 설명해 주세요.</strong></div>', unsafe_allow_html=True)
    img_desc = st.text_input("이미지 설명", placeholder="예: 평화로운 호숫가에서 기도하는 모습")
    
    if st.button("이미지 생성 시작하기"):
        if img_desc:
            with st.spinner("이미지를 생성 중입니다..."):
                # 나노바나나 엔진 (Pollinations AI 기반)
                encoded = img_desc.replace(" ", "%20")
                st.session_state['img_url'] = f"https://image.pollinations.ai/prompt/{encoded}?nologo=true"
                time.sleep(1)
        else:
            st.warning("설명을 입력해 주세요.")

    if 'img_url' in st.session_state:
        st.markdown("---")
        # 이미지 결과 표시 및 저장 안내
        st.image(st.session_state['img_url'], use_container_width=True, caption="생성된 이미지 (우클릭하여 저장 가능)")
        st.success("이미지가 완성되었습니다. 마우스 우클릭이나 길게 눌러 저장하세요.")

# 하단 푸터
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.8rem; margin: 3rem 0;'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)

# 6. 하단 푸터
st.markdown("<br><br><div style='text-align: center; color: #9CA3AF; font-size: 0.8rem;'>CTS Media Ministry Center © 2026</div>", unsafe_allow_html=True)
