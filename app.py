# -*- coding: cp950 -*-
# comment
import telnetlib
import uao_decode.py
import sys
import time

tn = telnetlib.Telnet('ptt.cc');
time.sleep(3);
content = tn.read_very_eager().decode('uao_decode');

print(content);