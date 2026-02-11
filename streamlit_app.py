import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(
    page_title="CTS 미디어목회지원센터 | AI 목회비서", 
    page_icon="✝️", 
    layout="wide"
)

# 2. Genspark 스타일의 커스텀 CSS (디자인 핵심)
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA;
    }
    
    /* 상단 헤더 섹션 */
    .main-header {
        background-color: #1E3A8A;
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 서비스 카드 스타일 */
    .service-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* 입력창 및 여백 조정 */
    .stTextArea textarea { border-radius: 10px; }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        background-color: #1E3A8A !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API 키 보안 처리 (Secrets 활용)
# Streamlit 클라우드 설정의 Secrets 항목에 GOOGLE_API_KEY가 저장되어 있어야 합니다.
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ 시스템 설정에서 API 키를 찾을 수 없습니다.")
    st.stop()

# 4. 상단 브랜딩 영역 (Genspark 디자인 참고)
st.markdown("""
    <div class="main-header">
        <h1 style='color: white; margin: 0;'>CTS 미디어목회지원센터</h1>
        <p style='font-size: 1.1rem; opacity: 0.9;'>콘텐츠지원국 AI 목회 비서 시스템</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 레이아웃 (좌측 메뉴 / 우측 작업 영역)
tab1, tab2 = st.tabs(["📝 AI 설교·칼럼 작성", "🎨 AI 성화 이미지 생성"])

# --- 탭 1: 설교 및 칼럼 작성 ---
with tab1:
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("""
            <div class="service-card">
                <h3>📖 설교문 작성 도우미</h3>
                <p>본문과 주제를 입력하시면 제미나이가 초안을 작성합니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        topic = st.text_area(
            "작성 요청 사항", 
            height=250, 
            placeholder="예시: 마태복음 5장 13-16절을 본문으로 '세상의 소금과 빛' 설교 개요를 3대지로 짜줘. 현대적인 예화를 포함해줘."
        )
        
        if st.button("AI 초안 생성 시작 🚀", key="btn_sermon"):
            if topic:
                with st.spinner("메시지를 분석하여 묵상 중입니다..."):
                    try:
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(topic)
                        st.session_state['sermon_result'] = response.text
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
            else:
                st.warning("작성할 내용을 입력해주세요.")

    with col2:
        if 'sermon_result' in st.session_state:
            st.markdown("### 📄 생성된 결과물")
            st.info("내용을 확인하신 후 아래 코드 상자에서 복사하여 사용하세요.")
            st.write(st.session_state['sermon_result'])
            st.divider()
            with st.expander("간편하게 텍스트 복사하기"):
                st.code(st.session_state['sermon_result'], language="markdown")
        else:
            st.markdown("""
                <div style='text-align: center; color: #666; padding-top: 5rem;'>
                    왼쪽에서 내용을 입력하고 버튼을 누르면 이곳에 결과가 표시됩니다.
                </div>
            """, unsafe_allow_html=True)

# --- 탭 2: 이미지 생성 ---
with tab2:
    col_img1, col_img2 = st.columns([1, 1.2], gap="large")
    
    with col_img1:
        st.markdown("""
            <div class="service-card">
                <h3>🎨 AI 성화 생성기</h3>
                <p>설교 예화나 포스터에 사용할 이미지를 생성합니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        img_desc = st.text_input("그림 설명 (예: 기도하는 소년, 웅장한 빛)", placeholder="영어로 입력 시 품질이 더 좋아집니다.")
        style = st.selectbox("추천 화풍", ["유화 (Oil Painting)", "수채화 (Watercolor)", "시네마틱 (Cinematic)", "일러스트 (Illustration)"])
        
        if st.button("그림 그리기 시작 🎨", key="btn_img"):
            if img_desc:
                with st.spinner("AI 화가가 생성 중입니다..."):
                    final_prompt = f"{img_desc}, {style} style"
                    encoded_prompt = final_prompt.replace(" ", "%20")
                    st.session_state['gen_image_url'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
                    time.sleep(2)
            else:
                st.warning("설명을 입력해주세요.")

    with col_img2:
        if 'gen_image_url' in st.session_state:
            st.image(st.session_state['gen_image_url'], use_container_width=True, caption="생성된 이미지")
            st.success("이미지가 완성되었습니다! 마우스 우클릭으로 저장 가능합니다.")
        else:
            st.markdown("""
                <div style='text-align: center; color: #666; padding-top: 5rem;'>
                    생성된 그림이 이곳에 표시됩니다.
                </div>
            """, unsafe_allow_html=True)

# 하단 푸터
st.markdown("---")
st.caption("CTS Media Ministry Center | 콘텐츠지원국 국장 전용 시스템 © 2026")
