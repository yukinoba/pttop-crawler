# -*- coding: utf-8 -*-
# comment
import telnetlib
import uao_decode
import sys
import datetime
import time

tn = telnetlib.Telnet('ptt.cc');
time.sleep(3);
content = tn.read_very_eager().decode('uao_decode');

# print(content);

if "請輸入代號" in content:
    print(">>> 輸入帳號\r\n");
    tn.write("SeptemberCat".encode('cp950') + b"\r\n");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    if "請輸入您的密碼" in content:
        print(">>> 輸入密碼\r\n");
        tn.write("meow".encode('cp950') + b"\r\n");
        time.sleep(3);
        content = tn.read_very_eager().decode('uao_decode');
        
        if "您想刪除其他重複登入的連線嗎" in content:
            print(">>> 刪除重複登入\r\n");
            tn.write("Y".encode('cp950') + b"\r\n");
            time.sleep(3);
            content = tn.read_very_eager().decode('uao_decode');
        
        if "請按任意鍵繼續" in content:
            print(">>> 登入成功\r\n");
            tn.write(" ".encode('cp950') + b"\r\n");
            time.sleep(3);
            content = tn.read_very_eager().decode('uao_decode');

print(content);