#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Filter:
    def __init__(self, infile, outfile):
        self.__infile = infile
        self.__outfile = outfile

    def do_filter(self):
        self.__infilefp = open(self.__infile, "r")
        if not self.__infilefp:
            print "Failed to open input file"
            return
        self.__outfilefp = open(self.__outfile, "w")
        if not self.__outfilefp:
            print "Failed to open output file"
            return
        for line in self.__infilefp:
            line = line.decode("cp936").encode("utf8")
            items = line.split("\t")
            if not items[3]:
                continue
            #print items[3]
            temp = items[3]
            #xx = ur'^[\u4eac]'
            xx = "(^京)"
            pattern = re.compile(xx)
            results = pattern.findall(temp)
            if not results:
                continue
            self.__outfilefp.write("%s\t%s\t%s\t%s\t%s\t%s\t%s" %
                                   (items[0], items[1], items[2], temp, items[4], items[5], items[6]))
        self.__infilefp.close()
        self.__outfilefp.close()

if __name__ == '__main__':
    fil = Filter("icps_full.txt", "../out.txt")
    fil.do_filter()