import streamlit as st
import google.generativeai as genai

# (페이지 설정 및 CSS 생략 - 기존 스타일 유지)

# 3. API 보안 설정 (기존과 동일)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. 프롬프트 템플릿 정의 (직관적인 문구로 구성)
templates = {
    "📖 설교 초안": "성경 본문 [본문 입력]을 바탕으로 '세상의 소금과 빛'이라는 주제의 3대지 설교 초안을 작성해줘. 현대적인 예화와 실천 방안을 포함해줘.",
    "✍️ 목회 칼럼": "신앙생활 속에서의 '감사'를 주제로 성도들의 마음을 울리는 따뜻한 목회 칼럼을 한 페이지 분량으로 작성해줘.",
    "🙏 기도문": "질병으로 고통받는 환우들과 그 가족들을 위로하고 소망을 주는 중보 기도문을 작성해줘."
}

# 5. 텍스트 입력창 관리 (버튼 클릭 시 내용을 채워주기 위해 사용)
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def set_template(template_text):
    st.session_state['user_input'] = template_text

# 6. 메인 화면 구성
tab1, tab2 = st.tabs(["📝 설교 및 칼럼 작성", "🎨 이미지 생성"])

with tab1:
    st.markdown('<div class="service-card"><strong>자주 사용하는 양식을 선택하시거나 직접 입력해 주세요.</strong></div>', unsafe_allow_html=True)
    
    # 템플릿 선택 버튼 (가로로 배치하여 깔끔하게)
    cols = st.columns(len(templates))
    for i, (name, text) in enumerate(templates.items()):
        if cols[i].button(name):
            set_template(text)

    # 입력창 (st.session_state와 연결)
    user_topic = st.text_area(
        "내용 입력",
        value=st.session_state['user_input'],
        height=250,
        label_visibility="collapsed",
        placeholder="주제나 본문을 입력하거나 위 버튼을 눌러보세요."
    )
    
    if st.button("AI 비서에게 요청하기"):
        if user_topic:
            with st.spinner("내용을 구성 중입니다..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_topic)
                st.session_state['generated_text'] = response.text
        else:
            st.warning("내용을 입력해 주세요.")
            
    # (결과 표시 및 다운로드 기능 - 기존과 동일)
