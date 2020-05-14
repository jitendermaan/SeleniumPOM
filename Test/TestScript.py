import inspect
from  Test.POMDriver1 import webdriver

webdriver.uploadXML('../Resources/FirstOne.xml')
driver=webdriver.Firefox(executable_path='../Resources/geckodriver.exe')
driver.get('https://www.python.org/')
driver.getElement('FirstOne_Welcome to Python.org_a_Donate').click()
#POMDriver = webdriver.POMDriver('C:/Users/maan/PycharmProjects/GIT/SeleniumPOM/Resources/FirstOne.xml')
#a = POMDriver.Page('FirstOne_a').Frame('f').WebObject('o')
#print(a)

