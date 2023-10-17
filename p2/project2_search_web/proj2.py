from flask import Flask, render_template, send_from_directory
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드로 설정
driver = webdriver.Chrome(options=chrome_options)
#------------------------------------------------------------------------------------
#네이버
URL = 'https://signal.bz/news'
driver.get(url=URL)
#웹사이트가 업데이트 되거나 변경되면 CSS선택자를 변경해야 불러올 수 있다.
naver_results = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > div > section > div > section > section:nth-child(2) > div:nth-child(2) > div > div > div > a > span.rank-text')

naver_list = []
for naver_result in naver_results:
    print('1',naver_result.text)
    naver_list.append(naver_result.text)#리스트 저장
    
#-------------------------------------------------------------------------------------
#줌
URL1='https://zum.com'
driver.get(url=URL1)

driver.find_element(By.CSS_SELECTOR,'#app > div > div.layer_wrap > div.layer_inner > button').click()
time.sleep(1.0)

driver.find_element(By.CSS_SELECTOR,'#app > div > header > div.search_bar > div > fieldset > div > input[type=text]').send_keys("아무거나 검색")
time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR,'#app > div > header > div.search_bar > div > fieldset > div > button.search').click()
time.sleep(1)

zum_results = driver.find_elements(By.CSS_SELECTOR,'#issue_wrap > ul > li > div > a:nth-child(1) > span.txt')

zum_list = []
for zum_result in zum_results:
    print('2',zum_result.text)
    zum_list.append(zum_result.text)#리스트 저장

#-----------------------------------------------------------------------------------------------------
#네이트
URL2='https://www.nate.com'
driver.get(url=URL2)
time.sleep(3.0)

driver.find_element(By.CSS_SELECTOR,'#olLiveIssueKeyword > li:nth-child(1) > a > span.txt_rank').click()
time.sleep(3.0)

nate_results = driver.find_elements(By.CSS_SELECTOR,'#search-option > form:nth-child(2) > fieldset > div.issue-kwd > span > a')

nate_list = []
for nate_result in nate_results:
    print('3',nate_result.text)
    nate_list.append(nate_result.text)#리스트 저장


#-------------------------------------------------------------------------------------------------------------------
#웹 페이지
app = Flask(__name__)#Flask 사용

@app.route('/')
def index():
    return render_template('index.html', naver_list=naver_list, nate_list=nate_list, zum_list=zum_list)# html로 출력값 전달

@app.route('/<path:name>')
def start(name):
    return send_from_directory('', name)#html 파일경로

if __name__ == '__main__':
    app.run(port=5000)#127.0.0.1:5000의 주소를 사용
