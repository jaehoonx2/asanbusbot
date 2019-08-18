from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
from InfoRequester import InfoRequester

class Asanbusbot :
        # 멤버변수
        requester = None
        updater = None

        # 생성자
        def __init__(self, tokenFileName, dbFileName):
                # requester 초기화
                self.requester = InfoRequester(dbFileName)

                # 토큰 파일 읽기 및 updater 초기화
                with open(tokenFileName, "r") as f:
                        token = f.readline()
                self.updater = Updater(token)

        # callback functions
        def cb_start_command(self, bot, update):
                update.message.reply_text("아산시내버스알리미입니다.\n정류장 이름을 입력해주세요.")

        def cb_message(self, bot, update):
                msgList = self.requester.requestBusInfo( update.message['text'] )

                if msgList :
                        for msg in msgList :
                                update.message.reply_text(msg)
                else :
                        update.message.reply_text("해당 정류장이 존재하지 않습니다.")

        def startBot(self):
                # 메시지 핸들러 등록
                message_handler = MessageHandler(Filters.text, self.cb_message)
                self.updater.dispatcher.add_handler(message_handler)
                
                # 명령어 핸들러 등록
                start_handler = CommandHandler('start', self.cb_start_command)
                self.updater.dispatcher.add_handler(start_handler)                

                print('start telegram chat bot')
                self.updater.start_polling(timeout=3, clean=True)
                self.updater.idle()

# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
        bot = Asanbusbot('asanbusbot_key.txt', 'db_connInfo.txt')
        bot.startBot()