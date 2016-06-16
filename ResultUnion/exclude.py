#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

if __name__ == '__main__':
    fileone = open("filter2.txt", "r")
    filetwo = open("filter1.txt", "r")
    fileout = open("exclude.txt", "w")

    dict = set()
    kv = {}

    for line in fileone:
        cont = line.strip("\n")
        parts = cont.split("\t")
        dict.add(parts[0])
        kv[parts[0]] = parts[1]

    for line in filetwo:
        cont = line.strip("\n")
        parts = cont.split("\t")
        pattern = re.compile("^www.")
        items = re.findall(pattern, parts[0])
        if len(items) > 0:
            if parts[0] in dict:
                continue
            url = parts[0].strip("www.")
            if url in dict:
                dict.remove(url)
                kv[parts[0]] = kv[url]
                kv.pop(url)
                dict.add(parts[0])
                continue
            fileout.write(parts[0] + "\t" + parts[1] + "\n")
        else:
            if parts[0] in dict:
                continue
            url = "www." + parts[0]
            if url in dict:
                continue
            fileout.write(parts[0] + "\t" + parts[1] + "\n")
    fileone.close()
    filetwo.close()
    fileout.close()