from Test.XMLProcessor import XML
import inspect
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

objectDict = []


def get_xml(xml_path):
    global objectDict
    xml_pom = XML(xml_path)
    objectDict = xml_pom.treeDict


class POMDriver:
    def __init__(self, xmlpath):
        self.XML = XML(xmlpath)
        self.Dict = self.XML.treeDict
        self.ObjectId = None
        self.objPage=None
    def Page(self,pagename):
        self.ObjectId=pagename
        self.objPage=Page(self.Dict,pagename)
        #self.ObjectId=self.objPage.ObjectID
        return self.objPage
        #print (str(len(inspect.stack())))
        #statement = inspect.stack()[len(inspect.stack())-1].code_context[0]
        #objectaddrress = statement.split('Page')[1]  # add catch for index out of range
        #print ('left :'+str(statement.index('Page(\'')+len('Page(\'')))
        #print ('right:'+str(statement.index('\')')))
        #print (statement[20:30])
        #for i in objectaddrress.split(').'):
        #    print(i)
        #return Page(self.Dict,pagename)



class Page:
    def __init__(self, treedict,pageName):
        self.ObjectID=pageName
        self.objFrame=None
        self.ObjWebObject=None
        self.treeDict=treedict
        self.PageObject=self.treeDict[pageName]
        self.objectID=self.PageObject.ObjectID


    def Frame(self, FrameName):
        self.objFrame=Frame(self.ObjectID+'_'+FrameName)
        return self.objFrame.ObjectID

    def WebObject(self,objectName):
        self.ParentObjectID =self.ParentObjectID+'_'+objectName

    @property
    def ObjectID(self):
        return self.strObjectID
    @ObjectID.setter
    def ObjectID(self,strObjectID):
        self.strObjectID=strObjectID

class WebObject:

    def __init__(self,objectid):
        self.strObjectID=None
        self.ObjectID=objectid

    @property
    def ObjectID(self):
        return self.strObjectID

    @ObjectID.setter
    def ObjectID(self, strObjectID):
        self.strObjectID = strObjectID


class Frame:
    def __init__(self, ObjectID):
        self.strObjectID = None
        self.ObjectID = ObjectID
        self.ObjWebObject=None

    def WebObject(self, objectname):
        self.ObjWebObject=WebObject(self.ObjectID+'_'+objectname)
        return self.ObjWebObject
    @property
    def ObjectID(self):
        return self.strObjectID
    @ObjectID.setter
    def ObjectID(self,strObjectID):
        self.strObjectID=strObjectID