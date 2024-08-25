from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urlparse, parse_qs

import csv

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage='
data = []

def crawl(url):
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
        )

        tr_crawl = driver.find_elements(By.TAG_NAME, 'tr')
        
        for tr in tr_crawl:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            row = [td.text for td in tds]
            data.append(row)

    finally:
        pass

    return data

def search_last_pg():
    driver.get('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage=1')

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )

        elements = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div[2]/a[13]')
        link = elements.get_attribute('href')

    finally:
        pass

    return link

def parsing_pg_num(link):
    url = link

    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)

    page_number = int(query_params.get('cpage', [1])[0])

    return page_number

page_number = parsing_pg_num(search_last_pg())

for pg_num in range(1, page_number + 1):
    crawl_url = url + str(pg_num)

    crawl(crawl_url)

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)