# -*- coding: utf-8 -*-
## http://www.w3schools.com/xml/xpath_axes.asp
## http://selenium-python.readthedocs.io/locating-elements.html
## http://stackoverflow.com/questions/38553512/org-openqa-selenium-invalidselectorexception-object-text-it-should-be-an-el
## http://stackoverflow.com/questions/27626783/python-selenium-browser-driver-back
## http://stackoverflow.com/questions/30316448/for-scrapy-selenium-is-there-a-way-to-go-back-to-a-previous-page
## https://www.python.org/dev/peps/pep-0263/
## http://stackoverflow.com/questions/23498151/how-to-verify-if-a-button-is-enabled-and-disabled-in-webdriver-python
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import pandas as pd
### initalization ###
chrome_path = '/Users/xingobar/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
chromedriver = "/Users/xingobar/Downloads/chromedriver-3" ## chromedriver 64 bits
opts = Options()
opts.binary_location = chrome_path
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver,chrome_options = opts)
#driver.get("https://www.ptt.cc/bbs/Gossiping/index1.html")
#driver.get("https://www.ptt.cc/bbs/Gossiping/index.html")
driver.get("https://www.ptt.cc/bbs/Gossiping/index16651.html")

## end
page =0 

class PTT(unittest.TestCase):

	def test_fetch(self):

		urls = []
		articles = []
		titles = []
		date = []
		push_users = []
		push_contents = []
		push_scores = []
		looping = True
		global page

		try:
			driver.find_element_by_name('yes').click()

		except NoSuchElementException:
			pass
		

		while(self.next_page()):
			## click next page
			if(page >=1):
				page_link = driver.find_elements_by_xpath("//div[@class='btn-group btn-group-paging']/a")
				page_link[2].click()

			div_title = driver.find_elements_by_xpath("//div[@class='title']")

			print 'Starting fetching.....'
			start_time = time.time()
			for idx in xrange(len(div_title)):
				title = driver.find_elements_by_xpath("//div[@class='title']")
				link = title[idx].find_element_by_tag_name('a')
				link.click()
				#article = driver.find_element_by_xpath("//div[@id='main-content']/text()")
				#print article.text
				try:
					url = driver.find_element_by_xpath("//span[@class='f2']/a").text
				except NoSuchElementException:
					url = 'NA'
				profile = driver.find_elements_by_xpath("//span[@class='article-meta-value']")
				#article = profile[0].text
				#title = profile[2].text
				#date = profile[3].text
				urls.append(url)
				articles.append(profile[0].text)
				titles.append(profile[2].text)
				date.append(profile[3].text)


				### push
				try:
					## push 
					push_list = driver.find_elements_by_xpath("//div[@class='push']")
					total_score = 0
					for push in push_list:
						push_tag = push.find_element_by_xpath("//span[@class='f1 hl push-tag']").text
						push_user = push.find_element_by_xpath("//span[@class='f3 hl push-userid']").text
						push_content = push.find_element_by_xpath("//span[@class='f3 push-content']").text
						push_content = push_content.split(':')[1]


						push_users.append(push_user)
						push_contents.append(push_content)
						## error
						try:
							if u'推' in push_tag:
								score = 1
								#print score
							elif u'噓' in push_tag:
								score = -1
								#print score
							else:
								score = 0
								#print score
						except UnicodeDecodeError:
							score =0 
						total_score += score
						#print push_tag
					#push_scores.append(total_score)
					
				except NoSuchElementException:
					push_users.append('No push')
					push_contents.append('No push')
					print 'No push'
				## end push

				## back to previous page
				#driver.execute_script("window.history.go(-1)")
				driver.back()
			end_time = time.time()
			print 'Time is %0.2f' %((end_time - start_time) / 60)
			looping = self.next_page()
			page +=1
			print 'Page %d' %(page)
			print 'going to next page.....'
		
		print 'last page'
		self.write_file()

	def next_page(self):
			
		a_link = driver.find_elements_by_xpath("//div[@class='btn-group btn-group-paging']/a")
		return a_link[2].get_attribute('href')
		#print a_link[2].text,a_link[2].get_attribute('href')

	def write_file(self):
		print 'Writing File ....'
		entry = pd.DataFrame({'Article':articles,'Title':titles,'Date':date,
							  'Url':urls,'Push_User':push_users,
							  'Push_Content':push_contents})
		entry.to_csv('ppt.csv')
		driver.close() ## close tab
		print 'Finish ....'

if __name__ == '__main__':
	unittest.main()




