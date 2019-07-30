# bus_firebase.py
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


# 아산 시내버스 정류장 정보 파싱,
# 파싱 데이터를 파이어베이스에 Insert
def putCSVIntoFirebase(csvFileName) :
    db = initFirebase()
   
    with open(csvFileName, 'rt', encoding='euc-kr') as f:
        stops = f.readlines()[1:]

    for stop in stops :
        columns = stop.split(",")
        key, busStopName = columns[0], columns[1]
        setData(db, key, busStopName)
        print(key, busStopName)


def setData(db, key, busStopName) :
    # busStopId 를 key Format 으로 변환
    if len(key) < 2 :
        busStopId = '28800000' + key
    elif len(key) < 3 :
        busStopId = '2880000' + key
    elif len(key) < 4 :
        busStopId = '288000' + key
    elif len(key) < 5 :
        busStopId = '28800' + key
    elif len(key) < 6 :
        busStopId = '2880' + key
    else :
        busStopId = key

    # data 작성
    data = { "busStopName" : busStopName }

    # 경로 설정 및 저장
    db.child('busStops').child(busStopId).set(data)


def updateData(db, busStopId) :
    pass


def removeData(db, busStopId) :
    pass


def getNameById(db, busStopId) :
    pass


def getIdByName(db, busStopName) :
    pass