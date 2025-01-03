import requests
import pandas as pd
import json
from datetime import datetime
from time import sleep
import pickle
import numpy as np
import traceback
import logging

def getJSON():
    url = "https://matchapi.delist.cn/integral_rank"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh,zh-CN;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://match.creditscoring.cn/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    data = {
        "keywords": "",
        "pageNum": 1,
        "pageSize": 200,
        "challenge_id": "21",
        "filtrate": "score"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def transTime(_time):
    return int(datetime.strptime(_time, "%Y-%m-%d %H:%M:%S").timestamp())

class UserInfo():
    
    def __init__(self, _phone, _name, _time, _score):
        self.phone = _phone
        self.username = [_name]
        self.scores = [_score]
        self.times = [_time]
        self.timestamp = [transTime(_time)]


    def addScore(self, _time, _score):
        self.scores.append(_score)
        self.times.append(_time)
        self.timestamp.append(transTime(_time))

    def checkNewSubmission(self, data):
        if data['nickname'] not in self.username:
            self.username.append(data['nickname'])
        if transTime(data['update_time']) > self.timestamp[-1]:
            self.addScore(data['update_time'], data['max_score'])

    def getNickname(self):
        return ',\n'.join(self.username)

    def getNewestInfo(self):
        return (self.times[-1], self.scores[-1])
    
    def getMaxInfo(self):
        id = self.scores.index(max(self.scores))
        return (self.times[id], self.scores[id])



class UserTable():
    def __init__(self):
        self.users = {}
    
    def updateUser(self, data):
        if data['username'] in self.users.keys():
            self.users[data['username']].checkNewSubmission(data)
        else:
            self.users[data['username']] = UserInfo(data['username'], data['nickname'], data['update_time'], data['max_score'])

    def getNewestRankTable(self):
        table = {'Nickname':[], 'UpdateTime':[], 'newScore':[], 'maxScore':[], 'listScore':[]}
        for id, user in enumerate(self.users.values()):
            table['Nickname'].append(user.getNickname())
            table['UpdateTime'].append(user.getNewestInfo()[0])
            table['newScore'].append(user.getNewestInfo()[1])
            table['maxScore'].append(user.getMaxInfo()[1])
            table['listScore'].append(user.scores)

        table = pd.DataFrame(table).sort_values(by='maxScore', ascending=False)
        table.loc[:, 'maxRank'] = np.linspace(1, table.shape[0], table.shape[0]).astype(int)

        table = table.sort_values(by='newScore', ascending=False)
        table.loc[:, 'newRank'] = np.linspace(1, table.shape[0], table.shape[0]).astype(int)

        table = table.loc[:, ['newRank', 'maxRank', 'Nickname', 'UpdateTime', 'newScore', 'maxScore', 'listScore']]
        return table

    def getHighestRankTable(self):
        table = {'Nickname':[], 'UpdateTime':[], 'newScore':[], 'maxScore':[], 'listScore':[]}
        for id, user in enumerate(self.users.values()):
            table['Nickname'].append(user.getNickname())
            table['UpdateTime'].append(user.getMaxInfo()[0])
            table['newScore'].append(user.getNewestInfo()[1])
            table['maxScore'].append(user.getMaxInfo()[1])
            table['listScore'].append(user.scores)

        table = pd.DataFrame(table).sort_values(by='newScore', ascending=False)
        table.loc[:, 'newRank'] = np.linspace(1, table.shape[0], table.shape[0]).astype(int)

        table = table.sort_values(by='maxScore', ascending=False)
        table.loc[:, 'maxRank'] = np.linspace(1, table.shape[0], table.shape[0]).astype(int)

        table = table.loc[:, ['maxRank', 'newRank', 'Nickname', 'UpdateTime', 'newScore', 'maxScore', 'listScore']]
        return table

# 存储UserTable对象d
def save_users(users, filename='./data/users.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(users, f)

# 从本地文件加载UserTable对象
def load_users(filename='./data/users.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)


# Init
try:
    users = load_users()
    print('加载完成！')
except:
    data_list = getJSON()['data']['list']
    users = UserTable()
    for data in data_list:
        users.updateUser(data)
    print('初始化完成！')
    

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename='./log/crawler.log',
                    filemode='a')


i = 0
# Loop
while True:
    try:
        data_list = getJSON()['data']['list']
    except:
        logging.error(traceback.format_exc())
        pass
    for data in data_list:
        users.updateUser(data)
    save_users(users)
    users.getNewestRankTable().to_csv('./data/new.csv', index=False)
    users.getHighestRankTable().to_csv('./data/high.csv', index=False)
    
    if i % 50 == 0:
        logging.info(f"{i} :Execute normally!")
    i += 1
    sleep(10)