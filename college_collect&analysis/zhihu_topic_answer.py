import requests
import time
# 引入topic.py
import topics
# 引入zhihu_comments.py
import zhihu_comments

"""
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
"""


def get_answer(page, keyword):
    # retry_count = 5
    # proxy = get_proxy()
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
        }
        topic_id = keyword
        # base_url
        base_url = 'https://www.zhihu.com/api/v4/topics/{topic_id}/feeds/essence?include=data%5B%3F(' \
               'target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(' \
               'target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting' \
               '%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(' \
               'target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info' \
               '%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(' \
               'target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(' \
               'target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B' \
               '%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(' \
               'target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(' \
               'target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed' \
               '%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(' \
               'target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting' \
               '%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(' \
               'type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(' \
               'target.type%3Darticle)%5D.target.content%2Cauthor.badge%5B%3F(' \
               'type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(' \
               'target.type%3Dquestion)%5D.target.comment_count&offset='.format(topic_id=topic_id)
        url = base_url + str(page * 5) + '&limit=5'
        print(url)
        # 设置每页显示5个回答
        response = requests.get(url, headers=header)
        # print(response.text)
        return response.json()
    except Exception:
        print('----------------- 遇到验证码 -------------')
        print('----------------- 遇到验证码 -------------')
        print('----------------- 遇到验证码 -------------')
        print('-- 输入"A"继续执行 --')
        while True:
            if input() == 'A':
                pass
            else:
                print('输入错误，请重新输入')
                continue


"""
    while retry_count > 0:
        try:
            response = requests.get(url, headers=header, proxies={"http": "http://{}".format(proxy)})
            # print(response.text)
            return response.json()
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None
"""


# 解析ajax回答
# with_comments
def parse_answer_page(html, topic_name):
    paging = html['paging']
    is_end = paging['is_end']
    items = html['data']
    try:
        for item in items:
            type = item['target']['type']
            id = item['target']['id']
            voteup_count = item['target']['voteup_count']
            author_name = item['target']['author']['name']
            author_gender = item['target']['author']['gender']
            author_headline = item['target']['author']['headline']
            comment_count = item['target']['comment_count']
            content = item['target']['content']
            if type == 'answer':
                question_title = item['target']['question']['title']
                # content = item['target']['content']
                print('问题:', question_title)
                print('回答者:', author_name, end='||')
                print('性别:', author_gender)
                print('回答者简介:', author_headline)
                # print('回答id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                print('-' * 50)
                print('-- 以下为回答的评论 --')
                # 通过返回的回答的id属性，传递到zhihu_comments.answer_comments()函数中，爬取所有回答
                zhihu_comments.comments(id, topic_name)
                """
                info = '\n'.join(
                    [question_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)
                """
            else:
                article_title = item['target']['title']
                content = item['target']['content']
                print('专栏文章:', article_title)
                print('作者:', author_name, end='||')
                print('性别:', author_gender)
                print('作者简介:', author_headline)
                # print('文章id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                print('-' * 50)
                print('-- 以下为回答的评论 --')
                zhihu_comments.comments(id, topic_name)
                # 通过返回的回答的id属性，传递到zhihu_comments.answer_comments()函数中，爬取所有回答
                """
                info = '\n'.join(
                    [article_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)
                """
            print('=' * 60)
            time.sleep(0.5)
    except Exception:
        print('parse_answer_page() failed...')
        pass
    return is_end


# without_comments
def parse_answer_page_without(html, topic_name):
    paging = html['paging']
    is_end = paging['is_end']
    items = html['data']
    try:
        for item in items:
            type = item['target']['type']
            voteup_count = item['target']['voteup_count']
            author_name = item['target']['author']['name']
            author_gender = item['target']['author']['gender']
            author_headline = item['target']['author']['headline']
            comment_count = item['target']['comment_count']
            content = item['target']['content']
            if type == 'answer':
                question_title = item['target']['question']['title']
                # content = item['target']['content']
                print('问题:', question_title)
                print('回答者:', author_name, end='||')
                print('性别:', author_gender)
                print('回答者简介:', author_headline)
                # print('回答id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                """
                info = '\n'.join(
                    [question_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)
                """
            else:
                article_title = item['target']['title']
                content = item['target']['content']
                print('专栏文章:', article_title)
                print('作者:', author_name, end='||')
                print('性别:', author_gender)
                print('作者简介:', author_headline)
                # print('文章id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                """
                info = '\n'.join(
                    [article_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)
                """
            print('=' * 60)
            time.sleep(1)
    except Exception:
        print('parse_answer_page_without() failed...')
        pass
    return is_end


#  without_comments
def parse_answer_page_without_test(html, topic_name):
    items = html['data']
    try:
        for item in items:
            type = item['target']['type']
            voteup_count = item['target']['voteup_count']
            author_name = item['target']['author']['name']
            author_gender = item['target']['author']['gender']
            author_headline = item['target']['author']['headline']
            comment_count = item['target']['comment_count']
            content = item['target']['content']
            if type == 'answer':
                question_title = item['target']['question']['title']
                # content = item['target']['content']
                print('问题:', question_title)
                print('回答者:', author_name, end='||')
                print('性别:', author_gender)
                print('回答者简介:', author_headline)
                # print('回答id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                info = '\n'.join(
                    [question_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)
            else:
                article_title = item['target']['title']
                voteup_count = item['target']['voteup_count']
                content = item['target']['content']
                print('专栏文章:', article_title)
                print('作者:', author_name, end='||')
                print('性别:', author_gender)
                print('作者简介:', author_headline)
                # print('文章id:', id)
                print('评论数:', comment_count)
                print('赞同数:', voteup_count)
                print(content)
                print('-' * 50)
                info = '\n'.join(
                    [article_title, author_name, str(author_gender), author_headline, str(comment_count), content])
                save_to_txt(info, topic_name)

            print('=' * 60)
            time.sleep(2)
    except Exception:
        print('parse_answer_page_without_test() failed...')
        pass


##########################################################
def answer_with_comments(keyword, topic_name):
    i = 0
    while True:
        i = i + 1
        data = get_answer(i - 1, keyword)
        end = parse_answer_page(data, topic_name)
        # 每爬取一次休眠2秒
        time.sleep(2)

        if end is True:
            break


def answer_without_comments(keyword, topic_name):
    i = 0
    while True:
        i = i + 1
        data = get_answer(i - 1, keyword)
        end = parse_answer_page_without(data, topic_name)
        # 每爬取一次休眠2秒
        time.sleep(2)

        if end is True:
            break


# ###############  TEST  #################### #
def answer_with_comments_test(keyword, topic_name):
        data = get_answer(0, keyword)
        parse_answer_page(data, topic_name)
        # 每爬取一次休眠2秒
        time.sleep(2)


def answer_without_comments_test(keyword, topic_name):
        data = get_answer(0, keyword)
        parse_answer_page_without_test(data, topic_name)
        # 每爬取一次休眠2秒

# ###############  TEST  #################### #


# topic_name参数为输出txt的名称传递参数
def save_to_txt(info, topic_name):
    file = open('{topic_name}.txt'.format(topic_name=topic_name), 'a', encoding='utf-8')
    file.write(info)
    file.write('\n' + '=' * 50 + '\n')
    file.close()


#######################################################
def main(cookie):
    # ####从topics模块，获取topics##### #
    keyword = topics.get_topic(cookie)
    # ####从topics模块，获取topics##### #
    # keyword[0]为话题的总数量
    total = keyword[0]
    # keyword[1]为话题的url_token
    url_token = keyword[1]
    # keyword[2]为话题的name
    name = keyword[2]
    print('############# 是否爬取所有评论?(y/n) #############')
    # 判断是否爬取评论
    #############################
    while True:
        judge = input()
        if judge == 'y':
            for i in range(0, total):
                print('- 正在爬取 -')
                print('--', name[i], '--')
                print('- 的精选回答和评论... -')
                time.sleep(1)
                print('=' * 100)
                print('=' * 100)
                # keyword[0]为话题的url_token属性,keyword[1]为话题name属性，为输出txt传递参数
                answer_with_comments(url_token[i], name[i])
                # 通过返回的回答的id属性，传递到zhihu_comments.answer_comments()函数中，爬取所有回答
                # zhihu_comments.answer_comments(id)
        elif judge == 'n':
            for i in range(0, total):
                print('- 正在爬取 -')
                print('--', name[i], '--')
                print('- 的精选回答... -')
                time.sleep(2)
                print('=' * 100)
                print('=' * 100)
                answer_without_comments(url_token[i], name[i])
        else:
            print('- 输入错误，请重新输入 -')
            continue
    #############################


def test(cookie):
    # ####从topics模块，获取topics##### #
    keyword = topics.get_topic_test(cookie)
    # ####从topics模块，获取topics##### #
    # keyword[0]为话题的总数量
    total = keyword[0]
    # keyword[1]为话题的url_token
    url_token = keyword[1]
    # keyword[2]为话题的name
    name = keyword[2]
    print('############# 是否爬取评论?(y/n) #############')

    # 判断是否爬取评论
    #############################
    while True:
        judge = input()
        if judge == 'y':
            for i in range(0, total):
                print('- 正在爬取 -')
                print('--', name[i], '--')
                print('- 的精选回答和评论... -')
                time.sleep(1)
                print('=' * 100)
                print('=' * 100)
                # keyword[0]为话题的url_token属性,keyword[1]为话题name属性，为输出txt传递参数
                answer_with_comments_test(url_token[i], name[i])
                # 通过返回的回答的id属性，传递到zhihu_comments.answer_comments()函数中，爬取所有回答
                # zhihu_comments.answer_comments(id)
        elif judge == 'n':
            for i in range(0, total):
                print('- 正在爬取 -')
                print('--', name[i], '--')
                print('- 的精选回答... -')
                time.sleep(1)
                print('=' * 100)
                print('=' * 100)
                answer_without_comments_test(url_token[i], name[i])
        else:
            print('- 输入错误，请重新输入 -')
            continue
    #############################
#######################################################
