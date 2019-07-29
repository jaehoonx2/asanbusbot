# firebase.py
# 아산 시내버스 정류장 정보 csv 파일을 파싱하여 firebase에 저장
# 혹은 firebase 내에 저장된 시내버스 정류장 정보를 조회
import pyrebase

# Firebase 인증 및 앱 초기화
def initFirebase() :
    with open("firebase_apiKey.txt", "r") as f:
        apiKey = f.readline()

    config = {
        "apiKey" : apiKey,
        "authDomain" : "asanbusbot.firebaseapp.com",
        "databaseURL" : "https://asanbusbot.firebaseio.com",
        "storageBucket" : "asanbusbot.appspot.com",
        "serviceAccount" : "serviceAccountCredentials.json"     # authenticate as a admin
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    return db


# 아산 시내버스 정류장 정보 파싱
def parseCSV(csvFileName) :
    with open(csvFileName, 'rt', encoding='euc-kr') as f:
        stops = f.readlines()[1:]
    return stops


# 파싱 데이터를 파이어베이스에 Insert
def putCSVIntoFirebase(csvFileName) :
    db = initFirebase()
    stops = parseCSV(csvFileName)

    for stop in stops :
        columns = stop.split(",")
        id, name = columns[0], columns[1]
        setData(db, id, name)
        print(id, name)


def setData(db, busStopId, busStopName) :
    # busStopId 를 key Format 으로 변환
    if len(busStopId) < 2 :
        cusKey = '28800000' + busStopId
    elif len(busStopId) < 3 :
        cusKey = '2880000' + busStopId
    elif len(busStopId) < 4 :
        cusKey = '288000' + busStopId
    elif len(busStopId) < 5 :
        cusKey = '28800' + busStopId
    elif len(busStopId) < 6 :
        cusKey = '2880' + busStopId

    # data 작성
    data = { "busStopName": busStopName }

    # 경로 설정 및 저장
    db.child('busStopId').child(cusKey).set(data)


def updateData(db, busStopId) :
    pass


def removeData(db, busStopId) :
    pass


def getNameById(db, busStopId) :
    pass


def getIdByName(db, busStopName) :
    pass