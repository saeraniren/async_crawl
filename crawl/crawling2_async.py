import aiohttp
import asyncio
from bs4 import BeautifulSoup

# 비동기적으로 페이지의 HTML을 가져오는 함수
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

# 페이지에서 마지막 페이지 번호를 가져오는 함수
async def get_last_page(session):
    url = 'https://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=310&pageIndex=141&mode=&pageSize=10&recordCountPerPage=10&sort=&SearchFirstYn=N&searchPublicDate=&tgtTypeCd=SUB_CONT&searchKey='
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    # 마지막 페이지 번호 찾기
    paging_div = soup.find('div', class_='paging')
    page_numbers = paging_div.find_all('a')
    last_page = max([int(a.text) for a in page_numbers if a.text.isdigit()])

    return last_page

# 특정 페이지에서 데이터를 크롤링하는 함수
async def crawl_data(session, page_num):
    url = f'https://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=310&pageIndex={page_num}&sort=&SearchFirstYn=N&searchPublicDate=&tgtTypeCd=SUB_CONT&searchKey='
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # 테이블 데이터 크롤링
    table = soup.find('table')
    if not table:
        return []

    rows = table.find_all('tr')
    data = []
    for row in rows:
        cells = row.find_all('td')
        data.append([cell.get_text(strip=True) for cell in cells])

    return data

# 메인 비동기 함수
async def crawl_2_async():
    async with aiohttp.ClientSession() as session:
        last_page = await get_last_page(session)
        
        # 모든 페이지에 대한 비동기 작업 생성
        tasks = [crawl_data(session, page_num) for page_num in range(1, last_page + 1)]
        results = await asyncio.gather(*tasks)

        # 결과 데이터 통합
        data = [item for sublist in results for item in sublist]
        print(data)

        return data

# 비동기 실행
if __name__ == "__main__":
    asyncio.run(crawl_2_async())
