from DBHelper import *

class CSVHelper :
    # 멤버변수 : db
    db = None
    
    # 생성자
    def __init__(self):
        self.db = DBHelper();

    # 멤버함수
    # id를 새로운 포맷으로 변환
    def getNewId(self, id) :
        if len(id) < 2 :
            NewId = '28800000' + id
        elif len(id) < 3 :
            NewId = '2880000' + id
        elif len(id) < 4 :
            NewId = '288000' + id
        elif len(id) < 5 :
            NewId = '28800' + id
        elif len(id) < 6 :
            NewId = '2880' + id
        else :
            NewId = id

        return NewId

    # CSV 파일을 파싱하여 mariaDB에 삽입
    def insertCSV(self, csvFileName) :
        with open(csvFileName, 'rt', encoding='euc-kr') as f:
            stops = f.readlines()[1:]

        for stop in stops :
            columns = stop.split(",")
            id, stop_name = columns[0], columns[1]

            stop_id = self.getNewId(id)

            print(stop_name, stop_id)
            self.db.insertStopData(stop_name, stop_id)     # MariaDB에 데이터 삽입

# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
    csvObj = CSVHelper()
    csvObj.insertCSV('bus_stops_list.csv')