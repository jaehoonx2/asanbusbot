import telegram
from bus_InfoRequester import InfoRequester
from telegram.ext import Updater, MessageHandler, Filters   # Telegram Bot 이 사용자의 메시지에 응답하도록 함

def readToken() :
    with open("asanbusbot_key.txt", "r") as f:
        token = f.readline()
    return token

# 메시지핸들러 설정(텍스트에 대해 응답, 콜백함수)
def addMessageHandler(botUpdater, msg_callback_func) :
    msgHandler = MessageHandler(Filters.text, msg_callback_func)
    botUpdater.dispatcher.add_handler(msgHandler)

# msg_callback_func    
def replyMessage(bot, botUpdater) :
    msgList = req.requestBusInfo( botUpdater.message['text'] )
    
    if msgList :
        for msg in msgList :
            botUpdater.message.reply_text(msg)
    else :
            botUpdater.message.reply_text("No such stop.")

# cmd_callback_func
def helpCommand(bot, botUpdater) :
    botUpdater.message.reply_text(helpMsg)

# init
myToken = readToken()
bot = telegram.Bot(token = myToken)
updater = Updater(myToken)
req = InfoRequester()

# 핸들러 적용
addMessageHandler(updater, replyMessage)

# 실행
updater.start_polling(timeout = 3, clean = True)        # polling 설정 및 updater 돌리기
updater.idle()                                          # 계속 실행되게 만들기