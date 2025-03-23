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
    너는 이제부터 한국어 **신조어 단어 1개**를 입력받아,  
    의미가 명확히 존재하는 경우에만 표준어 또는 일반인이 이해할 수 있는 쉬운 말로 번역하는 GPT-4o 번역가야.  
    아래 조건에 따라 신조어인지 판별하고 번역 결과만 출력해.

    📌 **입력**: {text}

    📌 **작업 절차**:
    1. 입력된 단어가 실제로 존재하는 신조어인지 판단한다.
    2. 학습된 데이터, 커뮤니티 사용 사례, 위키, 블로그, SNS 등에서의 사용 맥락을 내부적으로 유추한다.
    3. 아래 조건 중 **하나라도 해당하면 반드시 "잘 모르겠습니다."만 출력**한다:
        - 단어가 학습되지 않았거나 의미가 정의되어 있지 않은 경우
        - 의미가 명확하게 통용되지 않거나, 커뮤니티 등에서도 맥락이 불분명한 경우
        - 추론은 가능하지만 신뢰도가 낮은 경우

    📌 **출력 형식**:
    - 의미가 명확한 경우: **"~을 뜻함"** 혹은 **"~라는 의미"** 형태로 간결하게 출력
    - 의미가 불확실한 경우: **"잘 모르겠습니다."**만 출력
    - 설명, 분석, 예시 문장은 출력하지 말 것
    - 오직 한 줄만 출력

    📌 **주의 사항**:
    - 신조어가 아닌 단어는 무시하고, 반드시 위 조건을 만족하는 신조어만 번역할 것
    - 억지 해석이나 애매한 설명은 하지 않도록 주의할 것
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.o",  # GPT 모델 선택
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