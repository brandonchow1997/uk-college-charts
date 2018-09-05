import requests
import pymongo
from tqdm import tqdm
import time


# 利用cookie模拟登录知乎，请求topic页面
def login_zhihu_ajax(cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36 '
    }
    # 传入cookie:'z_c0'
    cookies = {
        # 我的账号的cookie
        'z_c0': '{cookie}'.format(cookie=cookie)
    }
    # 显示80个关注的topic（参数limit改变数量）
    url = "https://www.zhihu.com/followed_topics?offset=0&limit=80"
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.json()


# 解析topic页面返回的json数据
def parse_page_json_test(html_json):
    url_token_list = []
    name_list = []
    data = html_json['payload']
    print('--- 已获取关注的话题%s个 ---' % len(data))
    pbar = tqdm(data)
    for item in pbar:
        time.sleep(0.4)
        name = item['name']
        pbar.set_description("Processing Topic:%s..." % name)
        url_token = item['url_token']
        url_top_answers = 'https://www.zhihu.com/topic/{url_token}/top-answers'.format(url_token=url_token)
        introduction = item['introduction']
        # 生成topic字典
        print('topic:', name)
        print(introduction)
        print('=' * 80)
        url_token_list.append(url_token)
        name_list.append(name)
        # 存入数据库的代码
        topic_info = {
            'name': name,
            'url_token': url_token,
            'url': url_top_answers,
            'introduction': introduction
        }
        # 存入数据库中
        save_to_mongo(topic_info)
        # 返回话题的url_token属性和name属性
    # print(url_token_list)
    return len(data), url_token_list, name_list


# 解析topic页面返回的json数据
def parse_page_json(html_json):
    url_token_list = []
    name_list = []
    data = html_json['payload']
    print('--- 已获取关注的话题%s个 ---' % len(data))
    for item in data:
        name = item['name']
        url_token = item['url_token']
        introduction = item['introduction']
        # 生成topic字典
        print('topic:', name)
        print(introduction)
        print('=' * 80)
        url_token_list.append(url_token)
        name_list.append(name)
        # 返回话题的url_token属性和name属性
    # print(url_token_list)
    return len(data), url_token_list, name_list


# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_topic'
MONGO_COLLECTION = 'topic_info_college'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


# 存储到数据库
def save_to_mongo(data):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(data):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


#######################################################
# 获取topic函数，被"zhihu_topic_answer"调用
def get_topic(cookie):
    # 爬取ajax异步传输的内容
    html_json = login_zhihu_ajax(cookie)
    # 解析json
    url_answers = parse_page_json(html_json)
    return url_answers


############ TEST
def get_topic_test(cookie):
    # 爬取ajax异步传输的内容
    html_json = login_zhihu_ajax(cookie)
    # 解析json
    url_answers = parse_page_json_test(html_json)
    return url_answers
#######################################################


if __name__ == '__main__':
    get_topic()
