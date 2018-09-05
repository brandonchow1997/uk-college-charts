from snownlp import SnowNLP
import pymongo


def get_text():
    textlist = []
    with open('诺丁汉大学（The University of Nottingham）.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # 分割
            item = line.strip('\r').strip('\n')
            textlist.append(item)
        return textlist


def process(data):
    for item in data:
        print(item)
        s = SnowNLP(item)
        score = s.sentiments
        print(score)
        info = {
            'score': score
        }
        save_to_mongo(info)
        print('-'*20)


# 存储到数据库
def save_to_mongo(data):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(data):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_college'
MONGO_COLLECTION = 'comments_Nottingham'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


if __name__ == '__main__':
    data = get_text()
    process(data)