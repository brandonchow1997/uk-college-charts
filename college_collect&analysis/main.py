import zhihu_topic_answer


# 主函数
if __name__ == '__main__':
    # zja的cookie
    cookie = '"2|1:0|10:1536064098|4:z_c0|92' \
             ':Mi4xMnREX0JBQUFBQUFBVUtjcUNEcnFEU1lBQUFCZ0FsVk5Zc2g3WEFEUHk2bFRMdTVONnBJUUlXaTg3VDAtSFV1RzZn' \
             '|dc005abc5e83e8ac94e51023fc8135e6d22931baa6e6d5aa5f038f97ef86eb49" '
    print('-- 演示版请输入：TEST --')
    print('-- 默认则为完整版 --')
    print('请输入:', end='')
    choose = input()
    if choose == 'TEST':
        zhihu_topic_answer.test(cookie)
    else:
        zhihu_topic_answer.main(cookie)