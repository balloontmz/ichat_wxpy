#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
a test module
"""

__author__ = 'tomtiddler'

import json
import itchat
import requests


def get_response(msg):
    api_url = 'http://openapi.tuling123.com/openapi/api/v2'  # 改成你自己的图灵机器人的api，上图红框中的内容，不过用我的也无所谓，只是每天自动回复的消息条数有限
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": "ec64111fe57245eeadefe6c33bf785fd",  # Tuling Key
            "userId": "wechatrobot0000",  # 这里你想改什么都可以
        }
    }
    data = json.dumps(data)
    # 我们通过如下命令发送一个post请求
    r = requests.post(api_url, data=data).json()
    r = r['results'][0]['values']['text']
    return r


@itchat.msg_register(itchat.content.TEXT)
def print_contents(msg):
    # itchat.send(get_response(msg['Text']), toUserName=msg['FromUserName'])
    re_data = get_response(msg['Text'])
    return re_data


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def print_content(msg):
    return get_response(msg['Text'])


itchat.auto_login(True)
itchat.run()
