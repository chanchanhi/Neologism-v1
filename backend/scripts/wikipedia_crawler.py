import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Slang
from app.utils import get_korean_initial
import requests
from bs4 import BeautifulSoup
import re

WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/대한민국의_인터넷_신조어_목록"

# ✅ 크롤링 요청 차단 방지를 위한 헤더 추가
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_wikipedia_slang():
    """위키백과에서 대한민국 인터넷 신조어 목록과 뜻을 크롤링"""
    response = requests.get(WIKIPEDIA_URL, headers=HEADERS)
    if response.status_code != 200:
        print("⚠️ 위키백과 페이지를 불러오지 못했습니다. 상태 코드:", response.status_code)
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

    slang_dict = {}

    # ✅ 'h3' 태그를 기준으로 초성을 찾고, 바로 뒤의 'ul' 태그에서 신조어 목록을 가져옴
    for h3_tag in soup.find_all("h3"):
        span_tag = h3_tag.find("span")  # 초성 추출
        if not span_tag or not span_tag.text.strip():
            continue  # 초성이 없으면 무시

        initial = span_tag.text.strip()  # 초성 (ㄱ, ㄴ, ㄷ 등)
        print(f"📌 초성 찾음: {initial}")  # ✅ 디버깅용 출력

        # ✅ 해당 초성 아래 있는 <ul> 리스트 찾기
        ul_tag = h3_tag.find_next_sibling("ul")
        if ul_tag:
            for li in ul_tag.find_all("li"):
                bold_tag = li.find("b")  # 신조어 단어 (굵게 표시된 부분)
                if bold_tag and bold_tag.text.strip():
                    word = bold_tag.text.strip()

                    # ✅ 뜻에서 신조어 단어 부분을 제거하여 깔끔한 뜻만 추출
                    meaning_text = li.get_text(strip=True)  # 전체 텍스트 가져오기
                    meaning = meaning_text.replace(word, "").strip("(): ").split(":")[-1].strip()
                    meaning = re.sub(r"\[.*?\]", "", meaning).strip()  # [숫자] 제거

                    if word and meaning:
                        slang_dict[word] = {"translation": meaning, "initial": initial}
                        print(f"✅ 신조어 추가: {word} → {meaning}")  # ✅ 디버깅용 출력

    return slang_dict

def save_slang_to_db(slang_dict):
    """크롤링한 신조어, 뜻, 초성을 데이터베이스에 저장 (중복 제거)"""
    db: Session = SessionLocal()
    existing_words = {s.word for s in db.query(Slang).all()}  # 기존 DB 신조어 가져오기

    new_slang_count = 0
    for slang, data in slang_dict.items():
        if slang not in existing_words:  # 중복 체크
            initial = data["initial"]
            translation = data["translation"]
            new_slang = Slang(word=slang, translation=translation, initial=initial)
            db.add(new_slang)
            new_slang_count += 1

    db.commit()
    db.close()

    print(f"✅ 새로운 신조어 {new_slang_count}개가 추가되었습니다!")

if __name__ == "__main__":
    slang_dict = fetch_wikipedia_slang()  # 1️⃣ 위키피디아 크롤링
    print(f"🔍 크롤링된 신조어 개수: {len(slang_dict)}")  # ✅ 개수 확인
    print("🔍 샘플 데이터:", list(slang_dict.items())[:10])  # ✅ 상위 10개 출력
    
    if slang_dict:
        save_slang_to_db(slang_dict)  # 2️⃣ DB에 저장



