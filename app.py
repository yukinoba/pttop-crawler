# -*- coding: cp950 -*-
# comment
import telnetlib
import uao_decode
import sys
import datetime

tn = telnetlib.Telnet('ptt.cc');
time.sleep(3);
content = tn.read_very_eager().decode('uao_decode');

print(content);