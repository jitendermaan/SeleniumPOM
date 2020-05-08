import xml.etree.ElementTree as ET
#from xml.etree. ElementTree import Element, SubElement, Comment from tkinter.filedialog import asksaveasfile import tkinter


class XML:
    def __init__(self,filePath=None):
        self.POMXml=None
        self.strFileName = None
        self.filePath = None
        self.treeDict = {}
        self.currObject = None
        if filePath is not None:
            self.filePath = filePath
            self.POMXML = filePath
            self.fileName = (self.filePath.split('/')[-1]).split(':')[0]
    @property
    def filePath(self):
        return self.XMLFilePath
    @filePath.setter
    def filePath(self, strFilePath):
        self.XMLFilePath=strFilePath
    @property
    def ObjectType(self):
        return self.objtype
    @ObjectType.setter
    def ObjectType(self, strobjtype):
        self.objtype=strobjtype

    @property
    def POMXML(self):
        return self.POMXml

    @POMXML.setter
    def POMXML(self, filePath):
        self.XMLtree = ET.parse(filePath)
        self.XMLroot = self.XMLtree.getroot()
        currMainObject = POMObject(self.XMLroot)
        self.treeDict[currMainObject.ObjectID] = currMainObject
        self.POMXml = self.readPOMXML(self.XMLroot, currMainObject)

    def readPOMXML(self, parent, currParentObj):
        currParentID = currParentObj.ObjectID if currParentObj.ObjectType!= 'POM File' else None
        if len(list((parent)))>0:
            for child in list(parent):
                if child.tag!= 'Property':
                    currObj=currParentObj.addObject(child,currParentID)
                    self.treeDict[currObj.ObjectID]=currObj
                    print(currObj.ObjectID)
                    self.readPOMXML ( child, currObj)
        return currParentObj

    def printPOMXML ( self, objPOM):
        for child in objPOM.childList:
            print (child.ObjectID)
            if child.childList!=None and child.childList!=[]:
                self.printPOMXML (child)

    @property
    def fileName(self):
        return self.strFileName
    @fileName.setter
    def fileName(self,strfileName):
        self.strFileName=strfileName

    def get_Object(self):
        return self.currObject

    def set_Object(self, strName):
        for pageObject in self.pageList:
            if pageObject.DisplayName==strName:
                self.currObject=pageObject
                return
            for webObject in pageObject. WebObjectList:
                if webObject.DisplayName==strName:
                    self.currObject=webObject
                    webObject.parentPageName=pageObject.DisplayName
                    return
    ORObject=property (get_Object, set_Object)


class POMObject():
    def __init__(self,XMLElement, parentId=None):
        self.strobjectID = None
        self.ParentId=parentId
        self.eleXML=XMLElement
        self.ObjectType=self.eleXML.tag
        self.DisplayName=XMLElement.get('Name')
        self.ObjectID=parentId+'_'+self.DisplayName if parentId!=None else self.DisplayName
        self.childList=[]
        self.propertyList=[]

        for oProperty in self.eleXML.findall( 'Property'):
            self.propertyList.append(Property(oProperty))

    def addObject(self,XMLElement, parentId):
        currObj=POMObject(XMLElement,parentId)
        self.childList.append(currObj)
        return currObj
    @property
    def DisplayName(self):
        return self.strDisplayName

    @DisplayName.setter
    def DisplayName(self, strdisplayName):
        self.strDisplayName = strdisplayName

    @property
    def ParentId(self):
        return self.objParentId

    @ParentId.setter
    def ParentId(self, parentId):
        self.objParentId = parentId

    @property
    def ObjectID(self):
        return self.strobjectID

    @ObjectID.setter
    def ObjectID(self, strobjId):
        self.strobjectID = strobjId

    @property
    def ObjectType(self):
        return self.objType \

    @ObjectType.setter
    def ObjectType(self, objType):
        self.objType = objType


class Property:

    def __init__(self, objProperty=None):
        self.ObjectType = 'Property'
        self.strPropertyName = None
        self.strPropertyValue = None
        self.isSelected = None
        if objProperty != None :
            self.oProperty = objProperty
            self.propertyName = self.oProperty.get('Name')
            self.Value = self.oProperty.find('value').text
            self.Selected=self.oProperty.find('IsSelected').text

    @property
    def propertyName(self):
        return self.strPropertyName

    @propertyName.setter
    def propertyName(self,strProperty):
        self.strPropertyName=strProperty

    @property
    def Value(self):
        return self.strPropertyValue
    @Value.setter
    def Value(self, strPropertyVal):
        self.strPropertyValue=strPropertyVal

    @property
    def Selected(self):
        return self.isSelected

    @Selected.setter
    def Selected(self, intIsSelected):
        self.isSelected=intIsSelected

