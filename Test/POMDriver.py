from Test.XMLProcessor import XML
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

objectDict = []


def get_xml(xml_path):
    global objectDict
    xml_pom = XML(xml_path)
    objectDict = xml_pom.treeDict

def create_xpath(self,propertyList):
    tag='*'
    xpath=''
    for oProperty in propertyList:
        if oProperty.Selected=='1' or  oProperty.Selected==1:
            if oProperty.propertyName.strip() == 'tag':
                tag=oProperty.Value
            elif oProperty.propertyName.strip() == 'text' or oProperty.propertyName.strip() == 'innerHTML':
                xpath = xpath + 'text()=\'' + oProperty.Value + '\' and '
            else:
                xpath=xpath+'@'+oProperty.propertyName+'=\''+oProperty.Value+'\' and '
    if xpath=='':
        raise Exception("Xpath is null. Object property not selected"
                        "\n Please make sure that you have selected the property that you intended"
                        " to use for object identification")
    else:
        xpath=('.//'+tag+'['+xpath)[:-4]+']'
        return WebDriver.find_element_by_xpath(self,xpath)


def getElement(self,objectid):
    currobj=objectDict[objectid]
    properties=currobj.propertyList
    return create_xpath(self,properties)

webdriver.uploadXML=get_xml
WebDriver.getElement= getElement