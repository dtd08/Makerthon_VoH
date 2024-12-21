import streamlit as st # type: ignore
from datetime import datetime
from PIL import Image
import ai

if 'welcomed' not in st.session_state:
    st.session_state.welcomed = False

# 이미지 가져오기
img = Image.open("assets\-removebg-preview_1.png")
main_img = Image.open("assets\img.png")

# 페이지 설정
st.set_page_config(page_title="인공지능 메이커톤", page_icon="💬", layout="centered")

# 이미지와 제목을 나란히 표시하기 위한 컬럼 생성
col1, col2 = st.columns([4, 1])  # 4:1 비율로 공간 분할 (순서 변경)

with col1:
    st.title("AI 상담 챗봇")  # 왼쪽 컬럼에 제목 표시
    st.write("고민을 이야기하고 AI와 대화를 시작해보세요.")

with col2:
    st.markdown("""
        <style>
            div[data-testid="column"]:nth-of-type(2) > div:nth-child(2) > div:first-child > div:first-child > img {
                margin-top: -30px !important;  # 이 값을 조절하여 상하 위치 변경
            }
        </style>
        """, unsafe_allow_html=True)
    st.image(main_img)  # 메인 이미지

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
            justify-content: flex-end;  /* 사용자 메시지용 기본 정렬 */
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

# 사용자가 입력한 텍스트 받기
user_input = st.chat_input("고민을 말해주세요")

# 세션 상태에서 대화 메시지를 저장할 리스트 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

if not st.session_state.welcomed:
    welcome_message = {
        "role": "assistant",
        "content": "안녕? 오늘은 어떤 하루를 보냈어? 네가 속상했던 일이나 즐거웠던 일, 행복하거나 화가났던 일들을 내가 모두 들어줄게!",
        "time": datetime.now().strftime("%H:%M")
    }
    st.session_state.messages.append(welcome_message)
    st.session_state.welcomed = True

if user_input:
    # 사용자의 메시지를 messages 리스트에 추가 (시간 정보 포함)
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })

    # AI의 응답 생성 - ai.py의 함수 호출
    chatbot_response = ai.get_ai_response(user_input)

    # 챗봇의 응답을 messages 리스트에 추가 (시간 정보 포함)
    st.session_state.messages.append({
        "role": "chatbot", 
        "content": chatbot_response,
        "time": datetime.now().strftime("%H:%M")
    })

# 대화 내용 표시
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

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
            st.markdown('''
                <style>
                    [data-testid="column"] {
                        padding-top: 1rem;  # 상단 여백 조절
                    }
                </style>
            ''', unsafe_allow_html=True)
            st.image("assets/-removebg-preview_1.png", width=50)
        with col2:
            st.markdown(f'''
                <div class="message-container ai">
                    <div class="message ai-message">
                       {message["content"]}
                        <div class="message-time">{message.get("time", "")}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
