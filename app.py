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

# Login process

if "請輸入代號" in content:
    print(">>> 輸入帳號");
    tn.write("SeptemberCat".encode('cp950') + b"\r");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    if "請輸入您的密碼" in content:
        print(">>> 輸入密碼");
        tn.write("meow".encode('cp950') + b"\r");
        time.sleep(3);
        content = tn.read_very_eager().decode('uao_decode');
        
        if "您想刪除其他重複登入的連線嗎" in content:
            print(">>> 刪除重複登入");
            tn.write("Y".encode('cp950') + b"\r");
            time.sleep(3);
            content = tn.read_very_eager().decode('uao_decode');
        
        if "請按任意鍵繼續" in content:
            print(">>> 登入成功");
            tn.write(" ".encode('cp950'));
            time.sleep(3);
            content = tn.read_very_eager().decode('uao_decode');

# Enter specific board and get article list

if "主功能表" in content:
    print(">>> 主功能表");
    tn.write("s".encode('cp950'));
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    if "選擇看板" in content:
        print(">>> 選擇看板");
        tn.write("one_piece".encode('cp950') + b"\r");
        time.sleep(3);
        content = tn.read_very_eager().decode('uao_decode');
        
        if "動畫播放中" in content:
            print(">>> 進板畫面");
            tn.write(" ".encode('cp950'));
            time.sleep(3);
            content = tn.read_very_eager().decode('uao_decode');

# Check violation and prosecute

# Logout process

while not "主功能表" in content:
    print(">>> 回上一層");
    tn.write(b"\x1b[D");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');

if "主功能表" in content:
    print(">>> 登出");
    tn.write(b"\x1b[D");
    time.sleep(3);
    tn.write(b"\x1b[C");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    if "您確定要離開" in content:
        print(">>> 確認登出");
        tn.write("Y".encode('cp950') + b"\r");
        time.sleep(3);
        content = tn.read_very_eager().decode('uao_decode');

print(content);