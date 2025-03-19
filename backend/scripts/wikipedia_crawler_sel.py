import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import sessionmaker
import time
import re
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Slang
from app.utils import get_korean_initial  # 초성 추출 함수

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# ✅ Chrome WebDriver 설정
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # GUI 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# ✅ 위키백과 신조어 페이지 URL
WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/대한민국의_인터넷_신조어_목록"
driver.get(WIKIPEDIA_URL)
time.sleep(2)  # 페이지 로딩을 기다림

# ✅ 모든 h3 태그 가져오기
h3_elements = driver.find_elements(By.CSS_SELECTOR, "h3")

slang_dict = {}
slang_count = 0  # DB에 저장된 신조어 개수

for h3 in h3_elements:
    section_title = h3.text.strip()
    initial = get_korean_initial(section_title)  # 초성 추출

    try:
        # ✅ `h3`가 속한 `div`의 다음 형제 `ul` 찾기
        ul_element = h3.find_element(By.XPATH, "./ancestor::div/following-sibling::ul[1]")
        slang_list = ul_element.find_elements(By.TAG_NAME, "li")

        for slang in slang_list:
            try:
                term_element = slang.find_element(By.TAG_NAME, "b")  # 신조어 (굵은 글씨)
                term = term_element.text.strip()
                meaning = slang.text.split(":", 1)[1].strip() if ":" in slang.text else "뜻 없음"

                # ✅ 출처 번호 제거
                meaning = re.sub(r"\[\d+\]", "", meaning).strip()

                # ✅ 데이터베이스 중복 체크 후 저장
                existing_slang = session.query(Slang).filter_by(word=term).first()
                if not existing_slang:
                    new_slang = Slang(word=term, translation=meaning, initial=initial)
                    session.add(new_slang)
                    session.commit()
                    slang_count += 1
                    slang_dict[term] = meaning
                else:
                    print(f"⚠️ 이미 존재하는 단어: {term}")

            except:
                print(f"⚠️ {section_title} 섹션에서 일부 항목을 찾을 수 없음.")

    except Exception as e:
        print(f"⚠️ {section_title} 섹션에 `ul`이 없습니다: {e}")

# ✅ 크롤링 결과 확인
print(f"🔍 크롤링 완료! 저장된 신조어 개수: {slang_count}")
print("🔍 샘플 데이터:", list(slang_dict.items())[:10])

# ✅ 크롤링 종료
driver.quit()
session.close()
