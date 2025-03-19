from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# ✅ Chrome 드라이버 옵션 설정
options = Options()
options.add_argument("--headless")  # GUI 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ Selenium 드라이버 실행
service = Service("/usr/bin/chromedriver")  # Chromedriver 경로
driver = webdriver.Chrome(service=service, options=options)

# ✅ 위키백과 페이지 로드
WIKIPEDIA_URL = "https://ko.wikipedia.org/wiki/대한민국의_인터넷_신조어_목록"
driver.get(WIKIPEDIA_URL)
time.sleep(3)  # ✅ 페이지가 완전히 로딩될 때까지 대기

# ✅ BeautifulSoup으로 페이지 HTML 파싱
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# ✅ HTML 출력하여 확인
print(soup.prettify())
