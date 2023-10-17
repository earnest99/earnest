import requests
from bs4 import BeautifulSoup
import json

# Slack 웹훅 URL 설정
slack_webhook_url = "https://hooks.slack.com/services/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"

# 날씨 정보 URL 설정
weather_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8"

def send_slack_webhook(str_text):
    """
    입력된 텍스트를 Slack 웹훅으로 전송하는 함수
    Args: str_text (str): 전송할 텍스트
    Returns: str: 전송 결과 ("OK" 또는 "error")
    """
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "text": str_text
    }
    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))
    if res.status_code == 200:
        return "OK"
    else:
        return "error"


#온도 크롤링
def get_current_temperature():
    response = requests.get(weather_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')


    tmp_elements = soup.select('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.weather_graphic > div.temperature_text > strong')

    print(tmp_elements[0].text)
    t=tmp_elements[0].text
    t=t.split('도')
    return t[1]

#날씨 크롤링
def get_current_weather():
    response = requests.get(weather_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')


    wth_elements = soup.select('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.temperature_info > p > span.weather.before_slash')

    print(wth_elements[0].text)
    w=wth_elements[0].text
    return w

#아이콘 설정
def get_icon(current_weather):
    if current_weather=='맑음':
        icon='☀'
    elif current_weather=='구름많음':
        icon='☁'
    elif current_weather=='구름조금':
        icon='🌤'
    elif current_weather=='흐림':
        icon='⛅'
    elif current_weather=='흐리고 비':
        icon='🌧'
    elif current_weather=='비':
        icon='☔'
    else:
        icon='🌡'
    return icon



# 현재 날씨 가져오기
current_temperature = get_current_temperature()
current_weather = get_current_weather()
current_icon=get_icon(current_weather)

#메세지 전송
message = "날씨: {} {}, 현재 온도: {}".format(current_weather,current_icon,current_temperature)
print(send_slack_webhook(message))
