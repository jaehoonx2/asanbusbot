from DBHelper import *

class CSVHelper :
    # 멤버변수 : db
    db = None
    
    # 생성자
    def __init__(self, dbFileName):
        self.db = DBHelper(dbFileName);

    # 멤버함수
    # 버스정류장 CSV 파일을 파싱하여 mariaDB에 삽입
    def insertCSV(self, csvFileName) :
        with open(csvFileName, 'rt', encoding='euc-kr') as f:
            stops = f.readlines()[1:]

        for stop in stops :
            columns = stop.split(",")
            id, name = columns[0], columns[1]

            # print(name, id)
            self.db.insertStop(name, id)            # MariaDB에 데이터 삽입
            print(name, self.db.selectStopId(name)) # 삽입 결과 확인 (id1, id2)

# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
    csvObj = CSVHelper('db_connInfo.txt')
    csvObj.insertCSV('bus_stops_list.csv')
    csvObj.db.freeDB();