# -*- coding: utf-8 -*-
# comment
import telnetlib
import uao_decode
import sys
import datetime
import time
import re
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
        # print(">>> 讀取標題：" + title.select('a')[0].text);
        if "檢舉區" in title.select('a')[0].text:
            # print(">>> 檢舉區連結：" + title.select('a')[0]['href']);
            prosec_href = title.select('a')[0]['href'];
            
            conn.request("GET", prosec_href);
            response_prosec = conn.getresponse();
            content_prosec = response_prosec.read().decode(response_prosec.headers.get_content_charset('utf-8'));
            
            newcoming = False;
            soup_prosec = BeautifulSoup(content_prosec, 'html.parser');
            for lastedit in soup_prosec.select('span.f2'):
                if "編輯" in lastedit.text:
                    for newpush in lastedit.find_next_siblings('div', 'push'):
                        tag = newpush.select('span.push-tag')[0].text.rstrip();
                        userid = newpush.select('span.push-userid')[0].text.rstrip();
                        content = newpush.select('span.push-content')[0].text.rstrip();
                        ipdatetime = newpush.select('span.push-ipdatetime')[0].text.rstrip();
                        
                        pushtext = '{} {}{}    {}'.format(tag, userid, content, ipdatetime);
                        
                        if pushtext in last_newpush_list:
                            print(">>> 尚未處理：" + pushtext);
                        else:
                            if not newcoming:
                                del last_newpush_list[:];
                                newcoming = True;
                            last_newpush_list.append(pushtext);
                    if not newcoming:
                        print(">>> 無新推文");
                        del last_newpush_list[:];
                    else:
                        #for newpushtext in last_newpush_list:
                           # print(">> 有新推文：" + newpushtext);
                        tn = telnetlib.Telnet('ptt.cc');
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Login process
                        if "請輸入代號" in content_term:
                            print(">>> 輸入帳號");
                            tn.write("yukinoba".encode('cp950') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            
                            if "請輸入您的密碼" in content_term:
                                print(">>> 輸入密碼");
                                tn.write("ckmagic007".encode('cp950') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                
                                if "您想刪除其他重複登入的連線嗎" in content_term:
                                    print(">>> 刪除重複登入");
                                    tn.write("n".encode('cp950') + b"\r");
                                    time.sleep(5);
                                    content_term = tn.read_very_eager().decode('uao_decode');
                                
                                if "請按任意鍵繼續" in content_term:
                                    print(">>> 登入成功");
                                    tn.write(" ".encode('cp950'));
                                    time.sleep(3);
                                    content_term = tn.read_very_eager().decode('uao_decode');
                        # Enter mailbox and send notifications
                        if "主功能表" in content_term:
                            print(">>> 主功能表");
                            tn.write("m".encode('cp950'));
                            time.sleep(3);
                            tn.write(b"\x1b[C");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            
                            if "電子郵件" in content_term:
                                print(">>> 進入寄信");
                                tn.write("m".encode('cp950'));
                                time.sleep(3);
                                tn.write(b"\x1b[C");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                
                                if "群組寄信名單" in content_term:
                                    print(">>> 寄信名單");
                                    tn.write("0".encode('cp950') + b"\r");
                                    time.sleep(3);
                                    tn.write("m".encode('cp950') + b"\r");
                                    time.sleep(3);
                                    content_term = tn.read_very_eager().decode('uao_decode');
                                    
                                    if "主題" in content_term:
                                        print(">>> 信件主旨");
                                        tn.write("有新檢舉推文通知".encode('cp950') + b"\r");
                                        time.sleep(3);
                                        content_term = tn.read_very_eager().decode('uao_decode');
                                        
                                        if "通告" in content_term:
                                            print(">>> 檢舉通知");
                                            tn.write(b"\x1b[6~");
                                            time.sleep(3);
                                            for newpushtext in last_newpush_list:
                                                tn.write(newpushtext.encode('cp950') + b"\r");
                                                time.sleep(3);
                                            tn.write(b"\x18");
                                            time.sleep(3);
                                            content_term = tn.read_very_eager().decode('uao_decode');
                                            
                                            if "檔案處理" in content_term:
                                                print(">>> 寄出信件");
                                                tn.write("s".encode('cp950') + b"\r");
                                                time.sleep(3);
                                                content_term = tn.read_very_eager().decode('uao_decode');
                                                
                                                if "簽名檔" in content_term:
                                                    print(">>> 不加簽名");
                                                    tn.write("0".encode('cp950') + b"\r");
                                                    time.sleep(3);
                                                    content_term = tn.read_very_eager().decode('uao_decode');
                                                    
                                                    if "自存底稿" in content_term:
                                                        print(">>> 不存底稿");
                                                        tn.write("n".encode('cp950') + b"\r");
                                                        time.sleep(3);
                                                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Logout process
                        while not "主功能表" in content_term:
                            print(">>> 回上一層");
                            tn.write(b"\x1b[D");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                        if "主功能表" in content_term:
                            print(">>> 登出");
                            tn.write(b"\x1b[D");
                            time.sleep(3);
                            tn.write(b"\x1b[C");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            
                            if "您確定要離開" in content_term:
                                print(">>> 確認登出");
                                tn.write("Y".encode('cp950') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
    time.sleep(60 * 1);