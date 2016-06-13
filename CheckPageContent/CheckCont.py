#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import Queue
import threading

THREAD_NUM = 200

class Checker:
    def __init__(self, dict):
        #self.__dict = ["城市", "外卖", "美食", "测试"]
        self.__dict = dict
        self.__isDictLoaded = True
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        self.header = {'User-Agent': self.user_agent}

    def __loadDict(self):
        file = open(self.__dictfile, "r")
        if not file:
            print "Failed to open dict file"
            return False
        filecont = file.readlines()
        file.close()
        for line in filecont:
            line = line.decode("utf-8").encode("utf-8")
            keys = line.split("\t")
            for key in keys:
                self.__dict.append(key)
        self.__isDictLoaded = True
        return True

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

    def check(self, url, type):
        if not self.__isDictLoaded:
            if not self.__loadDict():
                return None
        url = self.__geturl(url)
        request = urllib2.Request(url, headers=self.header)
        response = urllib2.urlopen(request)
        cont = ""
        try:
            cont = response.read().decode('gbk').encode('utf-8')
        except Exception, e:
            try:
                cont = response.read().decode('utf-8').encode('utf-8')
            except Exception, e:
                return False
        for key in self.__dict[type]:
            pattern = re.compile(key)
            items = re.findall(pattern, cont)
            if len(items) > 0:
                return key
        return None


class MultiAna(threading.Thread):
    def __init__(self, input, num, dict):
        threading.Thread.__init__(self)
        self.input = input
        self.num = str(num)
        self.__succ_file = open("tmp_" + self.num + ".succ", "w")
        self.__fail_file = open("tmp_" + self.num + ".fail", "w")
        self.__error_file = open("tmp" + self.num + ".err", "w")
        self.__checker = Checker(dict)


    def run(self):
        while True:
            try:
                item = self.input.get()
                parts = item.split("\t")
                res = self.__checker.check(parts[0], float(parts[2]))
                if res:
                    self.__succ_file.write(item)
                    self.__succ_file.write("\t")
                    self.__succ_file.write(res)
                    self.__succ_file.write("\n")
                else:
                    self.__fail_file.write(item)
                    self.__fail_file.write("\n")
                self.input.task_done()
            except Exception as e:
                self.__error_file.write(parts[0] + "\t" + str(e) + "\n")
                self.input.task_done()


if __name__ == '__main__':
    dict = {}
    indata = Queue.Queue(0)
    file = open("../data/site_data_out.txt", "r")
    for line in file:
    #for line in sys.stdin:
        line = line.strip("\n")
        indata.put(line)
    file = open("pdict.txt", "r")
    if not file:
        print "Failed to open dict file"
        exit()
    filecont = file.readlines()
    file.close()
    pdict = []
    for line in filecont:
        line = line.decode("utf-8").encode("utf-8")
        keys = line.split("\t")
        for key in keys:
            pdict.append(key)
    dict[1] = pdict

    file = open("tdict.txt", "r")
    if not file:
        print "Failed to open dict file"
        exit()
    filecont = file.readlines()
    file.close()
    tdict = []
    for line in filecont:
        line = line.decode("utf-8").encode("utf-8")
        keys = line.split("\t")
        for key in keys:
            tdict.append(key)
    dict[10] = tdict
    for i in range(THREAD_NUM):
        getter = MultiAna(indata, i, dict)
        getter.setDaemon(True)
        getter.start()
    indata.join()