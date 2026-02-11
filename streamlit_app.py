import streamlit as st
import google.generativeai as genai

# 1. 설정 (제목 및 디자인)
st.set_page_config(page_title="CTS AI 목회비서", page_icon="✝️")
st.title("✝️ CTS AI 목회 창작소")
st.write("제미나이(Gemini)가 목사님의 설교 준비와 이미지 제작을 돕습니다.")

# 2. 사이드바 (API 키 입력 - 보안을 위해)
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("구글 API Key를 입력하세요", type="password")
    
    # 기능 선택
    mode = st.radio("어떤 작업을 하시겠습니까?", ["📝 설교/칼럼 작성", "🎨 설교 이미지 생성"])

# 3. 메인 기능 구현
if api_key:
    genai.configure(api_key=api_key)
    
    if mode == "📝 설교/칼럼 작성":
        st.subheader("📝 설교 및 목회 칼럼 도우미")
        topic = st.text_area("주제나 성경 본문을 입력해주세요.", height=100, placeholder="예: 요한복음 3장 16절을 본문으로 '사랑'에 대한 3대지 설교를 작성해줘.")
        
        if st.button("설교문 작성하기"):
            with st.spinner("제미나이가 묵상 중입니다..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(topic)
                    st.markdown(response.text)
                    st.success("작성 완료! 복사해서 사용하세요.")
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    elif mode == "🎨 설교 이미지 생성":
        st.subheader("🎨 설교 예화/포스터 이미지 생성")
        img_desc = st.text_input("어떤 이미지를 원하시나요?", placeholder="예: 거친 파도 위를 걸어가시는 예수님의 뒷모습, 유화 스타일")
        
        st.info("💡 현재 이 기능은 '나노바나나(Imagen)' 모델 연동 준비 중입니다. (곧 업데이트 예정)")
        # 실제 이미지 생성 코드는 복잡해서, 텍스트가 성공하면 다음 단계로 추가해 드릴게요!

else:
    st.warning("왼쪽 사이드바에 'Google API Key'를 먼저 입력해주세요!")
