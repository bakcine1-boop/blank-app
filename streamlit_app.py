import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="CTS AI 목회비서", page_icon="✝️", layout="wide")

st.title("✝️ CTS AI 목회 창작소")
st.markdown("---")

# 2. 사이드바 (설정)
with st.sidebar:
    st.header("⚙️ 설정 및 모드 선택")
    
    # API 키 입력창
    api_key = st.text_input("구글 API Key를 입력하세요", type="password")
    
    # 기능 선택 라디오 버튼
    mode = st.radio("어떤 작업을 하시겠습니까?", ["📝 설교/칼럼 작성 (Gemini)", "🎨 설교 이미지 생성 (AI 화가)"])
    
    st.info("💡 '이미지 생성'은 API 키 없이도 체험 가능합니다.")
    st.markdown("---")
    st.caption("CTS Media Ministry Center © 2026")

# 3. 메인 기능: 설교/칼럼 작성 (Gemini)
if mode == "📝 설교/칼럼 작성 (Gemini)":
    st.subheader("📝 설교 및 목회 칼럼 도우미")
    st.caption("제미나이(Gemini Pro)가 목사님의 묵상을 글로 정리해 드립니다.")
    
    if not api_key:
        st.warning("👈 왼쪽 사이드바에 구글 API Key를 먼저 입력해주세요!")
    else:
        genai.configure(api_key=api_key)
        
        # 입력창
        topic = st.text_area("주제, 성경 본문, 예화 등을 입력해주세요.", height=150, 
                            placeholder="예: 마태복음 5장 13-16절을 본문으로 '세상의 소금과 빛'에 대한 3대지 설교 개요를 짜줘. 청년들이 이해하기 쉽게 작성해줘.")
        
        if st.button("설교문 작성 시작", type="primary"):
            with st.spinner("제미나이가 말씀을 묵상하고 있습니다..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(topic)
                    
                    st.success("작성이 완료되었습니다!")
                    st.markdown("### 📖 결과물")
                    st.write(response.text)
                    
                    # 복사 편의를 위한 코드 블록 제공
                    with st.expander("텍스트 복사하기"):
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# 4. 메인 기능: 이미지 생성 (AI 화가)
elif mode == "🎨 설교 이미지 생성 (AI 화가)":
    st.subheader("🎨 설교 예화/포스터 이미지 생성")
    st.caption("설교 화면에 띄울 이미지를 AI가 즉석에서 그려드립니다.")
    
    # 이미지 프롬프트 입력
    img_desc = st.text_input("어떤 그림을 원하시나요? (구체적일수록 좋습니다)", 
                            placeholder="예: 거친 파도 위를 걸어가시는 예수님의 뒷모습, 유화 스타일, 웅장한 빛")
    
    # 스타일 선택
    style = st.selectbox("화풍 선택", ["선택 안 함", "수채화 (Watercolor)", "유화 (Oil Painting)", "초현실주의 (Cinematic)", "일러스트 (Illustration)", "사진 같은 (Photorealistic)"])
    
    if st.button("그림 그리기 🎨", type="primary"):
        if not img_desc:
            st.warning("그림에 대한 설명을 입력해주세요!")
        else:
            with st.spinner("AI 화가가 붓을 들었습니다... (약 5초 소요)"):
                # 프롬프트 조합 (스타일 추가)
                final_prompt = img_desc
                if style != "선택 안 함":
                    final_prompt += f", {style} style"
                
                # 무료 이미지 생성 API 활용 (Pollinations AI)
                # 공백을 URL 형식(%20)으로 변환
                encoded_prompt = final_prompt.replace(" ", "%20")
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true"
                
                # 이미지 표시 (약간의 지연 시간 후 로드)
                time.sleep(2)
                st.image(image_url, caption=f"'{img_desc}' 생성 결과", use_column_width=True)
                
                st.success("완성되었습니다! 이미지를 마우스 우클릭하여 저장하세요.")
