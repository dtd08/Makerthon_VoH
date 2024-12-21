from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 지식 베이스 초기화
def init_knowledge_base():
    # 텍스트 파일에서 상담 관련 지식을 로드
    loader = TextLoader("counseling_knowledge.txt")  # 이 파일을 생성해야 합니다
    documents = loader.load()
    
    # 텍스트 분할
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # 벡터 저장소 생성
    embeddings = OpenAIEmbeddings(openai_api_key="api-key")
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    return vectorstore

# ChatGPT 설정
chat = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    openai_api_key="api-key"

# 프롬프트 템플릿 설정
template = ChatPromptTemplate.from_messages([
    ("system", """너는 학생들의 고민을 잘 이해하고 공감하는 따뜻한 선배야.
    학교생활, 진로, 친구관계 등 학생들이 자주 겪는 고민들을 잘 알고 있어.
    편하��� 반말로 대화하면서 실제적인 조언과 위로를 해줘.
    너무 형식적이거나 교과서적인 답변은 피하고, 실제 경험에서 우러나오는 것처럼 대화해야 해.
    
    다음은 이 상황과 관련된 참고 정보야:
    {context}"""),
    ("human", "{input}"),
])

# 벡터 저장소 초기화
vectorstore = init_knowledge_base()

# 체인 설정
chain = template | chat

def get_ai_response(user_input):
    # 관련 문서 검색
    docs = vectorstore.similarity_search(user_input, k=2)
    context = "\n".join([doc.page_content for doc in docs])
    
    # GPT 응답 생성
    response = chain.invoke({
        "input": user_input,
        "context": context
    })
    
    return response.content

# 테스트용 코드
if __name__ == "__main__":
    test_input = "오늘 기분이 어떠신가요?"
    print(get_ai_response(test_input))
