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
    tn.write("guest".encode('uao_decode') + b"\r\n");
    time.sleep(3);
    content = tn.read_very_eager().decode('uao_decode');
    
    print(content);