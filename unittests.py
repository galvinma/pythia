import time
import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/home/galvinma/Workspace/pythia/chromedriver')
username = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

class CreateUserTest(unittest.TestCase):
    def testCreateUserHappyPath(self):
        driver.get('http://localhost:5000/');
        time.sleep(2)
        driver.find_element_by_xpath("//*[contains(text(),'create')]").click();
        time.sleep(2)
        login = driver.find_element_by_id('firstname')
        login.send_keys('John')
        time.sleep(1)
        login = driver.find_element_by_id('lastname')
        login.send_keys('Doe')
        time.sleep(1)
        login = driver.find_element_by_id('email')
        login.send_keys('jdoe@gmail.com')
        time.sleep(1)
        login = driver.find_element_by_id('username')
        login.send_keys(username)
        time.sleep(1)
        login = driver.find_element_by_id('password')
        login.send_keys('password')
        time.sleep(1)
        sbtn = driver.find_element_by_class_name('login-button')
        sbtn.click()
        self.assertEqual(response.status_code, 200)
        time.sleep(5)

        def testTearDown(self):
            driver.quit()

#class CreateDuplicateUserTest(unittest.TestCase):
#    def testCreateDuplicateUserTest(self):

class LoginTest(unittest.TestCase):
    def testLoginHappyPath(self):
        driver.get('http://localhost:5000/');
        time.sleep(2)
        login = driver.find_element_by_id('lg_username')
        login.send_keys(username)
        time.sleep(1)
        password = driver.find_element_by_id('lg_password')
        password.send_keys('password')
        time.sleep(1)
        sbtn = driver.find_element_by_class_name('login-button')
        sbtn.click()

    def testTearDown(self):
        driver.quit()
if __name__ == "__main__":
    unittest.main()
