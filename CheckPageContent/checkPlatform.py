#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import os
import Queue
import threading
import time

THREAD_NUM = 100

class RedirctHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        #print "Oops! 301"
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        #print "Oops! 302"
        pass

class Checker:
    def __init__(self, dict):
        self.__dict = dict
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        self.header = {'User-Agent': self.user_agent}
        self.opener = urllib2.build_opener(urllib2.HTTPHandler(), RedirctHandler)

    def __geturl(self, url):
        pattern = re.compile("^http://")
        items = re.findall(pattern, url)
        if len(items) > 0:
            return url
        else:
            pattern = re.compile("^https://")
            items = re.findall(pattern, url)
            if len(items) > 0:
                return url
            return "http://" + url

    def check(self, url):
        url = self.__geturl(url)
        urllib2.install_opener(self.opener)
        request = urllib2.Request(url, headers=self.header)
        retry = 0
        cont = ""
        while True:
            if retry < 2:
                try:
                    response = urllib2.urlopen(request, timeout=5)
                    cont = response.read().decode('gbk', 'ignore').encode('utf-8')
                    break
                except Exception, e:
                    retry += 1
            else:
                return -1

        if cont == "":
            return 0
        for key in self.__dict:
            pattern = re.compile(key)
            items = re.findall(pattern, cont)
            if len(items) > 0:
                return key
        return 0


class MultiAna(threading.Thread):
    def __init__(self, input, num, dict):
        threading.Thread.__init__(self)
        self.input = input
        self.num = str(num)
        self.__succ_file = open("tmp/tmp_" + self.num + ".succ", "w")
        self.__fail_file = open("tmp/tmp_" + self.num + ".fail", "w")
        self.__error_file = open("tmp/tmp_" + self.num + ".err", "w")
        self.__checker = Checker(dict)

    def run(self):
        while True:
            try:
                item = self.input.get(False)
                parts = item.split("\t")
                res = self.__checker.check(parts[0])
                if res == -1:
                    self.__error_file.write(parts[0] + "\n")
                elif res == 0:
                    self.__fail_file.write(item)
                    self.__fail_file.write("\n")
                else:
                    self.__succ_file.write(item)
                    self.__succ_file.write("\t")
                    self.__succ_file.write(res.decode('utf-8').encode('cp936'))
                    self.__succ_file.write("\n")
                self.input.task_done()
            except Exception as e:
                break
        self.__succ_file.close()
        self.__fail_file.close()
        self.__error_file.close()


if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    dict = []
    indata = Queue.Queue(0)
    file = open("site.txt", "r")
    for line in file:
    #for line in sys.stdin:
        line = line.strip("\n")
        indata.put(line)
    file = open("dict.txt", "r")
    if not file:
        print "Failed to open dict file"
        exit()
    filecont = file.readlines()
    file.close()

    for line in filecont:
        line = line.decode("utf-8").encode("utf-8")
        keys = line.split("\t")
        for key in keys:
            dict.append(key)

    for i in range(THREAD_NUM):
        runner = MultiAna(indata, i, dict)
        runner.setDaemon(True)
        runner.start()
    indata.join()
    print time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    time.sleep(1)

    cmd = "cat tmp/tmp_*.succ > tmp/onlinetrade.txt; cat tmp/tmp_*.fail > tmp/normal.txt; cat tmp/tmp_*.err > tmp/diesite.txt; cat tmp/tmp_* > tmp/all.txt; rm -f tmp/tmp_*;"
    os.system(cmd)