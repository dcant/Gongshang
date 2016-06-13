#!/usr/bin/python
# -*- coding: utf-8 -*-

class AnaLarge:
    def __init__(self, infile, outfile):
        self.__cols = {14:"PT_YELLOW", 21:"PT_SUPPLY", 29:"FC_SUPPLY", 31:"FC_YELLOW"}
        self.__colsThreshold = {14:0.76, 21:0.13, 29:0.5, 31:0.29}
        self.__outfile = open(outfile, "w")
        self.__infile = infile

    def run(self):
        with open(self.__infile, "r") as file:
            total = 0
            sample = 0
            for line in file:
                cont = line.strip("\n")
                items = cont.split("\t")
                total += 1
                for col in self.__cols.keys():
                    if float(items[col]) >= self.__colsThreshold[col]:
                        self.__outfile.write(line)
                        sample += 1
                        break
            print float(sample) / total
        file.close()

    def __del__(self):
        self.__outfile.close()

if __name__ == '__main__':
    ana = AnaLarge("1000.txt", "large.txt")
    ana.run()