import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os

this_program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_program_directory)

fcsv = open('data/data_champion.csv','w',newline='')
writer = csv.writer(fcsv)
writer.writerow(['name','kor_name','tag1','tag2','attack_range','region','related_champions','release_code'])

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36"}

with open("champion.json", 'rt', encoding='UTF8') as f:
    json_format = json.load(f)

json_list = json_format["data"]
url_univ = "https://universe.leagueoflegends.com/en_US/champion/"
url_release = "https://namu.wiki/w/%EB%A6%AC%EA%B7%B8%20%EC%98%A4%EB%B8%8C%20%EB%A0%88%EC%A0%84%EB%93%9C/%EC%B1%94%ED%94%BC%EC%96%B8/%EC%B6%9C%EC%8B%9C%EC%9D%BC"

release_order = []
res_release = requests.get(url_release,headers=header)
soup_release = BeautifulSoup(res_release.text,"lxml")

for aclass in soup_release.find_all('a', {'class':"e0gNwMKL"}): #날마다 바뀜
    champ = aclass.find('span')
    if champ is None:
        continue
    else:
        cham_name = champ.string
        if cham_name == "4월 1일" or cham_name == "우르프" or cham_name == "☆":
            continue
        if cham_name is None:
            cham_name = aclass['title']
        cham_name=cham_name.strip()
        release_order.append(cham_name)


for name, detail in json_list.items():
    name = name.lower()
    kor_name = detail["name"]
    tags = detail["tags"]
    tag1 = tags[0]
    tag2 = tags[1] if len(tags) > 1 else "RIP"
    attack_range = detail["stats"]["attackrange"]

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("headless")
    driver_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36")
    driver = webdriver.Chrome(options=driver_options)
    if name=="renata":
        driver.get(url_univ+"renataglasc")
    else:
        driver.get(url_univ+name)
    time.sleep(2)
    soup_univ = BeautifulSoup(driver.page_source,"lxml")
    region = soup_univ.find('div',{'class':"top_1SjP"}).select_one("h6>span").string

    try:
        related_champions = name + ',' + ','.join(list(map(lambda x:x.find('h5').string.lower() ,soup_univ.find('ul',{'class':"relatedChampionsContainer_28pc"}).find_all('li',{'class':"champion_1xlO"}))))
    except:
        related_champions = name
    
    release_code = release_order.index(kor_name)
    
    writer.writerow([name,kor_name,tag1,tag2,attack_range,region,related_champions,release_code])

fcsv.close()



