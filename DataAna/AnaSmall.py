#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import Queue

class AnaSmall:
    def __init__(self, file):
        self.__data = xlrd.open_workbook(file)
        self.__table = self.__data.sheets()[0]
        self.__nrows = self.__table.nrows
        self.__ncols = self.__table.ncols
        self.__cols = {25: "PT_YELLOW", 27: "PT_COM", 32: "PT_SUPPLY", 40: "FC_SUPPLY", 42: "FC_YELLOW"}
        self.__dictcode = {1: 1, 10: 10, 11: 11}

#print nrows, ncols

#print table.cell(1, 1).value
#print table.cell(1, 25).value
#if "" == table.cell(4, 25).value:
#    print "HHH"

#if table.cell(1, 25).value < table.cell(8, 25):
#    print table.cell(1, 25).value, table.cell(8, 25).value

    def anaProp(self):
        sectionTotalNum = {}
        sectionShangwuNum = {}
        for row in range(1, self.__nrows):
            for col in self.__cols.keys():
                colSectionTotalNum = {}
                colSectionShangwuNum = {}
                if not sectionTotalNum.has_key(col):
                    sectionTotalNum[col] = {}
                colSectionTotalNum = sectionTotalNum[col]
                if not sectionShangwuNum.has_key(col):
                    sectionShangwuNum[col] = {}
                colSectionShangwuNum = sectionShangwuNum[col]
                value = self.__table.cell(row, col).value
                if "" == value:
                    continue
                shangwuProp = self.__table.cell(row, 8).value
                for i in range(int(value * 100), 0, -1):
                    if colSectionTotalNum.has_key(i):
                        colSectionTotalNum[i] += 1
                    else:
                        colSectionTotalNum[i] = 1
                    if shangwuProp == 1:
                        if colSectionShangwuNum.has_key(i):
                            colSectionShangwuNum[i] += 1
                        else:
                            colSectionShangwuNum[i] = 1

        for col in [25, 27, 32, 40, 42]:
            pq = Queue.PriorityQueue()
            colSectionTotalNum = sectionTotalNum[col]
            colSectionShangwuNum = sectionShangwuNum[col]
            for i in range(100, 0, -1):
                if colSectionTotalNum.has_key(i) and colSectionShangwuNum.has_key(i):
                    ratio = float(colSectionShangwuNum[i]) / colSectionTotalNum[i]
                    tuple = [-ratio, i, ratio, colSectionShangwuNum[i], colSectionTotalNum[i]]
                    pq.put(tuple)
            print self.__cols[col]
            print "threshold\tratio\tshangwu\ttotal"
            for i in [1, 2, 3]:
                if not pq.empty():
                    tuple = pq.get()
                    print float(tuple[1])/100, "\t", tuple[2]*100, "%\t", tuple[3], "\t", tuple[4]

    def anaDictCode(self):
        sectionTotalNum = {}
        sectionShangwuNum = {}
        for row in range(1, self.__nrows):
            for code in self.__dictcode.keys():
                if self.__table.cell(row, 13).value == code:
                    if sectionTotalNum.has_key(code):
                        sectionTotalNum[code] += 1
                    else:
                        sectionTotalNum[code] = 1
                    shangwuProp = self.__table.cell(row, 8).value
                    if shangwuProp == 1:
                        if sectionShangwuNum.has_key(code):
                            sectionShangwuNum[code] += 1
                        else:
                            sectionShangwuNum[code] = 1
                    break
        for col in self.__dictcode.keys():
            print col
            print float(sectionShangwuNum[col]) / sectionTotalNum[col], "\t", sectionShangwuNum[col], "\t", sectionTotalNum[col]

    def filter(self):
        self.__colsThreshold = {25:0.76, 32:0.13, 40:0.5, 42:0.29}
        cols = {25: "PT_YELLOW", 32: "PT_SUPPLY", 40: "FC_SUPPLY", 42: "FC_YELLOW"}
        total = 0
        sample = 0
        for row in range(1, self.__nrows):
            for col in cols.keys():
                prop = self.__table.cell(row, col).value
                if prop == "":
                    continue
                if float(prop) >= self.__colsThreshold[col]:
                    total += 1
                    code = self.__table.cell(row, 13).value
                    if code == 11:
                        sample += 1
                    break
        print "ratio\tshangwu\ttotal"
        print float(sample)/total, "\t", sample, "\t", total

if __name__ == '__main__':
    ana = AnaSmall("5000-garbage.xlsx")
    ana.anaProp()
    ana.anaDictCode()
    ana.filter()