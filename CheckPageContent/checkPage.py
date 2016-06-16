#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Checker:
    def __init__(self, dict):
        self.__dict = dict

    def check(self, cont, type):
        for key in self.__dict[type]:
            pattern = re.compile(key)
            items = re.findall(pattern, cont)
            if len(items) > 0:
                return key
        return None

def main():
    dict = {}

    succ_file = open("succ.txt", "w")
    fail_file = open("fail.txt", "w")

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

    ck = Checker(dict)

    kv = {}
    with open("code1001.txt") as file:
        for line in file:
            cont = line.strip("\n")
            parts = cont.split("\t")
            url = parts[0]
            type = float(parts[2])
            if kv.has_key(url):
                continue
            else:
                if url.find("www.") == 0:
                   if kv.has_key(url[4:]):
                       kv.pop(url[4:])
                kv[url] = type
    file.close()

    with open("page_data") as file:
        url = ""
        title = ""
        lastIsUrl = False
        found = False
        tmpurl = ""
        for line in file:
            line = line.strip("\n")
            if line.find("Url:") == 0:
                lastIsUrl = True
                turl = line[4:]
                if turl.find("http://") == 0:
                    tmpurl = turl[7:]
                elif turl.find("https://") == 0:
                    tmpurl = turl[8:]
                tmpurl = tmpurl.rstrip().rstrip('/')
                continue
            elif line.find("TITL:") == 0:
                if lastIsUrl == True:
                    if found:
                        found = False
                    else:
                        fail_file.write(url)
                        fail_file.write("\t")
                        fail_file.write(title.decode('utf-8').encode('cp936', 'ignore'))
                        fail_file.write("\n")
                    url = tmpurl
                    title = line[5:].decode('gb18030', 'ignore').encode('utf-8')
                    lastIsUrl = False
                else:
                    if found:
                        continue
                    line = line.decode('gb18030', 'ignore').encode('utf-8')
                    if kv.has_key(url):
                        res = ck.check(line, kv[url])
                        if res:
                            found = True
                            succ_file.write(url)
                            succ_file.write("\t")
                            succ_file.write(title.decode('utf-8').encode('cp936', 'ignore'))
                            succ_file.write("\t")
                            succ_file.write(res.decode('utf-8').encode('cp936', 'ignore'))
                            succ_file.write("\n")
            else:
                if found:
                    continue
                else:
                    line = line.decode('gb18030', 'ignore').encode('utf-8')
                    if kv.has_key(url):
                        res = ck.check(line, kv[url])
                        if res:
                            found =True
                            succ_file.write(url)
                            succ_file.write("\t")
                            succ_file.write(title.decode('utf-8').encode('cp936', 'ignore'))
                            succ_file.write("\t")
                            succ_file.write(res.decode('utf-8').encode('cp936', 'ignore'))
                            succ_file.write("\n")
                    else:
                        if url.find("www.") == 0:
                            if kv.has_key(url[4:]):
                                res = ck.check(line, kv[url])
                                if res:
                                    found = True
                                    succ_file.write(url)
                                    succ_file.write("\t")
                                    succ_file.write(title.decode('utf-8').encode('cp936', 'ignore'))
                                    succ_file.write("\t")
                                    succ_file.write(res.decode('utf-8').encode('cp936', 'ignore'))
                                    succ_file.write("\n")
                        else:
                            if kv.has_key("www."+url):
                                url = "www." + url
                                res = ck.check(line, kv[url])
                                if res:
                                    found = True
                                    succ_file.write(url)
                                    succ_file.write("\t")
                                    succ_file.write(title.decode('utf-8').encode('cp936', 'ignore'))
                                    succ_file.write("\t")
                                    succ_file.write(res.decode('utf-8').encode('cp936', 'ignore'))
                                    succ_file.write("\n")

    file.close()
    succ_file.close()
    fail_file.close()

if __name__ == '__main__':
    main()
