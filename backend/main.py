from fastapi import FastAPI
import pandas as pd
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os
import threading
import similarity
import statistics
import schedule
import time

this_program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_program_directory)


app = FastAPI()

origins = [
    "http://www.lolmantle.kro.kr:8001",
    "http://www.lolmantle.kro.kr"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = pd.read_csv("data/data.csv",encoding='utf-8')

app.mount("/css", StaticFiles(directory="../frontend/css"))
app.mount("/js", StaticFiles(directory="../frontend/js"))
app.mount("/favicon", StaticFiles(directory="../frontend/favicon"))


def server_update():
    print("update start/" + str(time.localtime()))
    doing = -1
    doing = statistics.writing_statistics()
    while True:
      time.sleep(1)
      if doing == 0:
        break
    #similarity.writing_similarity()
    similarity.updating_similarity()
    print("update end/" + str(time.localtime()))


def update_schedule():
    schedule.every().day.at("14:55").do(server_update)
    #schedule.every().day.at("03:34").do(server_update)
    while True:
        schedule.run_pending()
        time.sleep(60)

ans_code = data.index[(data['rank']==0)]
if ans_code != similarity.hashcham():
    similarity.writing_similarity()

thread_up = threading.Thread(target=update_schedule)
thread_up.start()

@app.get("/")
def index():
    return FileResponse("../frontend/index.html")

@app.get("/{guess_name}")
async def ans(guess_name):
    try:
        data = pd.read_csv("data/data.csv",encoding='utf-8')
        guess_code = data.index[(data['name']== guess_name)]
        guess = data.loc[guess_code]
        return {"이름":guess['kor_name'].item(),"순위":guess['rank'].item(),"유사도":guess['simularity'].item(),"역할군1":guess['tag1'].item(),"역할군2":guess['tag2'].item(),"사거리":guess['attack_range'].item(),"라인1":guess['position1'].item(),"라인2":guess['position2'].item(),"룬":guess['rune'].item(),"아이템":guess['items'].item(),"티어":guess['tier'].item(),"지역":guess['region'].item(),"관련 챔피언":guess['related_champions'].item(),"출시순":guess['release_code'].item()+1}
    except:
        return dict()


"""guess_code = -1
while guess_code != ans_code:
    guess_name = input("챔피언의 이름을 입력해주세요:")
    try:
        guess_code = data.index[(data['kor_name']== guess_name)]
    except:
        print("챔피언을 찾을 수 없습니다.")
        continue
    guess = data.loc[guess_code]

    print("순위:"+ guess['rank'].to_string(index=False) + "위, 유사도:" + guess['simularity'].to_string(index=False) + "%")
    #print("역할군:%f, 사거리:%d, 라인:%d, 룬:%d, 아이템:%d, 티어:%d, 지역:%d, 관련챔피언:%d" %(tag_point, attack_range_point, position_point , rune_point , items_point , tier_point , region_point , related_point))

print("성공!")"""


"""cd ../ubuntu/lolmantle/backend   [경로변경]

nohup /home/rsa-key-20240129/.local/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8001 --workers 4 &  [서버실행]


ps -ef     [pid 찾기]
/usr/bin/python3 /home/rsa-key-20240129/.local/bi 찾기
kill -9 (PID)   [서버 프로세스 종료]"""