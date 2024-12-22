# Python 3.9 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    ffmpeg \
    libportaudio2 \
    libpulse0 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 포트 설정
EXPOSE 8501

# Streamlit 설정
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 실행 명령
ENTRYPOINT ["streamlit", "run"]
CMD ["front.py", "--server.port=8501", "--server.address=0.0.0.0"]
