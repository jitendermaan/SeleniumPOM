'''
Created on Apr 19, 2020

@author: maan
'''
import sys 
import xml.etree.ElementTree as ET 
from tkinter import IntVar,StringVar, Checkbutton, TclError,messagebox 
import POM.Util as Util 

class POMTree: 
    def __init__(self,config, tree=None, XML=None):
        self.XMLFilePath=None 
        self.config=config 
        self.pomobject=None 
        self.XML=XML 
        self.tree=tree 
        self.treeDict={} 
        if self.XML!=None and self.XML.filePath!=None and self.tree!=None:
            self.createTree()

    def createTree(self,XML, tree, processType=None):
        try:
            self.tree=tree 
            self.XML=XML 
            self.XMLFilePath=self.XML.filePath 
            self.XMLtree = ET.parse(self.XMLFilePath) 
            self.XMLroot = self.XMLtree.getroot() 
            if processType=='newfile':
                self.setTreeHeading(self.XML.fileName) 
            else:
                self.setTreeHeading(self.XMLroot.get( 'Name')) 
            self.currMainobject=TreePOMObject(xmlelement=self.XMLroot)
            self.POMXml=self.createPOMTree(self.XMLroot, self.currMainobject) 
        except ET.ParseError: 
            if processType=='newfile':
                self.setTreeHeading(self.XML.fileName)


    def createPOMTree(self, parent, currParentObj):
        currParentID=currParentObj.ObjectID if currParentObj.ObjectType!='POM_File' else None 
        if len(list((parent)))>0: 
            for child in list(parent): 
                if child.tag!='Property':
                    currObj=currParentObj.addobject(xmlelement=child,parentid=currParentID) 
                    self.treeDict[currObj.ObjectID]=currObj
                    currObj.addTree(self.tree, parentid=currParentID)
                    self.createPOMTree(child, currObj) 
        return currParentObj

    def printPOMXML (self, objPOM):
        for child in objPOM.childList:
            print (child.ObjectID) 
            if child.childList!=None and child.childList!=[]:
                self.printPOMXML (child)

    def get_Object(self):
        return self.pomObject 
    
    def set_Object(self, treeObjectId):
        obj=None 
        self.pomObject =self.treeDict[treeObjectId]
        return obj 
    ORObject=property(get_Object,set_Object)

    def updateTreeChild(self,currParentObj):
        currParentID=currParentObj.ObjectID if currParentObj.ObjectType!='POM_File' else None
        for child in currParentObj.childList:
            child.ParentID=currParentID 
            child.ObjectID=currParentID+'_'+child.DisplayName 
            child.addTree(self.tree,parentid=currParentID) 
            self.treeDict[child.ObjectID]=child
            self.updateTreeChild(child) 
        return currParentObj
    
    def updateTree (self, tree, currObject, **kwargs):
        parentObject = kwargs['parentid'] if 'parentid' in kwargs and kwargs['parentid']!=None else'' 
        index= kwargs['index'] if 'index' in kwargs and kwargs['index']!=None else 'end' 
        tree.insert(parentObject, index, iid=currObject.ObjectID, text=currObject.DisplayName) 
        self.updateTreeChild(currObject)
    
    def setTree(self, tree):
        self.tree=tree 
    def setTreeHeading(self,strval):
        self.tree.heading('#0', text=strval)
        
    def updateObjectProperty(self, tree, treeValues, currItem, actionType=None):
        try:
            startindex=2 
            index=tree.index(currItem) 
            currObj=self.treeDict[currItem] 
            self.treeDict.pop(currItem) 
            if currObj.DisplayName!=(treeValues.grid_slaves(0,1)[0]).get():
                currObj.DisplayName=(treeValues.grid_slaves(0,1)[0]).get() 
                currObj.ObjectID=currObj.ParentID+'_'+currObj.DisplayName if currObj.ParentID!=None else currObj.DisplayName 
                self.updateTree (tree, currObj,parentid=currObj.ParentID, index=index) 
                tree.delete(currItem)
                currItem=currObj.ObjectID 
            y=treeValues.grid_size()[1] 
            currObj.propertyList.clear()
            for i in range (startindex,y-1):
                oProperty=Property()
                oProperty.propertyName=(treeValues.grid_slaves(i,0)[0]).cget('text') 
                oProperty.Value=(treeValues.grid_slaves(i,1)[0]).get() 
                oProperty.Selected=(treeValues.grid_slaves(i,0)[0]).is_selected.get() 
                currObj.propertyList.append(oProperty)
    
            self.treeDict[currObj.ObjectID]=currObj
            return currObj 
        except TclError as e:
            print(str(e)) 
            messagebox.showinfo(e, e )

    def addProperty(self, tree, currItem, treeValues):
        tree.selection_remove(currItem) 
        currObj=self.treeDict[currItem] 
        oProperty=Property() 
        oProperty.propertyName=(treeValues.grid_slaves(0,1)[0]).get() 
        oProperty.Value=(treeValues.grid_slaves (1,1)[0]).get() 
        oProperty.Selected=0 
        currObj.propertyList.append(oProperty) 
        treeValues.destroy() 
        tree.selection_set(currItem)


class TreePOMObject():
    def __init__(self,**kwargs):
        self.childList=[] 
        self.propertyList=[] 
        self.objParentID=None 
        self.strObjectID=None 
        self.attrDict={}
        self.strDisplayName=None 
        if 'xmlelement' in kwargs and kwargs [ 'xmlelement']!=None:
            self.ParentID=kwargs['parentid'] if 'parentid' in kwargs else None 
            self.eleXML=kwargs['xmlelement'] 
            self.ObjectType=self.eleXML.tag 
            self.DisplayName=self.eleXML.get( 'Name') 
            self.ObjectID=self.ParentID+'_'+self.DisplayName if self.ParentID!=None else self.DisplayName 
            for oProperty in self.eleXML.findall( 'Property'):
                self.propertyList.append(Property(oProperty)) 
                
        if 'objectaction' in kwargs and kwargs['objectaction']=='newobject' and 'attributeDict' in kwargs and kwargs['attributeDict'] !=None:
            self.attrDict=kwargs['attributeDict'] 
            self.DisplayName=kwargs['displayname'] 
            self.ParentID=kwargs['parentid'] if 'parentid' in kwargs else None 
            self.ObjectID=self.ParentID+'_'+self.DisplayName if self.ParentID!=None else self.DisplayName 
            if 'objecttype' in kwargs and kwargs ['objecttype']!=None:
                self.ObjectType=kwargs['objecttype'] 
            elif 'tag' in self.attrDict and (self.attrDict['tag']=='frame' or self.attrDict['tag']=='iframe'):
                self.ObjectType='POM_' +self.attrDict['tag'] 
            else:
                self.ObjectType='POM_Object'
        if 'Display Name' in self.attrDict : self.attrDict.pop( 'Display Name') 
        if 'Object Type' in self.attrDict : self.attrDict.pop( 'Object Type') 
        for key, value in self.attrDict.items():
            self.property=Property() 
            self.property.propertyName=key 
            self.property.Value=value 
            self.property.Selected=0 
            self.propertyList.append(self.property)
    
    def addobject(self, **kwargs) : 
        if 'xmlelement' in kwargs and 'parentid' in kwargs:
            currObj=TreePOMObject(xmlelement=kwargs['xmlelement'], parentid=kwargs['parentid']) 
            self.childList.append(currObj)
        return currObj
    
    def addTree(self, tree, **kwargs) :
        parentObject = kwargs['parentid'] if 'parentid' in kwargs and kwargs['parentid']!=None else ''
        index= kwargs['index'] if 'index' in kwargs and kwargs['index']!=None else 'end' 
        objectId=kwargs['objectid'] if 'objectid' in kwargs and kwargs['objectid']!=None else self.ObjectID 
        displayName=kwargs['displayname'] if 'displayname' in kwargs and kwargs['displayname'] !=None else self.DisplayName 
        print (parentObject+objectId)
        tree.insert(parentObject, index, iid=objectId, text=displayName) 
        
    @property 
    def DisplayName(self):
        return self.strDisplayName

    @DisplayName.setter 
    def DisplayName(self, strdisplayName) :
        self.strDisplayName=strdisplayName

    @property 
    def ParentID(self):
        return self.objParentID

    @ParentID.setter 
    def ParentID(self,ParentID):
        self.objParentID=ParentID

    @property 
    def ObjectID(self):
        return self.strObjectID
    
    @ObjectID.setter 
    def ObjectID(self, strobjId):
        self.strObjectID=strobjId
    
    @property 
    def ObjectType(self):
        return self.objType 
    
    @ObjectType.setter 
    def ObjectType(self, objType):
        self.objType=objType

class Property: 
    def __init__(self,objProperty=None, **kwargs):
        self.ObjectType='Property' 
        self.strPropertyName=None 
        self.strPropertyValue=None 
        self.isSelected=None 
        if objProperty!=None:
            self.oProperty=objProperty 
            self.propertyName=self.oProperty.get('Name') 
            self.Value=self.oProperty.find('value').text 
            self.Selected=self.oProperty.find('IsSelected').text 
            if 'newobject' in kwargs: 
                self.newObj=kwargs['newobject']
    
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
    def Value(self,strPropertyVal):
        self.strPropertyValue=strPropertyVal

    @property 
    def Selected(self):
        return self.isSelected 
    @Selected.setter 
    def Selected(self,intIsSelected):
        self.isSelected=intIsSelected
        
class ObjectPropertyTree:
    def __init__(self, tree, attributeList=None, **kwargs):
        self.objTree=tree 
        self.attrList=attributeList 
        self.objectDict={} 
        self.objectId=None 
        self.ParentID=None 
        self.manualTreeVals=kwargs['treevals'] if 'treevals' in kwargs else None 
        if attributeList!=None:
            currMainObjectAttr=self.attrList.pop(0) 
            self.currMainObject=TreePOMObject(objectaction='newobject', attributeDict=currMainObjectAttr,displayname=currMainObjectAttr['Display Name'],objecttype='POM_Page') 
            self.objectDict[self.currMainObject.ObjectID]=self.currMainObject 
            self.currMainObject.addTree(self.objTree, objectid=self.currMainObject.ObjectID,displayname=self.currMainObject.DisplayName) 
            self.ParentID=self.currMainObject.ObjectID 
            self.createObjectTree(self.attrList, self.currMainObject)
            
    def createObjectTree(self, attributeList, currParentObject): 
        for objAttrMap in attributeList:
            currParentObject=self.createTreeObject(currParentObject, objAttrMap)
            
    def createTreeObject(self,currParentObject=None, objAttrMap=None): 
        if objAttrMap==None:
            objAttrMap={} 
            y=self.manualTreeVals.grid_size()[1] 
            for i in range(0,y-5):
                objAttrMap[(self.manualTreeVals.grid_slaves(i,0)[0]).cget('text')]=(self.manualTreeVals.grid_slaves(i,1)[0]).get() 
            displayname=objAttrMap[ 'Display Name'] 
            if currParentObject==None:
                self.ParentID='' 
                self.objectId=objAttrMap[ 'Display Name'] 
                currObject=TreePOMObject(objectaction='newobject', attributeDict=objAttrMap, displayname=displayname, objecttype=objAttrMap['Object Type']) 
            else:
                self.ParentID=currParentObject.ObjectID 
                self.objectId=self.ParentID+'_'+displayname 
                currObject=TreePOMObject(objectaction='newobject', attributeDict=objAttrMap, objectid=self.objectId, parentid=self.ParentID, displayname= displayname, objecttype=objAttrMap['Object Type'])
        else:
            displayname=objAttrMap['Display Name'] 
            self.objectId=currParentObject.ObjectID+ '_'+displayname 
            currObject=TreePOMObject(objectaction='newobject', attributeDict=objAttrMap,objectid=self.objectId, parentid=self.ParentID, displayname=displayname) 
        self.objectDict[self.objectId]=currObject 
        if currParentObject!=None and (currParentObject.ObjectType=='POM_Page' or currParentObject.ObjectType=='POM_frame' or currParentObject.ObjectType=='POM_iframe'): 
            currParentObject.childList.append(currObject) 
            self.ParentID=currParentObject.ObjectID
        currObject.addTree(self.objTree, objectid=self.objectId, displayname=currObject.DisplayName, parentid=self.ParentID)

        Util.focusTree(self.objTree, currObject.ObjectID)
        
    def getObjectDict(self):
        return self.objectDict
    
    def updateObjectDict(self,propertyValues, key):
        currObject=self.objectDict[key] 
        displayName=(propertyValues.grid_slaves(0,1)[0]).get() 
        self.updateParentObjectId(currObject, key,displayName) 
        self.objTree.item(key, text=displayName) 
        y=propertyValues.grid_size()[1]
        currObject.propertyList.clear() 
        for i in range(0,y-1):
            if (propertyValues.grid_slaves(i,0)[0]).cget('text')!='Display Name':
                oProperty=Property()
                oProperty.propertyName=(propertyValues.grid_slaves(i,0)[0]).cget( 'text') 
                oProperty.Value=(propertyValues.grid_slaves(i,1)[0]).get() 
                print ((propertyValues.grid_slaves(i,0)[0]).cget('text'))
                #if (propertyValues.grid_slaves(i,0)[0]).cget('text')!='Display Name':
                oProperty.Selected=(propertyValues.grid_slaves(i,0)[0]).is_selected.get() 
                currObject.propertyList.append(oProperty)
                
    def updateParentObjectId(self, currObject, key, displayName):
        objectKey=key 
        updatedObjectId=None 
        while len(self.objTree.parent(key))>0:
            updatedObjectId=displayName if updatedObjectId==None else self.objTree.item(key)[ 'text']+'_'+updatedObjectId
            key=self.objTree.parent(key) 
        updatedObjectId=key+'_'+updatedObjectId if updatedObjectId!=None else displayName 
        currObject.ParentID=updatedObjectId.split('_'+displayName)[0] if updatedObjectId!=displayName else '' 
        currObject.ObjectID=updatedObjectId 
        currObject.DisplayName=displayName
        self.objectDict[updatedObjectId]=self.objectDict[objectKey] 
        print ('new parent id='+currObject.ParentID+' updated object key='+updatedObjectId) 
        for key,val in self.objectDict.items(): 
            if self.objectDict[key].ParentID==objectKey:
                self.objectDict[key].ParentID=updatedObjectId 
                self.objectDict[key].ObjectID=updatedObjectId+'_'+self.objectDict[key].DisplayName 
                self.objectDict[updatedObjectId+'_'+self.objectDict[key].DisplayName]=self.objectDict[key]


