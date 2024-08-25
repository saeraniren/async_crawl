import asyncio
import json
import aiomysql
import time  # time 모듈 추가

from crawl import crawl_1_async, crawl_2_async

async def save_to_db(crawl_1_data, crawl_2_data):
    try:
        conn = await aiomysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='test1',
        )
        async with conn.cursor() as cursor:
            query = """
            INSERT INTO your_table_name (crawl_1_data, crawl_2_data)
            VALUES (%s, %s)
            """
            await cursor.execute(query, (json.dumps(crawl_1_data), json.dumps(crawl_2_data)))
            await conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            await conn.ensure_closed()

async def main():
    start_time = time.time()

    try:
        # 비동기 크롤링 작업 실행
        crawl_1_data, crawl_2_data = await asyncio.gather(
            crawl_1_async(),
            crawl_2_async()
        )

        # JSON 형식으로 출력 (선택 사항)
        print("crawl_1_data:", json.dumps(crawl_1_data, indent=4, ensure_ascii=False))
        print("crawl_2_data:", json.dumps(crawl_2_data, indent=4, ensure_ascii=False))

        # 데이터베이스에 JSON 데이터 저장
        await save_to_db(crawl_1_data, crawl_2_data)
    except Exception as e:
        print(f"Error in main execution: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"처리 완료 시간: {elapsed_time:.4f} 초")

    return crawl_1_data, crawl_2_data

if __name__ == '__main__':
    asyncio.run(main())