import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Slang
from app.utils import get_korean_initial
import requests
from bs4 import BeautifulSoup


WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/대한민국의_인터넷_신조어_목록"

def fetch_wikipedia_slang():
    """위키피디아에서 대한민국 인터넷 신조어 목록과 뜻을 크롤링"""
    response = requests.get(WIKIPEDIA_URL)
    if response.status_code != 200:
        print("⚠️ 위키피디아 페이지를 불러오지 못했습니다.")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    
    slang_dict = {}

    # ✅ 위키피디아 문서에서 <ul> 태그 찾기
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            text = li.text.strip()
            if "–" in text or "-" in text:  # 신조어 – 뜻 형태 찾기
                parts = text.split("–") if "–" in text else text.split("-")
                slang = parts[0].strip()
                meaning = parts[1].strip() if len(parts) > 1 else "뜻 없음"

                if slang:
                    slang_dict[slang] = meaning

    return slang_dict

def save_slang_to_db(slang_dict):
    """크롤링한 신조어, 뜻, 초성을 데이터베이스에 저장 (중복 제거)"""
    db: Session = SessionLocal()
    existing_words = {s.word for s in db.query(Slang).all()}  # 기존 DB 신조어 가져오기

    new_slang_count = 0
    for slang, meaning in slang_dict.items():
        if slang not in existing_words:  # 중복 체크
            initial = get_korean_initial(slang)  # ✅ 초성 추출
            new_slang = Slang(word=slang, translation=meaning, initial=initial)
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
