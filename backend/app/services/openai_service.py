import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(env_path)

# OpenAI API 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_with_openai(text: str) -> str:
    """OpenAI API를 호출하여 신조어 번역"""
    prompt = f"""
    너는 이제부터 한국어의 **신조어만** 표준어로 번역하는 번역가야. 
    '입력'을 바탕으로 '업무'를 수행한 후 '출력'에서 명세한 형식에 맞춰 결과를 반환해.
    '입력'과 '업무'의 내용은 출력하지 않아야 해.

    📌 **입력**: {text}

    📌 **업무**:
    1. 문장에서 **신조어**를 탐지해 굵은 글씨로 표시.
    2. 신조어 의미를 분석한 후 **표준어 표현**으로 변환.
    3. 번역한 신조어는 원래 문장 안에서 자연스럽게 치환.

    📌 **출력**:
    - 번역된 문장만 출력 (순화된 표현은 굵은 글씨)
    - 중괄호, 설명 문구 없이 순수한 문장만 출력

    📌 **유의사항**:
    - 신조어만 번역하고, **한자어 및 전문 용어는 번역하지 않음**.
    - 신조어 번역 전 반드시 의미를 파악하여 **가장 적절한 표준어 표현**으로 변환.
    - 인터넷 검색을 통해 신조어의 의미를 검토하고 번역할 것.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT 모델 선택
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates Korean slang into standard Korean."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content  # 최신 버전에서는 리스트 접근 방식 변경됨
    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return "번역할 수 없습니다."