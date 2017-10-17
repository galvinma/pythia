import time
import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sqlalchemy import exists, create_engine, exc
from sqlalchemy.orm import sessionmaker, scoped_session, query
from sqlalchemy.ext.declarative import	declarative_base

from model import DeclarativeBase, User

original_engine = create_engine('postgresql://admin:password@localhost/pythia')
Session = sessionmaker(bind=original_engine)
metadata = DeclarativeBase.metadata
metadata.create_all(original_engine)
session = Session()

driver = webdriver.Chrome('/home/galvinma/Workspace/pythia/chromedriver')
username = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def createnewuser():
    username = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    return username

def commituser(username):
    try:
        user = User(firstname = 'test_firstname',
            lastname = 'test_lastname',
            username = username,
            email = 'testemail@123.com',
            password = 'password',
            profilepicture = 'static/images/profile_default.png')
        session.add(user)
        session.commit()
    except exc.SQLAlchemyError:
        print('Error creating user account')

class CreateUserHappyPath(unittest.TestCase):
    def testCreateUserHappyPath(self):
        username = createnewuser()
        print(username)
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
        time.sleep(2)
        self.assertTrue(driver.find_element_by_id('profilepic'))
        time.sleep(2)

        def TearDown(self):
            driver.quit()

class CreateDuplicateUserTest(unittest.TestCase):
    def testCreateDuplicateUserTest(self):
        username = createnewuser()
        print(username)
        commituser(username)
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
        time.sleep(2)
        self.assertRaises(exc.SQLAlchemyError)
        time.sleep(2)

        def TearDown(self):
            driver.quit()

class LoginHappyPath(unittest.TestCase):
    def testLoginHappyPath(self):
        username = createnewuser()
        print(username)
        commituser(username)
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
        time.sleep(2)
        self.assertTrue(driver.find_element_by_id('profilepic'))
        time.sleep(2)

    def TearDown(self):
        driver.quit()
if __name__ == "__main__":
     unittest.main()
