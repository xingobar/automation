## http://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1
## http://stackoverflow.com/questions/19200497/python-selenium-webscraping-nosuchelementexception-not-recognized
## http://engineering.aweber.com/getting-started-with-ui-automated-tests-using-selenium-python/
## http://stackoverflow.com/questions/12711211/receiving-error-multiple-values-for-index-in-a-simple-data-frame
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import pandas as pd
### initalization ###
chrome_path = Chome File
chromedriver = Binary File
opts = Options()
opts.binary_location = chrome_path
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver,chrome_options = opts)
driver.get("http://scweb.cwb.gov.tw/Page.aspx?ItemId=20&loc=tw&adv=1")

## end


#select = Select(driver.find_element_by_id('ctl03_ddlMonth'))
#options = select.options ## get all available options
month = []
magnitude = []
depth  = []
longitude = []
latitude = []

month_select = driver.find_element_by_id('ctl03_ddlMonth')
month_options = month_select.find_elements_by_tag_name('option')
class Earthquake(unittest.TestCase):

	def test_option(self):
		for option in xrange(10):
			
			## you must fetch again when the page is reloading
			WebDriverWait(driver,100).until(
				lambda driver:driver.find_element_by_id('ctl03_ddlMonth'),
				lambda month_select:month_select.find_elements_by_tag_name('option')
			)
			month_select = driver.find_element_by_id('ctl03_ddlMonth')
			test_month_options = month_select.find_elements_by_tag_name('option')
			test_month_options[option].click()
			#option.click()
			submit = driver.find_element_by_id('ctl03_btnSearch')
			submit.click()

			## detecting whether it can fetch the table element
			try:
				## loading ajax
				WebDriverWait(driver,100).until(
					lambda driver:driver.find_element_by_id('ctl03_gvEarthquake')
				)
				table = driver.find_element_by_id('ctl03_gvEarthquake') ## find table tag
				total_tr = table.find_elements_by_tag_name('tr')
				for j in xrange(len(total_tr)):
					if j >=1 :
						total_td = total_tr[j].find_elements_by_tag_name('td')
						month.append(option+1)
						#month.append(option.get_attribute('value'))
						longitude.append(total_td[2].text)
						latitude.append(total_td[3].text)
						magnitude.append(total_td[4].text)
						depth.append(total_td[5].text)
			except NoSuchElementException:
				break
			except TimeoutException:
				break
			#driver.implicitly_wait(100)

	def test_write(self):
		## columns
		d = {'Month':month,'Longitude':longitude,'Latitude':latitude,
			'Magnitude':magnitude,'Depth':depth}
		data = pd.DataFrame(d)
		data.to_csv('2016-earthquake.csv')
		driver.close()
unittest.main()




