import pymongo
import pandas as pd


def to_csv():
    client = pymongo.MongoClient('localhost')
    cur = client["zhihu_topic"]["topic_comments_college"]
    data = pd.DataFrame(list(cur.find()))
    del data["_id"]
    del data['vote_count']
    del data['name']
    del data['gender']
    # 存储的时候可以做一些数据清洗的工作,清洗脏数据
    data.to_csv("college.csv", encoding='utf-8')


if __name__ == '__main__':
    to_csv()