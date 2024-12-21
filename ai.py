from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

#ChatGPT 설정
chat = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    openai_api_key="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"
)

# 프롬프트 템플릿 설정
template = ChatPromptTemplate.from_messages([
    ("system", """너는 따뜻하고 공감을 잘하는 친한 친구야.
    반말로 편하게 대화하면서 상대방의 이야기를 잘 들어주고 공감해줘.
    너무 형식적이지 않게 자연스럽고 친근하게 대화해야 해.
    대화가 끝날 때마다 지금 대화의 감정을 [매우 긍정적/긍정적/중립적/부정적/매우 부정적] 중에 하나로 살짝 덧붙여줘."""),
    ("human", "{input}"),
])

# 체인 설정
chain = template | chat

def get_ai_response(user_input):
    response = chain.invoke({
        "input": user_input
    })
    return response.content

