#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class CityFilter:
    def __init__(self, cityfile):
        self.__cityfile = cityfile
        self.__isCityFileLoaded = False
        self.__citys = []

    def filter(self, cont):
        if not self.__isCityFileLoaded:
            with open(self.__cityfile, "r") as file:
                for line in file:
                    line = line.decode("cp936").encode("utf-8")
                    words = line.split(" ")
                    for word in words:
                        word = word.strip()
                        if len(word) > 0:
                            self.__citys.append(word)
            self.__isCityFileLoaded = True
        for city in self.__citys:
            if cont.find(city) != -1:
                return True
        return False

    def printCitys(self):
        if not self.__isCityFileLoaded:
            with open(self.__cityfile, "r") as file:
                for line in file:
                    line = line.decode("cp936").encode("utf-8")
                    words = line.split(" ")
                    for word in words:
                        word = word.strip()
                        if len(word) > 0:
                            self.__citys.append(word)
            self.__isCityFileLoaded = True
        for word in self.__citys:
            print word

class FanyuFilter:
    def __init__(self):
        self.__pattern = "^[0-9]+_"
        self.__titlefilter = ["百业网", "博彩", "赌", "娱乐城", "娱乐场", "故事", "情色", "AV", "小说"]

    def filterUrl(self, url):
        items = re.findall(self.__pattern, url)
        if len(items) > 0:
            return True
        else:
            return False
    def filterTitle(self, title):
        for word in self.__titlefilter:
            if -1 != title.find(word):
                return True
            else:
                return False

if __name__ == '__main__':
    cf = CityFilter("city.txt")
    #cf.printCitys()
    ff = FanyuFilter()

    outfile1 = open("filtered.txt", "w")
    outcity = open("outcity.txt", "w")
    outbaiye = open("outbaiye.txt", "w")
    outfanyu = open("outfanyu.txt", "w")
    outsmall10 = open("outsmall.txt", "w")
    with open("head2000ana_dict_code.txt", 'rb') as file:
        for line in file:
            cont = line.strip("\n")
            parts = cont.split("\t")
            url = parts[0]
            title = parts[1].decode('gb18030', 'ignore').encode('utf-8')
            total = parts[7]
            if float(total) <= 10:
                outsmall10.write(line)
                continue
            if cf.filter(title):
                outcity.write(line)
                continue
            if ff.filterTitle(title):
                outbaiye.write(line)
                continue
            if ff.filterUrl(url):
                outfanyu.write(line)
                continue
            outfile1.write(line)