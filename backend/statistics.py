import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

this_program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_program_directory)

korenglst = dict()

def writing_statistics():
    url_1 = "https://www.op.gg/champions/"
    url_2 = "/build"
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36"}


    data = pd.read_csv("data/data_champion.csv",encoding='utf-8')
    data['position1'] = ""
    data['position2'] = ""
    data['rune'] = ""
    data['items'] = ""

    for idx,ser in data.iterrows():
        name = ser['name'].lower()

        time.sleep(1)
        res = requests.get(url_1+name+url_2,headers=header)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        positions =  soup.find_all('div',{'data-key':"FILTER-POSITION"})
        data.loc[idx,'position1'] = positions[0]['data-value'] if len(positions) > 0 else "RIP"
        data.loc[idx,'position2'] = positions[1]['data-value'] if len(positions) > 1 else "RIP"

        data.loc[idx,'rune'] = soup.find('div',{'class':"css-19js88b e1y8mv8s1"}).find('img')['alt']
        data.loc[idx,'items'] = ','.join(list(map(lambda x:x['alt'], soup.find('div',{'class':"css-37vh9h e1rgp2h81"}).find_all('img'))))
        try:
            tier = soup.find('div',{'class':"tier-icon"}).find('img')['alt']
            if tier=="op":
                tier = 0
        except:
            tier = "6"
        data.loc[idx,'tier'] = tier

        korenglst[ser['kor_name']] = ser['name']

    data.to_csv("data/data_statistics.csv",index=False)
    return 0

if __name__ == "__main__":
    writing_statistics()
    print(korenglst)