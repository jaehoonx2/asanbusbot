# firebase.py
# 아산 시내버스 정류장 정보 csv 파일을 파싱하여 firebase에 저장
# 혹은 firebase 내에 저장된 시내버스 정류장 정보를 조회
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Firebase 인증 및 앱 초기화
with open("firebase_url.txt", "r") as f:
    url = f.readline()

cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : url
})

# 시내버스 정류장 정보 파싱
with open('AsanBus.csv', 'rt', encoding='euc-kr') as f:
    stops = f.readlines()[1:]

# firebase db 위치 지정
ref = db.reference('busStopId')

# 데이터 저장
'''
for stop in stops:
    columns = stop.split(",")
    id, name = columns[0], columns[1]
    ref.update({ id : name })
    print(id, name)
'''
# 데이터 조회
print(ref.get())