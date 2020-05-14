from Test.POMDriver import webdriver

webdriver.uploadXML('../Resources/FirstOne.xml')
driver=webdriver.Firefox(executable_path='../Resources/geckodriver.exe')
driver.get('https://www.python.org/')
driver.getElement('FirstOne_Welcome to Python.org_a_Donate').click()


