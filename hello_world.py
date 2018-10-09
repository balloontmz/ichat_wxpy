#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
a test module
"""

__author__ = 'tomtiddler'

import itchat


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg['Text']


itchat.auto_login(True)
itchat.run()
