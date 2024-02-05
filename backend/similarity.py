import numpy as np 
import pandas as pd
import datetime as dt 
import hashlib
import os
import time

this_program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_program_directory)

data = pd.read_csv("data/data_statistics.csv",encoding='utf-8')
champions_cnt = len(data)

def hashcham():
    n = dt.datetime.now() + dt.timedelta(hours=9) + dt.timedelta(minutes=5)
    today = n.strftime("%y%m%d")
    hashtoday = int(hashlib.md5(today.encode('cp949')).hexdigest(),16)
    return hashtoday%champions_cnt

def tags_simularity(x1,y1,x2,y2):
    tags_dict = {"Assassin":np.array([1,0,0,0,0,0]),"Fighter":np.array([0,1,0,0,0,0]),"Mage":np.array([0,0,1,0,0,0]),"Marksman":np.array([0,0,0,1,0,0]),"Support":np.array([0,0,0,0,1,0]),"Tank":np.array([0,0,0,0,0,1]),"RIP":np.array([0,0,0,0,0,0])}
    loop_tag = tags_dict[x1] + tags_dict[y1] * 0.5
    ans_tag = tags_dict[x2] + tags_dict[y2] * 0.5

    loop_norm = np.linalg.norm(loop_tag)
    ans_norm = np.linalg.norm(ans_tag)
    if loop_norm == 0 or ans_norm == 0:
        return 0
    return (loop_tag.dot(ans_tag)/(loop_norm * ans_norm))

def positions_simularity(x1,y1,x2,y2):
    positions_dict = {"top":np.array([1,0,0,0,0]),"jungle":np.array([0,1,0,0,0]),"mid":np.array([0,0,1,0,0]),"adc":np.array([0,0,0,1,0]),"support":np.array([0,0,0,0,1]),"RIP":np.array([0,0,0,0,0])}
    loop_position = positions_dict[x1] + positions_dict[y1] * 0.5
    ans_position = positions_dict[x2] + positions_dict[y2] * 0.5

    loop_norm = np.linalg.norm(loop_position)
    ans_norm = np.linalg.norm(ans_position)
    if loop_norm == 0 or ans_norm == 0:
        return 0
    return (loop_position.dot(ans_position)/(loop_norm * ans_norm))
    

def attack_range_simularity(a,b):
    if a <= 325 and b <= 325:
        return (200-abs(a-b))/400 + 0.5
    elif a > 325 and b > 325:
        return (300-abs(a-b))/600 + 0.5
    else:
        return 0


def rune_region_simularity(a,b):
    if a==b:
        return 1
    return 0

def itmes_simularity(xlst,ylst):
    xset = set(xlst)
    yset = set(ylst)
    interxy = xset & yset
    r = 0
    w = {0:0.5,1:0.3,2:0.2,3:0.2}

    rt = 0
    for i in interxy:
        xi = xlst.index(i)
        yi = ylst.index(i)
        if xi == yi:
            r += w[xi]
        else:
            r += 0.1
    
    return min(1,r)

def tier_simularity(a,b):
    return (6-abs(a-b))/6

def related_champions_simularity(x,y,xlst,ylst):
    r = 0
    if x in ylst:
        r += 0.5
    if y in xlst:
        r += 0.5
    return r

def writing_similarity():

    ans_code = hashcham()
    ans = data.loc[ans_code]

    point_lst = []


    for loop_code in range(champions_cnt):
        loop = data.loc[loop_code]
        
        tag_point = tags_simularity(ans['tag1'],ans['tag2'],loop['tag1'],loop['tag2']) * 10
        attack_range_point = attack_range_simularity(int(ans['attack_range']),int(loop['attack_range'])) * 4
        position_point = positions_simularity(ans['position1'],ans['position2'],loop['position1'],loop['position2']) * 20
        rune_point = rune_region_simularity(ans['rune'],loop['rune']) * 10
        items_point = itmes_simularity(ans['items'].split(","),loop['items'].split(",")) * 15
        tier_point = tier_simularity(int(ans['tier']),int(loop['tier'])) * 5
        region_point = rune_region_simularity(ans['region'],loop['region']) * 20
        related_point = related_champions_simularity(ans['name'],loop['name'],ans['related_champions'].split(","),loop['related_champions'].split(",")) * 15
        release_point = (champions_cnt-abs(ans['release_code']-loop['release_code']))/champions_cnt

        point = tag_point + attack_range_point + position_point + rune_point + items_point + tier_point + region_point + related_point + release_point
        point_lst.append(round(point,2))

    data['simularity'] = point_lst
    data['rank'] = data['simularity'].rank(ascending=False,method='min').astype(int)-1
    data.to_csv("data/data.csv",index=False)

def updating_similarity():

    ans_code = hashcham()
    ans = data.loc[ans_code]

    point_lst = []


    for loop_code in range(champions_cnt):
        loop = data.loc[loop_code]
        
        tag_point = tags_simularity(ans['tag1'],ans['tag2'],loop['tag1'],loop['tag2']) * 10
        attack_range_point = attack_range_simularity(int(ans['attack_range']),int(loop['attack_range'])) * 4
        position_point = positions_simularity(ans['position1'],ans['position2'],loop['position1'],loop['position2']) * 20
        rune_point = rune_region_simularity(ans['rune'],loop['rune']) * 10
        items_point = itmes_simularity(ans['items'].split(","),loop['items'].split(",")) * 15
        tier_point = tier_simularity(int(ans['tier']),int(loop['tier'])) * 5
        region_point = rune_region_simularity(ans['region'],loop['region']) * 20
        related_point = related_champions_simularity(ans['name'],loop['name'],ans['related_champions'].split(","),loop['related_champions'].split(",")) * 15
        release_point = (champions_cnt-abs(ans['release_code']-loop['release_code']))/champions_cnt

        point = tag_point + attack_range_point + position_point + rune_point + items_point + tier_point + region_point + related_point + release_point
        point_lst.append(round(point,2))

    data['simularity'] = point_lst
    data['rank'] = data['simularity'].rank(ascending=False,method='min').astype(int)-1
    while True:
        now = dt.datetime.now()
        if now.hour == 0:
            data.to_csv("data/data.csv",index=False)
            return
        time.sleep(1)

if __name__ == "__main__":
    writing_similarity()