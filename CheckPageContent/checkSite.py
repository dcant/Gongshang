#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import Queue
import threading


THREAD_NUM = 200


class MultiAna(threading.Thread):
    def __init__(self, input, num):
        threading.Thread.__init__(self)
        self.input = input
        self.num = str(num)
        self.__succ_file = open("tmp_" + self.num + ".succ", "w")
        self.__fail_file = open("tmp_" + self.num + ".fail", "w")

    def __detect_site(self, _site, cont):
        if _site.find("http://") == -1:
            _site = "http://" + _site;

        try_cnt = 0
        while True:
            try:
                spage = urllib.urlopen(_site)
            except Exception, e:
                try_cnt += 1
                if try_cnt >= 3:
                    self.__fail_file.write(cont)
                    self.__fail_file.write("\t")
                    self.__fail_file.write(str(e))
                    self.__fail_file.write("\n")
                    return None
            else:
                break

        if spage.getcode() != 200:
            self.__fail_file.write(cont)
            self.__fail_file.write("\t")
            self.__fail_file.write(str(spage.getcode()))
            self.__fail_file.write("\n")
        else:
            self.__succ_file.write(cont)
            self.__succ_file.write("\t")
            self.__succ_file.write(str(spage.getcode()))
            self.__succ_file.write("\n")

    def run(self):
        while True:
            try:
                item = self.input.get()
                parts = item.split("\t")
                self.__detect_site(parts[0].strip(), item)
                self.input.task_done()
            except Exception as e:
                print e
                print 'ERROR-ERROR'
                self.input.task_done()


def start(file):
    with open(file, 'r') as urllist:
        lines = urllist.readlines()
    if len(lines) < 1:
        print 'no input'
        return
    indata = Queue.Queue(0)
    for line in lines:
        line = line.strip()
        indata.put(line)
    for i in range(THREAD_NUM):
        getter = MultiAna(indata, i)
        getter.setDaemon(True)
        getter.start()
    indata.join()

if __name__ == '__main__':
    indata = Queue.Queue(0)
    file = open("../data/ana_dict_code.txt", "r")
    for line in file:
    #for line in sys.stdin:
        line = line.strip("\n")
        indata.put(line)
    for i in range(THREAD_NUM):
        getter = MultiAna(indata, i)
        getter.setDaemon(True)
        getter.start()
    indata.join()
