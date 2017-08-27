# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import io
import os
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

## driver initialization
def init():
	chrome_path = '/Users/xingobar/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
	chromedriver = "/Users/xingobar/Downloads/chromedriver-3" ## chromedriver 64 bits
	opts = Options()
	opts.binary_location = chrome_path
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver,chrome_options = opts)
	return driver

def getDataByCountry(driver):
	url = 'http://yiqi.16fan.com/list/100005.html'
	driver.get(url)
	csvData =[]
	count = 0
	time.sleep(3)
	anchors = driver.find_elements_by_xpath("//a[@class='yb_box_con']")
	for anchor in anchors:
		csvData.append(anchor.get_attribute('href'))
		print('[*]reading ...... ' + anchor.get_attribute('href'))
		count +=1
		if(count == 8):
			break
	return csvData
		
def readData(csvData):
	commentList = ""
	count = 1
	for url in csvData:
		commentList += "-------------------No."+str(count)
		count += 1
		commentList = commentList + "\nNative Url: " + url +"\n\n"
		data = urllib2.urlopen(url)
		soup = BeautifulSoup(data, "html.parser")
		### read description ###
		content = soup.select("table.yb_detail tr:nth-of-type(4) td:nth-of-type(2)")[0].get_text()
		if(content):
			commentList = commentList + content + "\n"
		### read comment ###
		comments = soup.select("div.yb_comments div.comment_con")
		userComment = ""
		commentCount =  1
		for comment in comments:
			userComment = userComment + "comment [" + str(commentCount) + "]" + comment.get_text() + "\n"
			commentCount +=1
		if(not userComment):
			userComment = "No Comments\n"
		commentList = commentList + "\n[***] Comment . [***]\n" + userComment + "\n"

	writeFile(commentList)


def writeFile(text):
	print('[*]writing file ....')
	filename = datetime.now().strftime('%Y%m%d%H%M%S')
	filename = filename +"_sixteen.txt"
	with io.open(filename,'w',encoding="utf-8") as f:
		f.write(unicode(text))
	print('[*]finsihed')

def test():
	count = 1
	commentList =""
	#data = urllib2.urlopen("http://yiqi.16fan.com/info/112151.html")
	data = urllib2.urlopen("http://yiqi.16fan.com/info/111939.html")
	soup = BeautifulSoup(data, "html.parser")
	### read description
	content = soup.select("table.yb_detail tr:nth-of-type(4) td:nth-of-type(2)")[0].get_text()
	if(content):
		commentList = commentList + content + "\n"
	### read comment
	comments = soup.select("div.yb_comments div.comment_con")
	comentText = ""
	for comment in comments:
		comentText = comentText + comment.get_text() + "\n"

	commentList = commentList + "[*] Comment ." + comentText
	writeFile(commentList)

if __name__ == "__main__":
	### setting utf8 ###
	reload(sys)  
	sys.setdefaultencoding('utf8')
	driver = init()
	data = getDataByCountry(driver)
	readData(data)
	driver.quit()
	#test()
