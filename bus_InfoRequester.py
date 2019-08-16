import requests                                 # POST 요청을 보내기 위함
import json
from pprint import pprint
from DBHelper import *

class InfoRequester :
        # 멤버변수
        db              = None      # MariaDB
        srcURL          = None      # 들어간 사이트가 아닌 버스 정보 데이터가 오는 URL
        fake_header     = None      # 서버의 요청으로 인식하게 하는 가짜 헤더

        # 생성자
        def __init__(self):
                self.db          = DBHelper()
                self.srcURL      = "http://bus.asan.go.kr/mobile/traffic/searchBusStopRoute"
                self.fake_header = {
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                        'Referer' : 'http://bus.asan.go.kr/web/bus_arrInfo_pop?busStopId=288000863'
                }
                self.dataList = []
        
        # 멤버함수
        # DB 에서 받아온 ID들을 POST 요청에 알맞는 데이터 포맷으로 바꾸어 반환하기
        def getDataList ( self, idList ) :
                dataList = []
                for id in idList :
                        if id :         # id 가 존재하면
                                dataList.append({ 'busStopId' : id })

                return dataList

        # 가짜 헤더와 추가 데이터를 넣어서 url에 POST 요청하여 버스정보 얻어오기
        def requestBusInfo( self, stopname ) :
                # DB에서 찾고자 하는 정류장의 id(상,하행)을 가져온다
                idList = self.db.selectStopIds(stopname)        # { id1, id2 }
                # id들을 알맞은 데이터 포맷으로 바꾸어 저장한다
                dataList = self.getDataList(idList)
                msgList =[]
                
                if not dataList :                               # 해당하는 정류장 이름이 없음
                        print("'%s' 정류장이 존재하지 않습니다." % stopname)
                else :
                        for data in dataList :
                                res = requests.post(self.srcURL, headers = self.fake_header, data = data)
                                msg = ""

                                if res.status_code == requests.codes.ok:    
                                        bus_data = json.loads(res.text)         # json 형태로 변환
                                        #pprint(bus_data)
                                        
                                        for info in bus_data['busStopRouteList'] :
                                                msg += "%s번(%s) ETA : %s 현위치 : %s\n" % (info['route_name'], info['route_explain'].rstrip()+'방향', info['provide_type'], info['rstop'])
                                else :
                                        msg = "Request Failed"
                                
                                #print(msg)
                                msgList.append(msg)

                return msgList                

# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
        req = InfoRequester()

        list1 = req.requestBusInfo("온양초등학교")
        print(list1)

        list2 = req.requestBusInfo("휴대리입구")

        
        list3 = req.requestBusInfo("없는 정류장")
        print(list3)