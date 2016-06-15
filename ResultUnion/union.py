#!/usr/bin/python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    fileone = open("filter1.txt", "r")
    filetwo = open("filter2.txt", "r")
    fileout = open("union.txt", "w")

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
        if parts[0] in dict:
            pass
        else:
            fileout.write(line)

    for item in dict:
        fileout.write(item+"\t"+kv[item]+"\n")
    fileone.close()
    filetwo.close()
    fileout.close()