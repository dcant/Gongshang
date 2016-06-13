#!/usr/bin/python
# -*- coding: utf-8 -*-

class IcpCheck:
    def __init__(self, orifile):
        self.__orifile = open(orifile, "r")
        self.__lines = self.__orifile.readlines()
        self.__orifile.close()
        self.__dict = {}
        self.__secsub = ["com", "net", "edu", "org", "gov"]
        self.__sub = ["cn"]
        for line in self.__lines:
            items = line.split("\t")
            self.__dict[items[0]] = items[3]


    def __getDomain(self, url):
        if url[-1] == '/':
            url = url[0:-1]
        items = url.split(".")
        itemnum = len(items)
        temp = []
        if itemnum < 2:
            return None
        if items[itemnum - 1] in self.__sub and items[itemnum - 2] in self.__secsub:
            temp = items[itemnum - 3::]
        else:
            temp = items[itemnum - 2::]
        return ".".join(temp)

    def checkIcp(self, url, isDomain = False):
        domain = ""
        if isDomain:
            domain = url
        else:
            domain = self.__getDomain(url)
        print domain
        if not domain:
            print "Get domain error"
            return None
        if domain in self.__dict.keys():
            return True
        return False

if __name__ == '__main__':
    ipc = IcpCheck("out.txt")
    url = "http://www.gzjzx.com/"
    if ipc.checkIcp(url):
        print "True"
    else:
        print "False"