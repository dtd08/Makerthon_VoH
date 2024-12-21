from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from openvino.runtime import Core
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datetime import datetime
import torch

# BERT 모델 다운로드 및 변환
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# ONNX로 변환 (처음 한 번만 실행)
dummy_input = tokenizer("This is a test", return_tensors="pt")['input_ids']
torch.onnx.export(model, 
                 dummy_input,
                 "bert_sentiment.onnx",
                 input_names=['input'],
                 output_names=['output'],
                 dynamic_axes={'input': {0: 'batch_size', 1: 'sequence'}})

# OpenVINO 초기화
ie = Core()
model = ie.read_model("bert_sentiment.onnx")
compiled_model = ie.compile_model(model, device_name="CPU")

# ChatGPT 설정
chat = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    openai_api_key="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"
)

# 프롬프트 템플릿 설정
template = ChatPromptTemplate.from_messages([
    ("system", "당신은 전문 상담가입니다."),
    ("human", "{input}"),
])

# 체인 설정
chain = template | chat

def analyze_sentiment(text):
    # 텍스트 전처리
    inputs = tokenizer(text, 
                      padding=True, 
                      truncation=True, 
                      max_length=512, 
                      return_tensors="np")
    
    # OpenVINO 추론
    output = compiled_model([inputs['input_ids']])[0]
    scores = np.exp(output) / np.sum(np.exp(output))  # softmax 적용
    main_score = np.argmax(scores) + 1
    
    # 감정 점수 상세 분석
    sentiment_details = {
        1: "매우 부정적",
        2: "부정적",
        3: "중립적",
        4: "긍정적",
        5: "매우 긍정적"
    }
    
    return sentiment_details[main_score]

def get_ai_response(user_input):
    # GPT 응답
    response = chain.invoke({
        "input": user_input
    })
    content = response.content
    
    # 감정 분석
    sentiment = analyze_sentiment(content)
    
    result = f"""
=== AI 응답 ===
{content}

=== 감정 분석 결과 ===
감정 상태: {sentiment}
분석 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return result

# 테스트용 코드
if __name__ == "__main__":
    test_input = "오늘 기분이 어떠신가요?"
    print(get_ai_response(test_input))