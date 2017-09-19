# -*- coding: cp950 -*-
# comment
import telnetlib
import codecs
import sys
import time

tn = telnetlib.Telnet('ptt.cc');
time.sleep(3);
content = tn.read_very_eager().decode('cp950','ignore');

print(content);