import os
import sys

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from bs4 import BeautifulSoup, Tag

URL = sys.intern('https://www.naver.com')
EXECUTABLE = sys.intern('chromedriver.exe')

chrome = Chrome(EXECUTABLE)
chrome.get(URL)

try:
    enter = chrome.find_element(By.CSS_SELECTOR, '#NM_THEME_CATE_LIST > li:nth-child(1) > a') # 엔터 버튼 찾기.
    enter.click()
except ElementNotInteractableException:
    chrome.quit()
    os.execl(sys.executable, sys.executable, *sys.argv) # 페이지가 제대로 로딩이 되지 않은 게 원인이기 때문에 os.execl로 프로세스 다시 살리기.

source = chrome.page_source
soup = BeautifulSoup(source, 'lxml')

categories = soup.find_all('em', attrs={'class': 'theme_category'})
categories = filter(lambda element: element.parent.attrs['class'][0] != 'info_box', categories)
categories = list(categories)
titles = [category.parent.find('strong') for category in categories]
sources = [category.parent.find('div').find('span').find('span') for category in categories]

titles = map(Tag.getText, titles)
categories = map(Tag.getText, categories)
sources = map(Tag.getText, sources)

result = [
    {
        'title': title,
        'category': category,
        'source': source
    } for title, category, source in zip(titles, categories, sources)
] # 사전 리스트로 정리
print(result) 

chrome.quit() # 계속 지 혼자 안 꺼져서 그냥 임의적으로 끄기.
exit(0)
