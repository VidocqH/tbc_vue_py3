# -*- coding:UTF-8 -*-
TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.8.1/index.js'
INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'

def response(flow):
    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = INJECT_TEXT + flow.response.text
        print('注入成功')

    if 'um.js' in flow.request.url or '115.js' in flow.request.url:
    # 屏蔽selenium检测
        flow.response.text = flow.response.text + INJECT_TEXT
