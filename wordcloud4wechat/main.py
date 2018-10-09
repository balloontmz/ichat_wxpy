#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
代码搬运，运行成功，没有细致查看。
"""

__author__ = 'tomtiddler'

import re

import itchat
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


def my_friends():
    # 二维码登录
    itchat.auto_login(True)
    # 获取好友信息
    friends = itchat.get_friends(update=True)
    # with open('friends.txt', 'w') as fri_list:
    #     fri_list.write(friends)
    return friends


def my_friends_sex(friends):
    # 创建一个字典用于存放好友性别信息
    friends_sex = dict()
    # 定义好友性别信息字典的key，分别为男性，女性，其他
    male = "male"
    female = "female"
    other = "other"

    # 遍历列表中每一个好友的信息
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            friends_sex[male] = friends_sex.get(male, 0) + 1
        elif sex == 2:
            friends_sex[female] = friends_sex.get(female, 0) + 1
        elif sex == 0:
            friends_sex[other] = friends_sex.get(other, 0) + 1

    total = len(friends[1:])
    proportion = [float(friends_sex[male]) / total * 100,
                  float(friends_sex[female]) / total * 100,
                  float(friends_sex[other]) / total * 100]

    print(
        "男性好友：%.2f%% " % (proportion[0]) + '\n' +
        "女性好友：%.2f%% " % (proportion[1]) + '\n' +
        "其他：%.2f%% " % (proportion[2])
    )
    return friends_sex


def my_friends_style(friends):
    # 创建列表用于存放个性签名
    style = []
    for i in range(len(friends)):
        # 每一个好友的信息存放在列表中的字典里，此处获取到
        i = friends[i]
        # 得到每个字典的个性签名的key，即Signature
        # strip去除字符串首位的空格，replace去掉英文
        Signature = i['Signature'].strip().replace('span', '').replace('class', '').replace('emoji', '')
        # 通过正则表达式将签名中的特殊符号去掉，re.sub则相当于字符串操作中的replace
        rep = re.compile('1f\d+\w*|[<>/=]')
        Signature = rep.sub('', Signature)
        # 放入列表
        style.append(Signature)
    # join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
    # 此处将所有签名去除特殊符号和英文之后，拼接在一起
    text = ''.join(style)
    # 将输出保存到文件，并用结巴来分词
    with open('text.txt', 'a', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=False)
        word_space_split = ' '.join(wordlist)
        f.write(word_space_split)


def drow_sex(friends_sex):
    # 获取饼状图的标签和大小
    labels = []
    sizes = []
    for key in friends_sex:
        labels.append(key)
        sizes.append(friends_sex[key])
    # 每块图的颜色，数量不足时会循环使用
    colors = ['red', 'yellow', 'blue']
    # 每一块离中心的距离
    explode = (0.1, 0, 0)
    # autopct='%1.2f%%'百分数保留两位小数点；shadow=True,加阴影使图像更立体
    # startangle起始角度，默认为0°，一般设置为90比较好看
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=90)
    # 设置图像的xy轴一致
    plt.axis('equal')
    # 显示颜色和标签对应关系
    plt.legend()
    # 添加title，中文有乱码是个坑，不过我找到填平的办法了
    plt.suptitle("total sex distribute")
    # 保存到本地，因为show之后会创建空白图层，所以必须在show之前保存
    plt.savefig('好友性别饼状图.png')
    plt.show()


def wordart():
    back_color = plt.imread('好友性别饼状图.png')
    wc = WordCloud(background_color='white',  # 背景色
                   max_words=1000,
                   mask=back_color,  # 以该参数值绘制词云
                   max_font_size=100,

                   font_path="0081.ttf",  # 设置字体类型，主要为了解决中文乱码问题
                   random_state=42,  # 为每一词返回一个PIL颜色
                   )

    # 打开词源文件
    text = open("text.txt", encoding='utf-8').read()
    #
    wc.generate(text)
    # 基于彩色图像生成相应颜色
    image_colosr = ImageColorGenerator(back_color)
    # 显示图片
    plt.imshow(wc)
    # 关闭坐标轴
    plt.axis("off")
    # 保存图片
    wc.to_file("词云.png")


if __name__ == "__main__":
    friends_list = my_friends()
    friend_sex = my_friends_sex(friends_list)

    my_friends_style(friends_list)

    drow_sex(friend_sex)

    wordart()
