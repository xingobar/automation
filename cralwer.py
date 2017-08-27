# -*- coding: utf-8 -*-
### https://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
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

### initalization ###
def init():
	chrome_path = '/Users/xingobar/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
	chromedriver = "/Users/xingobar/Downloads/chromedriver-3" ## chromedriver 64 bits
	opts = Options()
	opts.binary_location = chrome_path
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver,chrome_options = opts)
	return driver

def getDataByCountry(driver):
	url = 'http://bbs.qyer.com/forum-2-1.html'
	driver.get(url)
	tableData = driver.find_elements_by_xpath("//table[@class='conitm  active']/tbody/tr/td/a")
	for data in tableData:
		if data.text == '台湾'.encode("utf8"):
			print '[*]click taiwan'
			data.click()
			crawlerData = crawler(driver)
			readData(crawlerData)	
			break
			
csvData = []
count = 0
def crawler(driver):
	global csvData
	global count
	driver.implicitly_wait(15) # waiting 15 seconds
	cards = driver.find_elements_by_xpath("//a[@class='card']")
	for card in cards:
		href = card.get_attribute('href')
		print('reading %s .......' %(href))
		time.sleep(0.5)
		dict = {'url':href}
		csvData.append(dict)
		count +=1
		if(count == 8):
			print('Finished...')
			break
	return csvData

def scroll(driver):
	SCROLL_PAUSE_TIME = 5

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")
	print('[*]scrolling........')
	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)
	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	    	print('[*]scroll to end')
	        break
	    last_height = new_height

def readData(csvData):
	commentList = ""
	global count
	count = 1
	for dictionary in csvData:
		commentList += "-------------------No."+str(count)
		count += 1
		commentList = commentList + "\nNative Url: " + dictionary['url'] +"\n"
		data = urllib2.urlopen(dictionary['url'])
		soup = BeautifulSoup(data, "html.parser")
		content = soup.find("li",{"class":'xlast xmt20'})

		## description
		if(content):
			text = content.get_text()
			commentList = commentList + text + "\n"

		## comments wrapper
		detailContent = soup.findAll("div",{"class":"bbs_detail_content"}) 
		userComment = ""
		commentCount = 1
		for content in detailContent:
			## get comment from comment wrapper
			contentList = content.select("table tr td.bbsDetailContainer")
			if(contentList):
				comment = contentList[0]
				userComment = userComment + "comment [" + str(commentCount) + "]" + comment.get_text().strip() + "\n"
				commentCount +=1
		
		if(not userComment):
			userComment = "No Comments\n"

		commentList = commentList + "\n[***] Comment . [***]\n" + userComment + "\n"

	writeFile(commentList)


def writeFile(text):
	print('[*]writing file ......')
	filename = datetime.now().strftime('%Y%m%d%H%M%S')
	filename = filename +"_poor.txt"
	with io.open(filename,'w') as f:
		f.write(text)
	print('[*]Finsihed....')

def test():
	#http://bbs.qyer.com/thread-2809444-1.html
	commentList =""
	data = urllib2.urlopen("http://bbs.qyer.com/thread-2809444-1.html")
	soup = BeautifulSoup(data, "html.parser")
	content = soup.find("li",{"class":'xlast xmt20'})
	if(content):
		text = content.get_text()
		commentList = commentList + text + "\n"
	
	detailContent = soup.findAll("div",{"class":"bbs_detail_content"}) ## comments
	userComment = ""
	commentCount = 1
	for content in detailContent:
		contentList = content.select("table tr td.bbsDetailContainer p")
		if(contentList):
			comment = contentList[0]
			userComment = userComment + "comment [" + str(commentCount) + "]" + comment.get_text() + "\n"
			commentCount +=1

	if(not userComment):
		userComment = "No Comments\n"
	
	commentList = commentList + "\n[***] Comment . [***]\n" + userComment + "\n"
	writeFile(commentList)
        
if __name__ == "__main__":
	### setting utf8 ###
	reload(sys)  
	sys.setdefaultencoding('utf8')
	driver = init()
	getDataByCountry(driver)
	#test()
	driver.quit()
	


