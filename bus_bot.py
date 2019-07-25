import telegram
from bus_crawler import *
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler   # Telegram Bot 이 사용자의 메시지에 응답하도록 함

helpMsg = '''
/help : 도움말
/search : 정류장 검색(미완성)
/alarm : 알람 설정(미완성)
'''

def getUserID(bot) :
    return bot.getUpdates()[-1].message.chat.id

def readToken() :
    with open("bot_key.txt", "r") as f:
        token = f.readline()
    return token

# 메시지핸들러 설정(텍스트에 대해 응답, 콜백함수)
def addMessageHandler(botUpdater, msg_callback_func) :
    msgHandler = MessageHandler(Filters.text, msg_callback_func)
    botUpdater.dispatcher.add_handler(msgHandler)

# 커맨드핸들러 설정(특정 커맨드, 콜백함수)
def addCommandHandler(botUpdater, cmd_name, cmd_callback_func) :
    cmdHandler = CommandHandler(cmd_name, cmd_callback_func)
    botUpdater.dispatcher.add_handler(cmdHandler)

# msg_callback_func    
def replyMessage(bot, botUpdater) :
    botUpdater.message.reply_text("AsanBusBot Testing")

# cmd_callback_func
def helpCommand(bot, botUpdater) :
    botUpdater.message.reply_text(helpMsg)

def searchCommand(bot, botUpdater) :
    botUpdater.message.reply_text(getBusInfo(srcURL, fake_header, busStop))
    
def alarmCommand(bot, botUpdater) :
    pass


# init
myToken = readToken()
bot = telegram.Bot(token = myToken)
updater = Updater(myToken)

# 핸들러 적용
addMessageHandler(updater, replyMessage)
addCommandHandler(updater, 'help', helpCommand)
addCommandHandler(updater, 'search', searchCommand)
#addCommandHandler(updater, 'alarm', alarmCommand)

# 실행
updater.start_polling(timeout = 3, clean = True)        # polling 설정 및 updater 돌리기
updater.idle()                                          # 계속 실행되게 만들기