import requests              # POST 요청을 보내기 위함
import json
import telegram
from pprint import pprint

bot = telegram.Bot(token = 'YOUR_BOT_TOKEN')

# 들어간 사이트가 아닌 버스 정보 데이터가 오는 URL. chrome devtool - network에서 확인 가능
srcURL = "http://bus.asan.go.kr/mobile/traffic/searchBusStopRoute"

# 서버의 요청으로 인식하도록 가짜 헤더 만들기
fake_header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Referer' : 'http://bus.asan.go.kr/web/bus_arrInfo_pop?busStopId=288000863'
}

# busStopInfo : Post 요청 메시지에 추가 데이터로 들어갈 버스 정류장 정보
busStopInfo = { 'busStopId' : '288000863' }     # 온양초등학교

def getUserID(bot) :
    return bot.getUpdates()[-1].message.chat.id

def sendBusInfoMsg(url, header, data, user) :
    # 중요 : POST 방식을 사용함
    # 가짜 헤더와 추가 데이터를 넣어서 POST 요청한다.
    res = requests.post(url, headers = header, data = data)
    msg = ""

    if res.status_code == requests.codes.ok:    
        bus_data = json.loads(res.text)         # json 형태로 변환
        # pprint(bus_data)

        for info in bus_data['busStopRouteList'] :
            msg += "%s번 도착 예정 시간 : %s 현재 위치 : %s\n" % (info['route_name'], info['provide_type'], info['rstop'])
    
        bot.sendMessage(chat_id = user, text = msg)
    else :
        bot.sendMessage(chat_id = user, text = "Crawl Failed")

sendBusInfoMsg(srcURL, fake_header, busStopInfo, getUserID(bot))