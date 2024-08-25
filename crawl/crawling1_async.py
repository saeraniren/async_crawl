import aiohttp
import asyncio
from bs4 import BeautifulSoup

# 비동기 크롤링을 위한 세션을 생성하고 데이터를 수집하는 함수
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

# 비동기적으로 페이지의 HTML을 가져와서 파싱하는 함수
async def get_last_page(session):
    url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage=91'
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    # 마지막 페이지 번호 찾기
    paging_div = soup.find('div', class_='page_wrap')
    page_numbers = paging_div.find_all('a')
    last_page = max([int(a.text) for a in page_numbers if a.text.isdigit()])

    return last_page

# 페이지의 데이터를 수집하는 함수
async def crawl_data(session, page_num):
    url = f'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?rows=15&cpage={page_num}'
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # 테이블 데이터 크롤링
    table = soup.find('table')
    rows = table.find_all('tr')
    
    data = []
    for row in rows:
        cells = row.find_all('td')
        data.append([cell.get_text(strip=True) for cell in cells])

    return data

# 메인 비동기 함수
async def crawl_1_async():
    async with aiohttp.ClientSession() as session:
        last_page = await get_last_page(session)
        
        tasks = [crawl_data(session, page_num) for page_num in range(1, last_page + 1)]
        results = await asyncio.gather(*tasks)

        # 결과 데이터 통합
        data = [item for sublist in results for item in sublist]
        print(data)

        return data

# 비동기 실행
if __name__ == "__main__":
    asyncio.run(crawl_1_async())