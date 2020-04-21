
import xml.etree.ElementTree as ET 
#From xml.etree. ElementTree Import Element, SubElement, Comment 
from tkinter.filedialog import asksaveasfile
import tkinter
from builtins import property

class XML:
    def __init__(self, filePath=None):
        self.POMXml=None 
        self.strFileName=None
        self.filePath=None
        if filePath!=None:
            self.filePath=filePath
            self.POMXML=filePath
            
    @property 
    def filePath(self):
        return self.XMLFilePath
    @filePath.setter 
    def filePath(self, strFilePath):
        self.XMLFilePath=strFilePath
    
    def ObjectType(self):
        return self.objtype
    def objectType(self, strobjType):
        self.objtype=strobjType

    @property 
    def POMXML(self):
        return self.POMXml

    @POMXML.setter 
    def POMXML (self, filePath):
        self.XMLtree = ET.parse(filePath) 
        self.XMLroot = self.XMLtree.getroot() 
        currMainObject=POMObject(self.XMLroot) 
        self.POMXml=self.readPOMXML(self.XMLroot, currMainObject)

    def readPOMXML (self,parent,currParentObj):
        parentId=currParentObj.ObjectID 
        if len(list((parent)))>0: 
            for child in list(parent): 
                if child.tag!= 'Property':
                    currObj=currParentObj.addObject(child,parentId)
                    self.readPOMXML(child, currObj) 
        return currParentObj


    def printPOMXML (self,objPOM):
        for child in objPOM.childList:
            print (child.ObjectID) 
            if child.childList!=None and child.childList!=[]:
                self.printPOMXML (child)
    
    @property
    def fileName(self):
        return self.strFileName
    
    @fileName.setter
    def fileName(self, strfileName):
        self.strFileName=strfileName

    def get_Object(self):
        return self.currObject 
    
    def set_Object(self, strName): 
        for pageObject in self.pageList: 
            if pageObject.DisplayName==strName:
                self.currObject=pageObject
                return 
        for webObject in pageObject.WebObjectList: 
            if webObject.DisplayName==strName:
                self.currObject=webObject 
                webObject.parentPageName=pageObject.DisplayName
                return 
    ORObject=property(get_Object,set_Object)

    def saveXML(self,tree, POMTreeView,processType=None): 
        if tree!=None and len(tree.get_children())>0:
            if self.fileName==None:
                files = [( 'ORFile', '*.xml.')] 
                file = asksaveasfile(title = "Select folder", filetypes = files, defaultextension = files) 
                self.filePath=file.name
                self.fileName=((file.name).split('/')[-1]).split('.')[0] 
                self.saveNewXML(tree, POMTreeView)
                
    def saveNewXML(self, POMtree, POMTreeView):
        SelPOMFile = ET.Element( 'POM_File', Name=self.fileName) 
        for child in POMtree.get_children():
            currObj=POMTreeView.treeDict[child] 
            POMPage = ET.SubElement(SelPOMFile, currObj.ObjectType, Name=currObj.DisplayName) 
            self.addProperties(currObj, POMPage)
            self.createChild(currObj, POMPage) 
        tree = ET.ElementTree(SelPOMFile) 
        tree.write(self.filePath)

    def createChild(self,objPOM, POMPage): 
        for child in objPOM.childList:
            POMObject=ET.SubElement(POMPage, child.ObjectType, Name=child.DisplayName)
            self.addProperties(child,POMObject) 
            if child.childList!=None and child.childList!=[]:
                self.createChild(child, POMObject)

    def addProperties(self, currObj,POMObject): 
        for oProp in currObj.propertyList:
            Property=ET.SubElement(POMObject,oProp.ObjectType,Name=oProp.propertyName) 
            ET.SubElement(Property,'IsSelected').text=str(oProp.Selected) 
            ET.SubElement(Property,'value').text=oProp.Value

class POMObject():
    def __init__(self, XMLElement, parentId=None):
        self.ParentId=parentId 
        self.eleXML=XMLElement 
        self.ObjectType=self.eleXML.tag 
        self.DisplayName=XMLElement.get( "Name")
        self.ObjectID=parentId+'_'+self.DisplayName if parentId!=None else self.DisplayName 
        self.childList=[] 
        self.propertylist=[] 
        for oProperty in self.eleXML.findall( 'Property'):
            self.propertylist.append(Property(oProperty))

    def addObject(self,XMLElement, parentId):
        currObj=POMObject(XMLElement,parentId) 
        self.childList.append(currObj) 
        return currObj
    
    @property
    def DisplayName(self):
        return self.strDisplayName
    @DisplayName.setter 
    def DisplayName(self, strDisplayName):
        self.strDisplayName=strDisplayName
    
    @property 
    def ParentId(self):
        return self.objParentId
    @ParentId.setter 
    def ParentId(self,parentId):
        self.objParentId=parentId
        
    @property 
    def ObjectID(self):
        return self.strObjectID
    @ObjectID.setter 
    def ObjectID(self, strObjID):
        self.strObjectID=strObjID
        
    @property 
    def ObjectType(self):
        return self.objType 
    @ObjectType.setter 
    def ObjectType(self,objType):
        self.objtype=objType
        
class Property: 
    def __init__(self,objProperty=None):
        self.ObjectType='Property'
        self.strPropertyName=None 
        self.strPropertyValue=None 
        self.isSelected=None 
        if objProperty!=None:
            self.oProperty=objProperty 
            self.propertyName=self.oProperty.get('Name') 
            self.Value=self.oProperty.find('value').text 
            self.Selected=self.oProperty.find('IsSelected').text
            
    @property
    def propertyName(self):
        return self.strPropertyName 
     
    @propertyName.setter 
    def propertyName(self, strProperty):
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


