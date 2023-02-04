# -*- coding: UTF-8 -*-
# mypy: ignore-errors

from datetime import datetime
from aiohttp import ClientSession

from typing import TypedDict, Union, Iterable, Literal

class Group(TypedDict):
    '- 네이버 트렌드 API 검색 키워드 그룹 인스턴스'
    name: str
    keywords: Iterable[str]

class Client(TypedDict):
    '- 네이버 API 애플리케이션 인스턴스'
    identifier: str
    secret: str

async def search(
    client: Client,
    start: datetime, 
    end: datetime, 
    time_unit: str, 
    keyword_groups: Iterable[Group],
    device: Union[Literal['pc', 'mo'], None] = None,
    gender: Union[Literal['f', 'm'], None] = None,
    ages: Union[Iterable[str], None] = None,
):
    '- 검색 함수'

    if time_unit: assert time_unit in ('month', 'week', 'date'), f'올바르지 않은 시간 유닛 {time_unit!r}이(가) 입력되었습니다.'
    if device: assert device in ('pc', 'mo'), f'올바르지 않은 디바이스 {device!r}이(가) 입력되었습니다.'
    if gender: assert gender in ('f', 'm'), f'올바르지 않은 성별 {gender!r}이(가) 입력되었습니다.'
    keyword_groups = [{'groupName': keyword_group['name'], 'keywords': keyword_group['keyword']} for keyword_group in keyword_groups]
    
    if start.year < 2016 or end.year < 2016 or start.year > datetime.now().year or end.year > datetime.now().year:
        raise ValueError('올바르지 않은 datetime 오브젝트가 입력되었습니다.')

    start = f'{start.year}-{start.month}-{start.day}'
    end = f'{end.year}-{end.month}-{end.day}'

    async with ClientSession(headers={
        'Content-Type': 'x-www-form-urlencoded',
        'X-Naver-Client-Id': client['identifier'],
        'X-Naver-Client-Secret': client['secret'],
    }) as session:
        response = await session.post('https://openapi.naver.com/v1/datalab/search', params={
            'startDate': start,
            'endDate': end,
            'timeUnit': time_unit,
            'keywordGroups': keyword_groups,
            'device': device,
            'ages': ages,
            'gender': gender,
        })
        response.raise_for_status()
        data = await response.json(encoding='UTF-8')
    await session.close()
    return data
