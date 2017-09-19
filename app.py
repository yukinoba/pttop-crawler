# -*- coding: cp950 -*-
# comment
import telnetlib
import sys
import time
from . import uao_decode

tn = telnetlib.Telnet('ptt.cc');
time.sleep(3);
content = tn.read_very_eager().decode('uao_decode');

print(content);