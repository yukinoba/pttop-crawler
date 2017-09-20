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
    tn.write("SeptemberCat".encode('cp950') + b"^m");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    if "請輸入您的密碼" in content:
        tn.write("meow".encode('cp950') + b"^m");
        time.sleep(3);
        content = tn.read_very_eager().decode('uao_decode');

print(content);