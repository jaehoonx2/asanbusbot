# bus_firebase.py
# 1. 아산 시내버스 정류장 CSV File을 파싱하여 Firebase에 저장
# 2. Firebase 내에 저장되어 있는 정류장 정보를 CRUD
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
        createData(db, key, busStopName)
        print(key, busStopName)


# Create
def createData(db, key, busStopName) :
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


# Read(ID)
def readIdByName(db, busStopName) :
    pass


# Read(Name)
def readNameById(db, busStopId) :
    stop = db.child('busStops').child(busStopId).get().val()
    return stop['busStopName']


# Update(ID)
def updateBusStopId(db, busStopId, newId) :
    name = readNameById(db, busStopId)
    deleteData(db, busStopId)
    createData(db, newId, name)


# Update(Name)
def updateBusStopName(db, busStopId, newName) :
    db.child('busStops').child(busStopId).update({ "busStopName" : newName })


# Delete
def deleteData(db, busStopId) :
    db.child('busStops').child(busStopId).remove()