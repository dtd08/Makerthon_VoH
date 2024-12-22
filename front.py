import streamlit as st # type: ignore
from datetime import datetime
from PIL import Image
import ai
import speech_recognition as sr
from gtts import gTTS
import os
from pygame import mixer
import tempfile
import time

if 'welcomed' not in st.session_state:
    st.session_state.welcomed = False

# 이미지 가져오기
img = Image.open("./assets/-removebg-preview_1.png")
main_img = Image.open("./assets/img.png")

# 페이지 설정
st.set_page_config(page_title="인공지능 메이커톤", page_icon="💬", layout="centered")

placeholder = st.empty()

# 이미지와 제목을 나란히 표시하기 위한 컬럼 생성
col1, col2 = st.columns([4, 1])  # 4:1 비율로 공간 분할 (순서 변경)

with col1:
    st.title("꽉두철의 상담실")  # 왼쪽 컬럼에 제목 표시
    st.write("고민을 이야기하고 꽉두철과 상담을 진행해보세요!")

with col2:
    st.markdown("""
        <style>
            div[data-testid="column"]:nth-of-type(2) > div:nth-child(2) > div:first-child > div:first-child > img {
                margin-top: -30px !important;  # 이 값을 조절하여 상하 위치 변경
            }
        </style>
        """, unsafe_allow_html=True)
    st.image(main_img)  # 메인 이미지

# 음성 입력 함수
def get_voice_input():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    
    try:
        with sr.Microphone() as source:
            with st.spinner('말씀해주세요...'):
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=10, phrase_time_limit=10)
                text = r.recognize_google(audio, language='ko-KR')
                return text
    except Exception as e:
        st.error(f"음성 인식 실패: {str(e)}")
        return None

# 입력 방식 선택 (사이드바에 배치)
st.sidebar.header("대화방식을 골라주세요")
input_method = st.sidebar.selectbox("",["텍스트 대화", "음성 대화"])
# 전체 페이지 배경 설정
st.markdown("""
    <style>
        img{
            width: 150%;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 600px;
            margin: auto;
        }
        .message-container {
            display: flex;
            width: 100%;
            justify-content: flex-end;  /* 사용자 메시지용 기��� 정렬 */
        }
        .message-container.ai {
            justify-content: flex-start;  /* AI 메시지는 왼쪽 정렬 */
        }
        .message {
            display: inline-block;
            padding: 10px 15px;
            border-radius: 15px;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.5;
            max-width: 50%;
        }
        .user-message {
            background-color: #DCF8C6;
        }
        .ai-message {
            background-color: #FFFFFF;
            border: 1px solid #E6E6E6;
        }
        .message-time {
            font-size: 11px;
            color: #999;
            margin-top: 4px;
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

method = False

# 사용자 입력 처리
user_input = None
if input_method == '텍스트 대화':
    user_input = st.chat_input("고민을 말해주세요")
else:
    
    with placeholder.container():
       talk = st.button('🎤 음성으로 말하기')
    if talk:
        user_input = get_voice_input()
        if user_input:
            st.info(f"인식된 텍스트: {user_input}")
    method = True

# 세션 상태에서 대화 메시지를 저장할 리스트 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # 초기 환영 메시지 추가
    welcome_message = {
        "role": "assistant",
        "content": "안녕 나는 꽉두철이라고 해! 오늘은 어떤 하루를 보냈어? 네가 속상했던 일이나 즐거웠던 일, 행복하거나 화가났던 일들을 내가 모두 들어줄게!",
        "time": datetime.now().strftime("%H:%M")
    }
    st.session_state.messages.append(welcome_message)

if user_input:
    # 사용자의 메시지를 messages 리스트에 추가
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })
    
    # AI의 응답 생성
    chatbot_response = ai.get_ai_response(user_input)
    
    # 챗봇의 응답을 messages 리스트에 추가
    st.session_state.messages.append({
        "role": "chatbot", 
        "content": chatbot_response,
        "time": datetime.now().strftime("%H:%M")
    })

    # 입력 필드 초기화
    st.empty()

# 대화 내용 표시
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 세션 상태에 읽은 메시지 저장을 위한 초기화
if 'read_messages' not in st.session_state:
    st.session_state.read_messages = set()

def text_to_speech(text, message_id):
    # 이미 읽은 메시지인지 확인
    if message_id in st.session_state.read_messages:
        return
        
    try:
        # pygame mixer 초기화
        mixer.init()
        
        # 임시 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_filename = os.path.join(temp_dir, 'tts_temp.mp3')
            
        # TTS 변환
        tts = gTTS(text=text, lang='ko', slow = False)
        tts.save(temp_filename)
        
        # 오디오 재생
        mixer.music.load(temp_filename)
        mixer.music.play()
        
        # 재생이 끝날 때까지 대기
        while mixer.music.get_busy():
            time.sleep(0.1)
            
        # mixer 종료
        mixer.quit()
        
        # 임시 파일 삭제
        try:
            os.remove(temp_filename)
        except:
            pass
            
        # 읽은 메시지 목록에 추가
        st.session_state.read_messages.add(message_id)
            
    except Exception as e:
        st.error(f"TTS 오류: {str(e)}")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'''
            <div class="message-container">
                <div class="message user-message">
                    {message["content"]}
                    <div class="message-time" style="text-align:left;">{message.get("time", "")}</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([0.8, 10])
        with col1:
            st.image("assets/-removebg-preview_1.png", width=50)
        with col2:
            if method:  # 음성 대화 모드
                st.markdown(f'''
                    <div class="message-container ai">
                        <div class="message ai-message">
                            {message["content"]}
                            <div class="message-time">{message.get("time", "")}</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # 메시지의 고유 ID 생성
                message_id = f"{message['content']}_{message.get('time', '')}"
                
                # TTS 실행 (새로운 메시지만)
                if message == st.session_state.messages[-1]:
                    text_to_speech(message["content"], message_id)
            else:  # 텍스트 대화 모드
                st.markdown(f'''
                    <div class="message-container ai">
                        <div class="message ai-message">
                            {message["content"]}
                            <div class="message-time">{message.get("time", "")}</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)   
