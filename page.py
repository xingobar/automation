## https://www.foolegg.com/how-to-get-the-users-input-in-python-with-input-or-raw_input-functions/
## http://www.qa-knowhow.com/?p=1930
## http://stackoverflow.com/questions/20587449/selenium-click-working-but-submit-isnt
## http://docs.seleniumhq.org/docs/03_webdriver.jsp#user-input-filling-in-forms
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
class BasePage(object):

	def __init__(self,driver):
		self.driver = driver


class MainPage(BasePage):


	def fill_in_form(self):

		driver = self.driver
		## input name
		LastName = driver.find_element_by_xpath("//input[@name='LastName']")
		FirstName = driver.find_element_by_xpath("//input[@name='FirstName']")
		EmailAddress = driver.find_element_by_xpath("//input[@name='GmailAddress']")
		Password = driver.find_element_by_xpath("//input[@name='Passwd']")


		## fill value
		LastName_values = raw_input("LastName : ")
		FirstName_values = raw_input("FirstName : ")
		EmailAddress_values = raw_input("EmailAddress : ")
		LastName.send_keys(LastName_values)
		FirstName.send_keys(FirstName_values)
		EmailAddress.send_keys(EmailAddress_values)
		Password.send_keys('xingobar')

		## check email 

		try:
			wrapper = driver.find_element_by_xpath("//div[@id='username-suggestions']")
			## waiting AJAX
			WebDriverWait(driver,100).until(
				lambda wrapper:wrapper.find_element_by_tag_name('a')
			)
			email_list = []
			a_list = wrapper.find_elements_by_tag_name('a')
			for i in a_list:
				email_list.append(i.text)
			print email_list
			print 'choosing the first email address....'
			EmailAddress.clear()
			EmailAddress_values = email_list[0]
			EmailAddress.send_keys(email_list[0])

		except Exception:
			print 'EmailAddress OK'
			

		Passowrd_again = driver.find_element_by_xpath("//input[@name='PasswdAgain']")
		Passowrd_again.send_keys('xingobar')

		Birthday_year = driver.find_element_by_xpath("//input[@name='BirthYear']")
		print 'birthday_year set default value ....'
		Birthday_year.send_keys('1995')

		## select options
		## loading ajax
		month_wrapper = driver.find_element_by_xpath("//div[@class='goog-inline-block goog-flat-menu-button jfk-select']")
		WebDriverWait(driver,100).until(
			lambda month_wrapper:month_wrapper.find_element_by_tag_name('div')
		)
		month_values = month_wrapper.find_elements_by_tag_name('div')
		click_dropdown = month_values[1].click()
		dropdown_wrapper = driver.find_element_by_xpath("//div[@class='goog-menu goog-menu-vertical']")
		month_list = dropdown_wrapper.find_elements_by_tag_name('div') ## month list 1- 12 month
		month_list[1].click() ## choose 1 month
		#month_list[2].click() ## choose 2 month
		print 'choose 1 month .....'
		## end select 

		Birthday_day = driver.find_element_by_xpath("//input[@name='BirthDay']")
		print 'birthday_day set default value ...'
		Birthday_day.send_keys(27)

		## choose sender 
		gender_wrapper = driver.find_element_by_xpath("//div[@id='Gender']/div/div")
		gender_wrapper.click()
		dropdown = driver.find_elements_by_xpath("//div[@id='Gender']/div/div[@class='goog-menuitem']")
		print 'choose man options ...'
		sender = dropdown[1].click()
		## end  

		## write file
		print 'Writing the file.....'
		f = open('google_account.txt','w')
		f.write('Account : ' +  EmailAddress_values + "@gmail.com \n")
		f.write('Password : xingobar\n' )
		f.write('Birthday : 1995/01/27\n' )
		f.write('Sender : male\n')
		f.close()
		print 'complete .....'
		## end
		
		## http://stackoverflow.com/questions/17530104/selenium-webdriver-submit-vs-click
		## http://stackoverflow.com/questions/20587449/selenium-click-working-but-submit-isnt
		##form = driver.find_element_by_xpath("//form[@id='createaccount']")
		form = driver.find_element_by_xpath("//input[@id='submitbutton']")
		
		
		print 'complete create google account'

