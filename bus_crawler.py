import requests                                                             # POST 요청을 보내기 위함
import json
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler   # Telegram Bot 이 사용자의 메시지에 응답하도록 함
from pprint import pprint
# from apscheduler.schedulers.blocking import BlockingScheduler

myToken = 'Your_Bot_Token'

# 들어간 사이트가 아닌 버스 정보 데이터가 오는 URL. chrome devtool - network에서 확인 가능
srcURL = "http://bus.asan.go.kr/mobile/traffic/searchBusStopRoute"

# 서버의 요청으로 인식하도록 가짜 헤더 만들기
fake_header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Referer' : 'http://bus.asan.go.kr/web/bus_arrInfo_pop?busStopId=288000863'
}

# busStopInfo : Post 요청 메시지에 추가 데이터로 들어갈 버스 정류장 정보
busStopInfo = {
        'busStopId' : '288000863'               # 온양초등학교
}

def getUserID(bot) :
    return bot.getUpdates()[-1].message.chat.id

# 가짜 헤더와 추가 데이터를 넣어서 url에 POST 요청한다.
def sendBusInfoMsg(bot, url, header, data, user) :
    # bot : telegram bot object
    # url : 버스 정보 데이터
    # header, data : 패킷의 헤더와 데이터
    # user : 메시지를 전송할 chatid
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

def getMessage(bot, update) :
    update.message.reply_text("I got a text.")
    update.message.reply_text(update.message.text)

def helpCommand(bot, update) :
    update.message.reply_text("무엇을 도와드릴까요?")


bot = telegram.Bot(token = myToken)

updater = Updater(myToken)                              # 봇의 업데이트 사항이 있으면 가져오는 클래스

msgHandler = MessageHandler(Filters.text, getMessage)   # 메시지핸들러 설정(텍스트에 대해 응답, 콜백함수)
updater.dispatcher.add_handler(msgHandler)              # 업데이터에 핸들러 추가

helpHandler = CommandHandler('help', helpCommand)       # 커맨드핸들러 설정(특정 커맨드, 콜백함수)
updater.dispatcher.add_handler(helpHandler)             # 업데이터에 핸들러 추가

updater.start_polling(timeout = 3, clean = True)        # polling 설정 및 updater 돌리기
updater.idle()                                          # 계속 실행되게 만들기

# 스케쥴러 세팅해서 주기적으로 유저에게 메시지 보내기
#sched = BlockingScheduler()
# lambda is a callable
#sched.add_job(lambda: sendBusInfoMsg(bot, srcURL, fake_header, busStopInfo, getUserID(bot)), 'interval', seconds=30)
#sched.start()

# 채널(public)로 메시지 보내기 - bot이 채널의 관리자로 등록되어 있어야 함
#user = '@******'  # Invite Link = t.me/******
#bot.sendMessage(chat_id = user, text = "Hello, I'm a bot").chat_id
