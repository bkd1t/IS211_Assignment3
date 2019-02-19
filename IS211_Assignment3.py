#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 3, Task 01"""
import urllib
import csv
from datetime import datetime
import os
import argparse
import operator
parser = argparse.ArgumentParser()
#parser.add_argument("--url", help="the url for the csv", action="store_true")
parser.add_argument('url', nargs='?', default="")
#_StoreAction(option_strings=[], dest='dir', nargs='?', const=None, default='', type=None, choices=None, help=None, metavar=None)
args = parser.parse_args()
if args.url:
    my_url = args.url
else:
    exit(0)

def downloadData(url):
    """ download the contents located at the ​url.
    """
    raw_data = urllib.urlopen(url).readlines()    
    return raw_data


def processData(raw_data):
    """ process the url data.
    """
    logf = open("errors.log", "w")
    res = {}
    browser_hits = {'Chrome':0,'Internet Explorer':0,'Firefox':0,'Safari':0,}
    hour_hits = {}
    img_file_count = 0
    count = len(raw_data)
    #for i,each in enumerate(raw_data): row in csv.reader(lines, delimiter=" "):
    for each in csv.reader(raw_data, delimiter=","):
	x = each
	if each[0].lower().endswith(('.png', '.jpg', '.jpeg','.gif')):
	    img_file_count+=1
	if 'MSIE' in each[2]:
	    browser_hits['Internet Explorer'] = browser_hits['Internet Explorer']+1
	elif 'Chrome'in each[2]:
	    browser_hits['Chrome'] = browser_hits['Chrome']+1
	elif 'Firefox'in each[2]:
	    browser_hits['Firefox'] = browser_hits['Firefox']+1
	else:
	    browser_hits['Safari'] = browser_hits['Safari']+1
	
	d = datetime.strptime(each[1], '%Y-%m-%d %H:%M:%S')
	hour_check = d.hour + 1
	if hour_hits.has_key(hour_check):
	    hour_hits[hour_check] = hour_hits[hour_check]+1
	else:
	    hour_hits.update({hour_check:1})

    img_file_percentage = (img_file_count/float(count))*100
    print "Image requests account for {0}% of all requests ".format(str(img_file_percentage))	
    most_popular_browser = max(browser_hits.iteritems(), key=operator.itemgetter(1))[0]
    print "{0} is the most popular browser today".format(str(most_popular_browser))
    for each in hour_hits:
        print "Hour {0} has {1} hits".format(str(each),str(hour_hits[each]))
    
    return res


def main():
  raw_data = downloadData(my_url)
  browserData = processData(raw_data)
  
if __name__== "__main__":
  main()

