# 디비 처리, 연결, 해제, 검색어 가져오기, 데이터 삽입
import pymysql as my

class DBHelper:
    # 멤버변수 : 커넥션
    conn = None

    # 생성자 - 초기화 시 디비 자동 연결
    def __init__(self, dbInfoFileName):
        self.initDB(dbInfoFileName)

    # 멤버함수
    def initDB(self, dbInfoFileName):
        # dbInfoFile 은 MariaDB 연결에 필요한
        # host, user, password, db 정보를 라인별로 갖고 있음
        # 파일을 읽어 conn_info에 저장한 후 DB 연결에 사용한다
        with open(dbInfoFileName, 'rt', encoding='euc-kr') as f:
            info = f.readlines()

        conn_info = []
        for temp in info :
            conn_info.append(temp.rstrip())

        self.conn = my.connect(
                        host        = conn_info[0],
                        user        = conn_info[1],
                        password    = conn_info[2],
                        db          = conn_info[3],
                        charset     = 'utf8',
                        cursorclass = my.cursors.DictCursor )

    def freeDB(self):
        if self.conn:
            self.conn.close()

    # id를 새로운 포맷으로 변환
    def getNewId(self, id) :
        if len(id) < 2 :
            newId = '28800000' + id
        elif len(id) < 3 :
            newId = '2880000' + id
        elif len(id) < 4 :
            newId = '288000' + id
        elif len(id) < 5 :
            newId = '28800' + id
        elif len(id) < 6 :
            newId = '2880' + id
        else :
            newId = id

        return newId

    # 버스정류장 데이터 삽입하기 => 만약 이미 정류장(name, id1)이 존재하면 id2에 저장
    def insertStop(self, name, id):
        newId = self.getNewId(id)   # 포맷 변환

        # 커서 오픈
        # with => 닫기 처리를 자동으로 처리해준다 => I/O 많이 사용
        with self.conn.cursor() as cursor:
            sql = '''
            INSERT INTO stops (name, id1)
            VALUES ( %s, %s )
            ON DUPLICATE KEY UPDATE id2 = %s;
            '''
            cursor.execute(sql, ( name, newId, newId ) )
        self.conn.commit()

    # 버스정류장 아이디 가져오기 => ID가 2개면 2개 모두 가져옴
    def selectStopId(self, name):
        idList = None

        with self.conn.cursor() as cursor:
            sql = "SELECT id1, id2 FROM stops WHERE name = %s;"
            cursor.execute(sql, name)
            idList = cursor.fetchall()
            #print(idList)
            if type(idList) is tuple :  # DB에 해당 정류장 없으면 => empty list 반환
                return []
            else :                      # 있으면 => values list 반환
                return list(idList[0].values())

    # 버스정류장 데이터 삭제하기
    def deleteStop(self, name):
        with self.conn.cursor() as cursor:
            sql = "DELETE FROM stops WHERE name = %s;"
            cursor.execute(sql, name)
        self.conn.commit()

    # 버스정류장 이름 업데이트하기 => DB stability가 깨질 수도 있으니 조심
    def updateStopName(self, name, newName):
        with self.conn.cursor() as cursor:
            sql = '''
            UPDATE stops
            SET name = %s
            WHERE name = %s;
            '''
            cursor.execute(sql, (newName, name))
        self.conn.commit()

    # 버스정류장 아이디 업데이트하기 => 아이디(id2)의 경우는 삭제(id2 = None)도 가능
    def updateStopId(self, name, idNum, newId=None):
        """
        targetId = ""
        if idNum == 1 :
            targetId = "id1"

            if newId :  # id1(PK)을 None으로 바꾸려 한다면 ERROR
                print("ERROR : id1 is PRIMARY KEY.")
                return None
        elif idNum == 2 :
            targetId = "id2"

            if newId :  # newId가 NULL이 아니면 포맷 변환
                newId = self.getNewId(newId)
        else :
            print("ERROR : parameter IdNum must be either 1 or 2.")
            return None

        with self.conn.cursor() as cursor:
            sql = '''
            UPDATE stops
            SET %s = %s
            WHERE name = %s;
            '''
            cursor.execute(sql, (targetId, newId, name))
        self.conn.commit()
        """
        pass


# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
    db = DBHelper("db_connInfo.txt")        # 연결
    '''
    print(db.selectStopId("온양초등학교"))   # 조회 - id가 2개인 경우
    print(db.selectStopId("휴대리입구"))     # 조회 - id가 1개인 경우
    print(db.selectStopId("없는정류장"))     # 조회 - 존재하지 않는 정류장일 경우

    print("test 이름 갱신 - abcd")
    db.updateStopName("test", "abcd")
    print(db.selectStopId("abcd"))

    print("test가 남아있는지 확인")
    print(db.selectStopId("test"))

    print("abcd 제거")
    db.deleteStop("abcd")
    print(db.selectStopId("abcd"))
    
    print("test 삽입")
    db.insertStop("test", "1234")
    print(db.selectStopId("test"))

    print("test 재삽입 - id2")
    db.insertStop("test", "5678")             
    print(db.selectStopId("test"))

    print("ERROR - PK is not null")
    db.updateStopId("test", 1)
    print(db.selectStopId("test"))

    print("id1 change")
    db.updateStopId("test", 1, "9999999999")
    print(db.selectStopId("test"))

    print("id2 NULL changed")
    db.updateStopId("test", 2)
    print(db.selectStopId("test"))

    print("id2 NULL changed")
    db.updateStopId("test", 2, "9999999999")
    print(db.selectStopId("test"))
    '''    
    db.freeDB()                             # 해제