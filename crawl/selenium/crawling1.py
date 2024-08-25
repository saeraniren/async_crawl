from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('-disable-gpu')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# selenium을 이용한 데이터 크롤링 (메인 기능)
def crawl_data():
    try:
        # table 태그가 불러올 때 까지 기다리기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
        )

        # td 태그 크롤링
        tr_crawl = driver.find_elements(By.TAG_NAME, 'tr')

        # td 태그를 data 리스트에 append
        for tr in tr_crawl:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            row = [td.text for td in tds]
            data.append(row)

    finally:
        pass

    return data

# bs4를 이용한 마지막 페이지 가져오기
def get_last_page():
    
    # 웹 페이지 가져오기
    url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage=91'
    response = requests.get(url)
    html = response.text

    # HTML 파싱하기
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 마지막 페이지 번호 찾기
    paging_div = soup.find('div', class_ = 'page_wrap')

    # 모든 페이지 번호가 들어있는 <a> 태그를 찾아 리스트로 지정
    page_numbers = paging_div.find_all('a')

    # 페이지 번호 중 가장 큰 값을 찾기
    last_page = max([int(a.text) for a in page_numbers if a.text.isdigit()])

    return last_page

url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage='
data = []

def crawl_1():
    last_page = get_last_page()

    try:
        for page_num in range(1, last_page):
            crawl_url = url + str(page_num)

            driver.get(crawl_url)
            crawl_data()

    finally:
        driver.quit
        print(data)

    return data