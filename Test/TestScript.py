import inspect
from  Test.POMDriver1 import webdriver

webdriver.uploadXML('C:/Users/maan/PycharmProjects/GIT/SeleniumPOM/Resources/FirstOne.xml')
driver=webdriver.Firefox(executable_path='C:/Users/maan/PythonGit/SeleniumPOM/Resources/geckodriver.exe')
driver.get('https://www.python.org/')
driver.getElement('FirstOne_Python Software Foundation_a_Bylaws')
#POMDriver = webdriver.POMDriver('C:/Users/maan/PycharmProjects/GIT/SeleniumPOM/Resources/FirstOne.xml')
#a = POMDriver.Page('FirstOne_a').Frame('f').WebObject('o')
#print(a)

