import time
import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/home/galvinma/Workspace/pythia/chromedriver')

class LoginTest(unittest.TestCase):
    def testLoginHappyPath(self):
        driver.get('http://localhost:5000/');
        time.sleep(2)
        login = driver.find_element_by_id('lg_username')
        login.send_keys('admin')
        time.sleep(1)
        password = driver.find_element_by_id('lg_password')
        password.send_keys('password')
        time.sleep(1)
        sbtn = driver.find_element_by_class_name('login-button')
        sbtn.click()
        time.sleep(5)
    def testTearDown(self):
        driver.quit()
if __name__ == "__main__":
    unittest.main()
