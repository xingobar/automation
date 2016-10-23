from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import page

chrome_path = 'chrome'
chromedriver = "binary file"
opts = Options()
opts.binary_location = chrome_path
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver,chrome_options = opts)
driver.get('https://accounts.google.com/SignUp?continue=https%3A%2F%2Fwww.google.com.tw%2F%3Fpli%3D1&hl=zh-TW')
main_page = page.MainPage(driver)
main_page.fill_in_form()


