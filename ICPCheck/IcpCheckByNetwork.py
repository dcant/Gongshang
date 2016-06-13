# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import urllib2


def perror_and_exit(message, status=-1):
    sys.stderr.write(message + '\n')
    sys.exit(status)


def get_text_from_html_tag(html):
    pattern_text = re.compile(r">.*?")
    return pattern_text.findall(html)[0][1:-2].strip()


def parse_alexa(url):
    url_alexa = "http://icp.alexa.cn/index.php?q=%s" % url
    print url_alexa
    # handle exception
    times = 0
    while times < 5000:  # 等待有一定次数限制
        try:
            alexa = urllib2.urlopen(url_alexa).read()

            pattern_table = re.compile(r"网站备案/许可证号</td>.*?<td>(.*?)</td>", re.DOTALL | re.MULTILINE)
            item = re.findall(pattern_table, alexa)
            for i in item:
                print i
            if not item:
                raise BaseException("No table in HTML")
            break
        except:
            print "try %s times:sleep %s seconds" % (times, 2 ** times)
            times += 1
            time.sleep(2 ** times)
            continue


if __name__ == "__main__":
    url = sys.stdin.readline()
    parse_alexa(url)

