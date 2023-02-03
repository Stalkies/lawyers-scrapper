import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

async def get_page_count(url, session: aiohttp.ClientSession):
    async with session.get(url) as responce:
        r = await responce.text()
    soup = BeautifulSoup(r, 'lxml')
    return re.findall(r'\d+',soup.find('li', class_='last-page').find('a').get('href'))[-1]

async def get_info(url, page, session: aiohttp.ClientSession):
    async with session.get(url+f'&page={page}') as responce:
        r = await responce.text()
    soup = BeautifulSoup(r, 'lxml')
    names = soup.find_all('h5')
    print(page)


async def main():
    url = 'https://www.cba.org/For-The-Public/Find-A-Lawyer/Results?searchradius=25'
    async with aiohttp.ClientSession() as session:
        last_page = int(await get_page_count(url, session=session))
        print(last_page)
        tasks = []
        for page in range(1, last_page+1):
            task = asyncio.create_task(get_info(url, page, session))
            tasks.append(task)
        print(len(tasks))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())