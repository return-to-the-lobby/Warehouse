# -*- coding: UTF-8 -*-

from os import environ
environ.update({'JAVA_HOME': 'jdk-19.0.2'})

import konlpy
import asyncio

pocily = asyncio.WindowsSelectorEventLoopPolicy()
asyncio.set_event_loop_policy(pocily)

from aiohttp import ClientSession

JVM = konlpy.init_jvm()
OKT = konlpy.tag.Okt(JVM)        
CLIENT = {
    "CLIENT_SECRET": "YOUR CLIENT SECRET HERE",
    "CLIENT_ID": "YOUR CLIENT ID HERE",
}

query = input('검색할 단어를 입력하세요: ')

async def search(query):
    async with ClientSession(headers={
        'X-Naver-Client-Id': CLIENT['CLIENT_ID'],
        'X-Naver-Client-Secret': CLIENT['CLIENT_SECRET'],
    }) as session:
        response = await session.get('https://openapi.naver.com/v1/search/news.json', params={'query': query})
        response.raise_for_status()
        response = await response.json()
    await session.close()
    return response

loop = asyncio.new_event_loop()

result = search(query)
result = loop.run_until_complete(result)

raw_titles = [item['title'] for item in result['items']]
raw_descriptions = [item['description'] for item in result['items']]
words = []

for title in raw_titles:
    result = OKT.pos(title, norm=True)
    result = filter(lambda word: word[1] not in ('Punctuation', 'Foreign', 'Alpha'), result)
    words.extend(result)

words = tuple([word[0] for word in words])
print(words)
