# -*- coding: utf-8 -*-
# Comments
# Libraries
import telnetlib
import uao_decode
import sys
import datetime
import time
import re
import http.client
from bs4 import BeautifulSoup
# Global setup definition
bm_list = ['yukinoba', 'frojet'];
login = {'account': 'yukinoba', 'password': 'ckmagic007'};
# Function definition
# Utility: convert PTT web filename to AIDu
def fn2aidu( type, v1, v2 ):
    aidu = None;
    type_int = 0;
    if type == "G":
        type_int = 1;
    v1_int = 0;
    if not v1 is None:
        v1_int = int(v1, 10);
    v2_int = 0;
    if not v2 is None:
        v2_int = int(v2, 16);
    aidu = ((type_int & 0xf) << 44) | ((v1_int & 0xffffffff) << 12) | (v2_int & 0xfff);
    return aidu;
# Utility: convert PTT AIDu to AIDc
def aidu2aidc( aidu ):
    aidc = None;
    aidc_cell = ['X','X','X','X','X','X','X','X'];
    aidc_map = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-','_'];
    if not aidu is None:
        aidu_tmp = aidu;
        for cell_index in range(7, -1, -1):
            map_index = aidu_tmp % len(aidc_map);
            aidc_cell[cell_index] = aidc_map[map_index];
            aidu_tmp = aidu_tmp // len(aidc_map);
    aidc = ''.join(aidc_cell);
    return aidc;
# Function: Send notification mail to board masters
def prosecute_notify( pushlist ):
    account = "yukinoba";
    password = "ckmagic007";
    tn = telnetlib.Telnet('ptt.cc');
    time.sleep(3);
    content_term = tn.read_very_eager().decode('uao_decode');
    # Login process
    if "請輸入代號" in content_term:
        print(">>> 輸入帳號");
        tn.write(login['account'].encode('cp950') + b"\r");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Enter password
        if "請輸入您的密碼" in content_term:
            print(">>> 輸入密碼");
            tn.write(login['password'].encode('cp950') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Duplicated login record
            if "您想刪除其他重複登入的連線嗎" in content_term:
                print(">>> 刪除重複登入");
                tn.write("n".encode('cp950') + b"\r");
                time.sleep(5);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Dashboard
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
        # Email
        if "電子郵件" in content_term:
            print(">>> 進入寄信");
            tn.write("m".encode('cp950'));
            time.sleep(3);
            tn.write(b"\x1b[C");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Mailing list
            if "群組寄信名單" in content_term:
                print(">>> 寄信名單");
                tn.write("0".encode('cp950') + b"\r");
                time.sleep(3);
                tn.write("m".encode('cp950') + b"\r");
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
                # Topic
                if "主題" in content_term:
                    print(">>> 信件主旨");
                    tn.write("有新檢舉推文通知".encode('cp950') + b"\r");
                    time.sleep(3);
                    content_term = tn.read_very_eager().decode('uao_decode');
                    # Prosecute push
                    if "通告" in content_term:
                        print(">>> 檢舉通知");
                        tn.write(b"\x1b[6~");
                        time.sleep(3);
                        for pushtext in pushlist:
                            tn.write(pushtext.encode('cp950') + b"\r");
                            time.sleep(3);
                        tn.write(b"\x18");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Save and send
                        if "檔案處理" in content_term:
                            print(">>> 寄出信件");
                            tn.write("s".encode('cp950') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Signature
                            if "簽名檔" in content_term:
                                print(">>> 不加簽名");
                                tn.write("0".encode('cp950') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                # Copy
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
        # Confirm logout
        if "您確定要離開" in content_term:
            print(">>> 確認登出");
            tn.write("Y".encode('cp950') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
# Function: Write warning message to those bad evaluation posts
def post_warning( postlist ):
    warning_message = [
        "本板板旨為討論 ONE PIECE作品相關內容，若有無涉作品之",
        "討論還請多加留意板規相關規範，並請尊重各方板友之意見",
        "請勿作情緒性人身攻擊之發言內容；如有需要修正推文內容",
        "請自行洽原發文者聯繫請求協助。",
        "以上根據本板板規C-2、I(3)給予提醒"
    ];
    tn = telnetlib.Telnet('ptt.cc');
    time.sleep(3);
    content_term = tn.read_very_eager().decode('uao_decode');
    # Login process
    if "請輸入代號" in content_term:
        print(">>> 輸入帳號");
        tn.write(login['account'].encode('cp950') + b"\r");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Enter password
        if "請輸入您的密碼" in content_term:
            print(">>> 輸入密碼");
            tn.write(login['password'].encode('cp950') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Duplicated login record
            if "您想刪除其他重複登入的連線嗎" in content_term:
                print(">>> 刪除重複登入");
                tn.write("n".encode('cp950') + b"\r");
                time.sleep(5);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Dashboard
            if "請按任意鍵繼續" in content_term:
                print(">>> 登入成功");
                tn.write(" ".encode('cp950'));
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
    # Enter specific board
    if "主功能表" in content_term:
        print(">>> 主功能表");
        tn.write("s".encode('cp950'));
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Choose board
        if "選擇看板" in content_term:
            print(">>> 選擇看板");
            tn.write("ONE_PIECE".encode('cp950') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Board entry
            if "動畫播放中" in content_term:
                print(">>> 進板畫面");
                tn.write("q".encode('cp950'));
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Post list
            if "文章選讀" in content_term:
                print(">>> 文章列表");
                # Go to the post
                for postlink in postlist:
                    # Convert web BBS postlink filename to telnet BBS post AIDc
                    aidc = None;
                    pattern = re.compile('\/([MG]{1})\.([0-9]+)\.A\.([0-9A-F]+)\.html');
                    mo = re.search(pattern, postlink);
                    if mo:
                        type = mo.group(1);
                        v1 = mo.group(2);
                        v2 = mo.group(3);
                        aidc = aidu2aidc(fn2aidu(type, v1, v2));
                    if aidc is None:
                        continue;
                    else:
                        tn.write("#".encode('cp950'));
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Jump to post by AID
                        if "文章代碼" in content_term:
                            tn.write(aidc.encode('cp950') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Post not exists
                            if "請按任意鍵繼續" in content_term:
                                tn.write(" ".encode('cp950'));
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                # Back to post list
                                continue;
                            # Push warning message under the post
                            if "文章選讀" in content_term:
                                for warnmsg in warning_message:
                                    tn.write("X".encode('cp950'));
                                    time.sleep(3);
                                    content_term = tn.read_very_eager().decode('uao_decode');
                                    # Possible push procedures
                                    # Push is prohibited
                                    if "禁止推薦" in content_term:
                                        tn.write(" ".encode('cp950'));
                                        time.sleep(3);
                                        content_term = tn.read_very_eager().decode('uao_decode');
                                        break;
                                    # Login account as same as author
                                    if "作者本人" in content_term:
                                        tn.write(b"\r");
                                        time.sleep(3);
                                        content_term = tn.read_very_eager().decode('uao_decode');
                                        break;
                                    # Normal push procedure
                                    if "您覺得這篇文章" in content_term:
                                        tn.write("3".encode('cp950'));
                                        time.sleep(3);
                                        content_term = tn.read_very_eager().decode('uao_decode');
                                        # Push content input field
                                        if (login['account'] + ":") in content_term:
                                            tn.write(warnmsg.encode('cp950') + b"\r");
                                            time.sleep(3);
                                            tn.write("y".encode('cp950') + b"\r");
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
        # Confirm logout
        if "您確定要離開" in content_term:
            print(">>> 確認登出");
            tn.write("Y".encode('cp950') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
# Main procedure
last_newpush_list = [];
warning_post_list = [];
conn = http.client.HTTPSConnection("www.ptt.cc");
# Work until shutdown
while True:
    conn.request("GET", "/bbs/ONE_PIECE/index.html");
    response_list = conn.getresponse();
    content_list = response_list.read().decode(response_list.headers.get_content_charset('utf-8'));
    # Check prosecute push
    soup_list = BeautifulSoup(content_list, 'html.parser');
    for title in soup_list.select('div.title'):
        # print(">>> 讀取標題：" + title.text);
        if "檢舉區" in title.text:
            # print(">>> 檢舉區連結：" + title.select('a')[0]['href']);
            prosec_href = title.select('a')[0]['href'];
            # Enter prosecute area
            conn.request("GET", prosec_href);
            response_prosec = conn.getresponse();
            content_prosec = response_prosec.read().decode(response_prosec.headers.get_content_charset('utf-8'));
            # Check the latest push
            newcoming = False;
            soup_prosec = BeautifulSoup(content_prosec, 'html.parser');
            for lastedit in soup_prosec.select('span.f2'):
                if "編輯" in lastedit.text:
                    for newpush in lastedit.find_next_siblings('div', 'push'):
                        tag = newpush.select('span.push-tag')[0].text.rstrip();
                        userid = newpush.select('span.push-userid')[0].text.rstrip();
                        content = newpush.select('span.push-content')[0].text.rstrip();
                        ipdatetime = newpush.select('span.push-ipdatetime')[0].text.rstrip();
                        # Format push text
                        pushtext = '{} {}{}    {}'.format(tag, userid, content, ipdatetime);
                        # Is there a new push?
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
                        for newpushtext in last_newpush_list:
                           print(">> 有新推文：" + newpushtext);
                        prosecute_notify(last_newpush_list);
    # Clear post list first
    del warning_post_list[:];
    # Check bad evaluation
    soup_list = BeautifulSoup(content_list, 'html.parser');
    for postentry in soup_list.select('div.r-ent'):
        # print(">>> 讀取評價：" + postentry.select('div.nrec')[0].text);
        # Skip annoucement posts
        if "[公告]" in postentry.select('div.title')[0].text:
            continue;
        if "X" in postentry.select('div.nrec')[0].text:
            for postlink in postentry.select('div.title>a'):
                # print(">>> 文章連結：" + postlink['href']);
                post_href = postlink['href'];
                # Enter warning post
                conn.request("GET", post_href);
                response_post = conn.getresponse();
                content_post = response_post.read().decode(response_post.headers.get_content_charset('utf-8'));
                # Check warning exists
                has_warned = False;
                soup_postpush = BeautifulSoup(content_post, 'html.parser');
                for userid in soup_postpush.select('div.push>span.push-userid'):
                    if userid.text.strip() in bm_list:
                        has_warned = True;
                # Has no warning, add to the warning list
                if not has_warned:
                    warning_post_list.append(post_href);
        else:
            # Check push before bad evaluation occurs
            if not postentry.select('div.nrec')[0].text:
                for postlink in postentry.select('div.title>a'):
                    # print(">>> 文章連結：" + postlink['href']);
                    post_href = postlink['href'];
                    # Enter warning post
                    conn.request("GET", post_href);
                    response_post = conn.getresponse();
                    content_post = response_post.read().decode(response_post.headers.get_content_charset('utf-8'));
                    # Count bad evalutions
                    bad_count = 0;
                    soup_postpush = BeautifulSoup(content_post, 'html.parser');
                    for pushtag in soup_postpush.select('div.push>span.push-tag'):
                        if "噓" in pushtag.text:
                            bad_count = bad_count + 1;
                    if bad_count > 10:
                        # Check warning exists
                        has_warned = False;
                        soup_postpush = BeautifulSoup(content_post, 'html.parser');
                        for userid in soup_postpush.select('div.push>span.push-userid'):
                            if userid.text.strip() in bm_list:
                                has_warned = True;
                        # Has no warning, add to the warning list
                        if not has_warned:
                            warning_post_list.append(post_href);
    if len(warning_post_list) > 0:
        for post_href in warning_post_list:
            print(">>> 需要警告：" + "https://www.ptt.cc/" + post_href);
        post_warning(warning_post_list);
    else:
        print(">>> 不需警告");
    # Rest a moment
    time.sleep(60 * 1);