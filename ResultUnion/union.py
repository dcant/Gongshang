#!/usr/bin/python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    fileone = open("filter1.txt", "r")
    filetwo = open("filter2.txt", "r")
    fileout = open("union.txt", "w")

    dict = []

    for line in fileone:
        cont = line.strip("\n")
        parts = cont.split("\t")
        dict.append(parts[0] + "\t" + parts[1])

    for line in filetwo:
        cont = line.strip("\n")
        if cont in dict:
            pass
        else:
            fileout.write(line)

    for item in dict:
        fileout.write(item+"\n")
    fileone.close()
    filetwo.close()
    fileout.close()