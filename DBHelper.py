# 디비 처리, 연결, 해제, 검색어 가져오기, 데이터 삽입
import pymysql as my

class DBHelper:
    
    # 멤버변수 : 커넥션
    conn = None
    conn_info = []

    # 생성자
    def __init__(self):
        self.initDB()
    
    # 멤버함수
    def initDB(self):
        # db_connInfo.txt는 MariaDB 연결에 필요한
        # host, user, password, db 정보를 라인별로 갖고 있음
        # 파일을 읽어서 변수(conn_info)에 저장한 후
        # 그 변수를 DB 연결에 사용한다. (유출 방지)
        with open('db_connInfo.txt', 'rt', encoding='euc-kr') as f:
            info = f.readlines()

        for temp in info :
            self.conn_info.append(temp.rstrip())
        
        self.conn = my.connect(
                        host        = self.conn_info[0],
                        user        = self.conn_info[1],
                        password    = self.conn_info[2],
                        db          = self.conn_info[3],
                        charset     = 'utf8',
                        cursorclass = my.cursors.DictCursor )

    def freeDB(self):
        if self.conn:
            self.conn.close()

    # 버스정류장 아이디 가져오기
    def selectStopIds(self, stopname):
        # 커서 오픈
        # with => 닫기 처리를 자동으로 처리해준다 => I/O 많이 사용
        idList = None
        with self.conn.cursor() as cursor:
            sql = "SELECT id1, id2 FROM stops WHERE name = %s;"
            cursor.execute( sql, stopname )
            idList = cursor.fetchall()
            #print(idList)
            if type(idList) is tuple :  # DB에 해당 정류장 없으면 => empty list 반환
                return []
            else :                      # 있으면 => values list 반환
                return list(idList[0].values())
    
    # 버스정류장 데이터 삽입하기 => 만약 이미 존재하면 아이디를 하나 더 추가한다
    def insertStopData( self, name, id ):
        with self.conn.cursor() as cursor:
            sql = '''
            INSERT INTO stops (name, id1)
            VALUES ( %s, %s )
            ON DUPLICATE KEY UPDATE id2 = %s;
            '''
            cursor.execute(sql, ( name, id, id ) )
        self.conn.commit()


# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__' :
    db = DBHelper() # 연결
    db.freeDB()     # 해제