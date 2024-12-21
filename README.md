# 팀_마음의 소리 프로젝트 소개

![bohlogo](https://github.com/user-attachments/assets/b8765edc-409f-4a77-a25a-cb0ce6883216) 
← 우리팀 마스코트

## 목차
- [팀 소개](#팀-소개)
- [프로젝트 개발 동기](#프로젝트-개발-동기)
- [프로젝트 개요](#프로젝트-개요)
- [개발 과정](#개발-과정)
- [실행 방법](#실행-방법)
- [문의](#문의)

---

## 팀 소개

| 이름          | 역할           | GitHub Profile                                   |
|---------------|----------------|-------------------------------------------------|
| 이서영       | 팀장 / 프로젝트 총괄  | [@dtd08](https://github.com/dtd08)   |
| 양준석       | 부팀장 / 프론트엔드     | [@gogi102](https://github.com/gogi102) |
| 김규민       | AI 엔지니어       | [@kornet79](https://github.com/kornet79)     |
| 장연준       | QA / 데이터 수집 및 정리 | [@Jangyeonjun](https://github.com/Jangyeonjun) |

---

## 프로젝트 개발 동기

최근 사회적 문제로 대두된 청소년의 정신건강 문제 완화를 위해 이 프로젝트를 기획하게 되었습니다. <br/>
특히 상담 분야를 정하기 위해 주변 고등학교 친구들을 대상으로 설문조사를 하여 가장 많이 나온 고민 분야,
진로 및 대인관계 분야를 위주로 또래의 눈높이에서 위로와 이정표를 제공하고자 하였습니다

### 주요 동기
1. **문제 상황: '상담'의 장벽** <br/>
: 전문적인 선생님을 만나 자신의 속마음을 털어놓는 것은 생각보다 큰 부담입니다. <br/>
실제로 주변 이야기를 들어보면 고민을 가진 친구들은 많지만 상담을 받았다는 친구는 생각보다 적습니다.
2. **목표: 상담의 장벽 및 스트레스 완화** <br/>
: '상담'이라는 사실에 과도한 집중이 되지 않게 친구같이 친근한 어휘로 접근하여 진입장벽을 낮추고 <br/>
누구에게도 쉽게 털어놓지 못했던 마음 속에 있던 말을 털어놓으면서 스트레스를 완화하길 원했습니다.
3. **주요 가치** <br/>
: 위와 같은 상황을 타파하고 목표를 달성하기 위해선 공감, 경청, 지원, 접근성의 가치가 필요하다고 생각하였습니다.

---

## 프로젝트 개요

### 시연 영상 (수정 필요)


### 프로젝트 이름: **BoH GPT (Beacon of Hearts)**

### 주요 기능: (수정 필요)
1. **OpenAI 모델(GPT-4) 기반**: 미리 학습된 한국어 문장 이해 모델을 기반으로 상담에 적합한 성격 설정.
2. **지식 베이스**: 상담 관련 데이터를 벡터 저장소로 활용하여 AI가 상담 관련 자료를 빠르게 참조하도록 함.
3. **대화 인터페이스**: Streamlit을 사용하여 웹 애플리케이션을 구현하여 친구와 실시간으로 대화하는 듯한 인터페이스를 제공함. 

### 핵심 장점
- **쉬운 조작법**: 간단히 문장을 입력하는 것만으로 이용 가능.
- **직관적인 UI/UX**: 직관적이고 이해하기 쉬운 UI/UX 제공.
- **낮은 진입장벽**: 시간적/공간적 제약 해결 및 친근한 어투로 상담에 대한 거부감 완화.

### 기술 스택:
- **프론트엔드**: Python streamlit
- **백엔드 / AI**: LangChain, FAISS, OpenAI API, CharacterTextSplitter, TextLoader
- **배포** : AWS

![시스템 구조](https://velog.velcdn.com/images/cataiden/post/ffa101d7-ff02-48c8-a5e2-156084e2dc66/image.png)

## 실행 방법

### 1. 환경 설정
1. **프로젝트 클론**
   ```bash
   git clone https://github.com/dtd08/Makerthon_VoH/tree/main
   cd Makerthon_VoH
   ```

2. **필요한 패키지 설치**

    | 패키지          | 명령어                |                     |                |
    |-----------------|----------------------|---------------------|-----------------|
    | LangChain       | ```python -m pip install langchain ``` | ```python -m pip install langchain-openai ``` | ```python -m pip install langchain-community ``` |
    | OpenAI          | ```python -m pip install openai ``` | 
    | 벡터 저장소 관련 | ```python -m pip install faiss-cpu ``` |
    | 환경 변수 관리   | ```python -m pip install python-dotenv ``` |
    | 의존성 패키지    | ```python -m pip install numpy ``` | ```python -m pip install typing ``` |

4. **환경 변수 설정**
   프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 추가:
   ```env
   DB_URL=your_database_url
   API_KEY=your_api_key
   ```

### 2. 실행
1. **개발 서버 실행**
   ```bash
   streamlit run Front.py
   ```

2. **프로덕션 빌드** (선택 사항)
   ```bash
   npm run build
   npm start
   ```

### 3. 접속
   - 로컬에서: `http://localhost:8504/`
   - 배포된 서버: `https://your-deployed-site.com` (수정 필요)

---

## 문의

- **데이터 출처**: [AI Hub](https://aihub.or.kr/aihubdata/data/view.do?currMenu=120&topMenu=100&aihubDataSe=extrldata&dataSetSn=267)
- **이메일**: ddwt0826@gmail.com
- **GitHub Issues**: [링크](https://github.com/dtd08/Makerthon_VoH/issues)
---
