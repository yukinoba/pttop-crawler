# -*- coding: utf-8 -*-
# comment
# import scrapy
# from bs4 import BeautifulSoup

# class PTTOPCrawler(scrapy.Spider):
    # name = 'pttop';
    # allowed_domains = ['ptt.cc'];
    # start_urls = ('https://www.ptt.cc/bbs/ONE_PIECE/index.html', );
    
    # def parse(self, response):
        # res = BeautifulSoup(response.body);
        # for title in res.select('div.title'):
            # print(title.select('a')[0].text);

import sys
import time
import http.client
from bs4 import BeautifulSoup

last_newpush_list = [];
conn = http.client.HTTPSConnection("www.ptt.cc");

while True:
    conn.request("GET", "/bbs/ONE_PIECE/index.html");
    response_list = conn.getresponse();
    content_list = response_list.read().decode(response_list.headers.get_content_charset('utf-8'));

    soup_list = BeautifulSoup(content_list, 'html.parser');
    for title in soup_list.select('div.title'):
        print(">>> 讀取標題：" + title.select('a')[0].text);
        if "檢舉區" in title.select('a')[0].text:
            print(">>> 檢舉區連結：" + title.select('a')[0]['href']);
            prosec_href = title.select('a')[0]['href'];
            
            conn.request("GET", prosec_href);
            response_prosec = conn.getresponse();
            content_prosec = response_prosec.read().decode(response_prosec.headers.get_content_charset('utf-8'));
            
            soup_prosec = BeautifulSoup(content_prosec, 'html.parser');
            for lastpush in soup_prosec.select('div.push'):
                pass
            print(">>> 最後推文：" + lastpush.text);
            
            newcoming = False;
            soup_prosec = BeautifulSoup(content_prosec, 'html.parser');
            for lastedit in soup_prosec.select('span.f2'):
                if "編輯" in lastedit.text:
                    for newpush in lastedit.find_next_siblings('div', 'push'):
                        if newpush.text in last_newpush_list:
                            print(">>> 尚未處理：" + newpush.text);
                        else:
                            print(">>> 有新推文：" + newpush.text);
                            if not newcoming:
                                del last_newpush_list[:];
                                newcoming = True;
                            last_newpush_list.append(newpush.text);
                        
    time.sleep(60 * 1);

# import telnetlib
# import uao_decode
# import sys
# import datetime
# import time
# import re

# tn = telnetlib.Telnet('ptt.cc');
# time.sleep(3);
# content = tn.read_very_eager().decode('uao_decode');

# # print(content);

# # Login process

# if "請輸入代號" in content:
    # print(">>> 輸入帳號");
    # tn.write("SeptemberCat".encode('cp950') + b"\r");
    # time.sleep(3);
    # content = tn.read_very_eager().decode('uao_decode');
    
    # if "請輸入您的密碼" in content:
        # print(">>> 輸入密碼");
        # tn.write("meow".encode('cp950') + b"\r");
        # time.sleep(3);
        # content = tn.read_very_eager().decode('uao_decode');
        
        # if "您想刪除其他重複登入的連線嗎" in content:
            # print(">>> 刪除重複登入");
            # tn.write("Y".encode('cp950') + b"\r");
            # time.sleep(3);
            # content = tn.read_very_eager().decode('uao_decode');
        
        # if "請按任意鍵繼續" in content:
            # print(">>> 登入成功");
            # tn.write(" ".encode('cp950'));
            # time.sleep(3);
            # content = tn.read_very_eager().decode('uao_decode');

# # Enter specific board and get article list

# if "主功能表" in content:
    # print(">>> 主功能表");
    # tn.write("s".encode('cp950'));
    # time.sleep(3);
    # content = tn.read_very_eager().decode('uao_decode');
    
    # if "選擇看板" in content:
        # print(">>> 選擇看板");
        # tn.write("one_piece".encode('cp950') + b"\r");
        # time.sleep(3);
        # content = tn.read_very_eager().decode('uao_decode');
        
        # if "動畫播放中" in content:
            # print(">>> 進板畫面");
            # tn.write(" ".encode('cp950'));
            # time.sleep(3);
            # content = tn.read_very_eager().decode('uao_decode');

# # Check violation and prosecute

# # print(content);

# # bbs_width = 160;
# # content_len = len(content);
# # for index in range(0, content_len, bbs_width):
    # # cap = index + bbs_width - 1;
    # # if index + bbs_width > content_len:
        # # cap = content_len - 1;
    # # print(">>> 讀取列表");
    # # print(content[index:cap]);

# # for line in content.splitlines():
    # # print(">>> 讀取列表");
    # # print(line);

# # pattern = re.compile("★[ ]+\~.*frojet       □ \[公告\] 板規《海賊教戰守則》");
# # pattern = re.compile("★");
# pattern = re.compile("[\x1b]");
# matches = pattern.finditer(content);
# count = 0;
# for mo in matches:
    # index = mo.start() + 1;
    # cap = index + 10;
    # if cap > len(content):
        # cap = len(content) - 1;
    # print(">>> 發現控制碼");
    # print(content[index:cap]);
    # count = count + 1;
# print(">>> 控制碼數量：" + str(count));
# # match = pattern.search(content);
# # if match:
    # # print(">>> 有沒看過的檢舉資訊");
# # else:
    # # print(">>> 沒有新的檢舉資訊了");

# # Logout process

# while not "主功能表" in content:
    # print(">>> 回上一層");
    # tn.write(b"\x1b[D");
    # time.sleep(3);
    # content = tn.read_very_eager().decode('uao_decode');

# if "主功能表" in content:
    # print(">>> 登出");
    # tn.write(b"\x1b[D");
    # time.sleep(3);
    # tn.write(b"\x1b[C");
    # time.sleep(3);
    # content = tn.read_very_eager().decode('uao_decode');
    
    # if "您確定要離開" in content:
        # print(">>> 確認登出");
        # tn.write("Y".encode('cp950') + b"\r");
        # time.sleep(3);
        # content = tn.read_very_eager().decode('uao_decode');

# print(content);