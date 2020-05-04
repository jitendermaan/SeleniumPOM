import POM.XMLProcessor as XMLProcessor
import POM.TreeProcessor as TreeProcessor 
import POM.SeleniumProcessor as SeleniumProcessor
import POM.Util as Util 
import POM.Settings as ST 
#===============================================================================
# from lxml.etree import XPathEvalError
#===============================================================================
import pyautogui as PYAUTO
import time

import tkinter as Tkinter
import tkinter.ttk as ttk
from tkinter import filedialog, Scrollbar, TclError, Menu, mainloop, Label, messagebox, Frame, Entry,Toplevel,StringVar, Tk, Canvas
from tkinter.filedialog import asksaveasfile
from tkinter import Checkbutton

class myApp: 
    def __init__(self):
        self.root = Tk()
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 11),background="green")
        self.config=ST.Setting(self.root)
        self.SelDriver=SeleniumProcessor.SeleniumDriver(self.config)
        self.POMTreeView=TreeProcessor.POMTree(self.config) 
        self.XML=XMLProcessor.XML() 
        self.treeFrame=None 
        self.tree=None 
        self.treeValues=None 
        self.ScreenCoverWindow=None 
        self.root.title("POM Manager") 
        self.root.geometry('700x600')
#MENU SECTION : to create Menu
# File Menu 
        menu = Menu(self.root) 
        self.root.config(menu=menu) 
        filemenu = Menu(menu) 
        menu.add_cascade (label="File", menu=filemenu) 
        filemenu.add_command(label="Create New POM..", command=self.NewFile) 
        filemenu.add_command(label="Open POM...", command=self.OpenFile) 
        filemenu.add_command(label="Save POM...", command=self.SaveFile) 
        filemenu.add_command(label="Save as POM...", command=self.SaveFileAs) 
        filemenu.add_separator() 
        filemenu.add_command(label="Exit", command=self.root.destroy)
        
        toolmenu = Menu(menu) 
        menu.add_cascade(label="Tool", menu=toolmenu) 
        toolmenu.add_command(label="Settings", command=self.Settings)

        helpmenu = Menu(menu) 
        menu.add_cascade(label="Help", menu=helpmenu) 
        helpmenu.add_command(label="About...", command=self.About)
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.grid_rowconfigure(1, weight=1) 
        top = ttk.Frame(self.root,height=200)
        
        top.grid_columnconfigure(1, weight=1) 
        top.grid(column=0, row=0, pady=10, sticky='nsew') 
        bottom=ttk.Frame(self.root) 
        bottom.grid(column=0, row=1, sticky='nsew') 
        bottom.grid_columnconfigure(0, weight=1, uniform="group1") 
        bottom.grid_columnconfigure(1, weight=1, uniform="group1") 
        bottom.grid_rowconfigure(0, weight=1)
        
        footer = ttk.Frame (bottom, height=120)
        Label(top, text='Enter Base URL :').grid(column=0, row=0) 
        self.txtURL =Entry(top)
        self.txtURL.grid(column=1, row=0, sticky='we')
        browserCombo=ttk.Combobox(top, values=['Chrome', 'IE','Edge', 'FireFox'], state='readonly') 
        browserCombo.set('Chrome') 
        browserCombo.grid(column=2, row=0, padx=5) 
        self.Launchbtn = ttk.Button(top, text="Launch",command=lambda : self.SelDriver.LaunchBrowser(browserCombo.get(),self.txtURL.get()))
        self.Launchbtn.grid(column=1, row=1, pady=5)
        self.root.bind("<Control-s>", lambda event: self.XML.saveXML(self.POMTreeView)) 
        self.AddNewObjectButton=ttk.Button(footer, text='Add New Object ', command= lambda: self.enable_mouseposition()) 
        self.AddNewObjectButton.grid(column=0, row=1, padx=5, pady=20)
        self.ManuallyAddobject= ttk.Button(footer, text='Add Object Manually',command= lambda: self.addobjectPropertiesManually()) 
        self.ManuallyAddobject.grid(column=2, row=1, padx=5, pady=20)
        self.savebutton=ttk.Button(footer, text='Save', command=lambda: self.XML.saveXML( self.tree, self.POMTreeView)) 
        self.savebutton.grid(column=3, row=1, padx=5, pady=20)
        self.AddToPageButton=ttk.Button(footer, text='Add With Delay' , command=lambda: self.getDelayCoordinates()) 
        self.AddToPageButton.grid(column=1, row=1, padx=5, pady=20)
        
        self.CancelButton=ttk.Button(footer, text='Cancel', command=self.root.destroy) 
        self.CancelButton.grid(column=4, row=1, padx=5, pady=20) 
        self.treeFrame=Frame (bottom, borderwidth=1, relief="solid") 
        self.treeValues=Frame (bottom, borderwidth=1, relief="solid") 
        self.treeFrame.grid_rowconfigure(0, weight=1) 
        self.treeFrame.grid_columnconfigure(0, weight=1) 
        self.treeFrame.grid(row=0, column=0, sticky='nsew') 
        self.treeValues.grid(row=0, column=1, sticky='nsew')
        
        bottom.grid_rowconfigure(0, weight=1) 
        footer.grid(column=0, row=1, columnspan=2) 
        mainloop()
        try:
            self.SelDriver.quit() 
        except AttributeError:
            None

    def NewFile(self):
        files = [('ORFile', '*.xml.')] 
        file =asksaveasfile(title = "Select folder", filetypes = files, defaultextension = files) 
        self.XML.filePath=file.name 
        self.XML.fileName=((file.name).split('/')[-1]).split('.')[0] 
        self.createPOMTree ('newfile')

    def OpenFile(self):
        filePath = filedialog.askopenfilename() 
        if len(filePath) >4:
            self.XML=XMLProcessor.XML(filePath) 
            if self.tree!=None:
                self.tree.destroy() 
            self.createPOMTree() 
            self.AddToPageButton[ 'state'] ='normal'
            
    def About (self):
        print ('This is a simple example of a menu!')

    def SaveFile(self):
        self.XML.saveXML(self.tree,self.POMTreeView)

    def SaveFileAs(self):
        self.XML.saveXML(self.tree,self.POMTreeView,'newfile')
        #=======================================================================
        # self.tree.heading('#0', text=self.XML.fileName)
        #=======================================================================
    def Settings(self):
        self.config.displaySettingPanel()
        
    def cancelAddObject(self, topWindow):
        topWindow.destroy()

    def getDelayCoordinates(self):
        try:
            self.root.iconify() 
            top = Toplevel() 
            top.geometry("+%d+%d"%(0,0)) 
            top.title("Counter") 
            top.attributes('-alpha',0.5)
            v = Tkinter.IntVar() 
            ttk.Label(top, text="**hover mouse to the object you want to add", font=('Arial' ,8)).pack()
            text = ttk.Label(top, textvariable = v) 
            text.config(font=( "Courier", 50)) 
            text.pack() 
            for i in range(5,-1,-1):
                v.set(i) 
                text.update()
                time.sleep(1) 
            top.destroy() 
            self.SelDriver.set_webElement(PYAUTO.position())
            self.createAttributePanel('delayadd')
        except AttributeError:
            messagebox.showinfo( 'Driver Not Initiated', 'Driver is not initiated.\nPlease make sure browser is Launched using tool.')

    def enable_mouseposition(self, actionType=None):
        try:
            driver=self.SelDriver.driver 
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
            self.root.after(100, self.get_WebObject(actionType)) 
        except AttributeError: 
            Tkinter.messagebox.showinfo('Driver Not Initiated','Driver is not initiated. \nPlease make sure browser is launched using tool.')
            
    def get_WebObject(self, actionType):
        self.ScreenCoverWindow=Toplevel()
        self.root.iconify()
        self.ScreenCoverWindow.attributes('-topmost', True) 
        self.ScreenCoverWindow.title("Object Properties") 
        self.ScreenCoverWindow.attributes('-alpha', 0.2) 
        self.ScreenCoverWindow.attributes("-fullscreen", True) 
        self.ScreenCoverWindow.focus_force() 
        self.ScreenCoverWindow.bind("<Button-1>", lambda event: self.createAttributePanel(actionType, event))
        
        
    def createAttributePanel(self,actionType=None, event=None): 
        if actionType !='delayadd':
            self.SelDriver.set_webElement((event.x, event.y),self.ScreenCoverWindow)
        attributePanelWindow=Toplevel()
        attributePanelWindow.geometry("600x500") 
        attributePanelWindow.attributes( '-topmost', True) 
        attributePanelWindow.title("Object Properties") 
        attributePanelWindow.grid_columnconfigure(0, weight=1) 
        attributePanelWindow.grid_rowconfigure(0, weight=1)
        top=ttk.Frame(attributePanelWindow) 
        top.grid(column=0, row=0, sticky='nsew') 
        top.grid_columnconfigure(0, weight=1, uniform="group1") 
        top.grid_columnconfigure(1,weight=1, uniform="group1") 
        top.grid_rowconfigure(0, weight=1)
        self.attributeTreeFrame=Frame(top, borderwidth=1, relief="solid") 
        self.attributetreeValues=Frame(top, borderwidth=1,relief='solid') 
        self.attributeTreeFrame.grid_rowconfigure(0, weight=1) 
        self.attributeTreeFrame.grid_columnconfigure(0, weight=1) 
        self.attributeTreeFrame.grid(row=0, column=0, sticky='nsew') 
        self.attributetreeValues.grid(row=0, column=1, sticky="nsew")
        footer =ttk.Frame (top, height=120) 
        footer.grid(column=0, row=1,columnspan=2) 
        ttk.Button(footer, text='Cancel' , command=attributePanelWindow.destroy).grid(column=2, row=1, padx=5, pady=10) 
        ttk.Button(footer, text='Add Object',command= lambda : self.updatePOMTree(attributePanelWindow,self.ObjectPropertyTree.getObjectDict())).grid(column=1,row=1, padx=5, pady=10)
        self.createAttributeTree (self.SelDriver.attributeList, actionType)
            
    def createAttributeTree(self, attrsList, processType=None):
        self.attributeTree=ttk.Treeview(self.attributeTreeFrame) 
        self.yscrollbar = Util.AutoScrollbar(self.attributeTreeFrame, orient='vertical', command=self.attributeTree.yview) 
        self.attributeTree.configure(yscrollcommand=self.yscrollbar.set) 
        self.attributeTree.grid(row=0, column=0, sticky='nsew') 
        self.yscrollbar.grid(row=0, column=1, sticky='ns') 
        self.ObjectPropertyTree=TreeProcessor.ObjectPropertyTree(self.attributeTree,attrsList,processtype=processType) 
        self.attributeTree.bind( "<<TreeviewSelect>>", lambda event: self.displayProperties(self.attributetreeValues, self.ObjectPropertyTree.getObjectDict()))


    def displayProperties(self, attributes, newObjectTreeDict, actiontype=None):
        propertyNum=0 
        for widget in attributes.winfo_children():
            widget.destroy() 
        currentItem=self.attributeTree.focus() 
        currObject=newObjectTreeDict[currentItem] 
        attributes.grid_columnconfigure(1,weight=1) 
        ttk.Label(attributes, text='Display Name', justify='left').grid(column=0, row=0, padx=5, pady=1, sticky='w') 
        DefaultVal = StringVar(attributes,value=currObject.DisplayName) 
        Entry(attributes, textvariable=DefaultVal).grid(column=1, row=0, padx=5, pady=1, sticky='we', columnspan=1)
        
        for oProperty in currObject.propertyList:
            isPropSelected=oProperty.Selected 
            isUsed = Tkinter.IntVar() 
            propertyCheckButton=ttk.Checkbutton(attributes, text=oProperty.propertyName, variable=isUsed) 
            propertyCheckButton.is_selected=isUsed 
            propertyCheckButton.grid(column=0, row=propertyNum+1, padx=5, pady=1, sticky='w') 
            DefaultVal = StringVar(attributes, value=oProperty.Value) 
            PropertyVal=Entry(attributes, textvariable=DefaultVal) 
            PropertyVal.grid(column=1, row=propertyNum+1, padx=5, pady=1, sticky='we', columnspan=2) 
            if isPropSelected=='1' or isPropSelected==1:
                propertyCheckButton.var=isUsed 
                propertyCheckButton.var.set(1)
            else:    
                propertyCheckButton.var=isUsed
                propertyCheckButton.var.set(0) 
            propertyNum=propertyNum+1 
        UpdateButton=ttk.Button(attributes, text='Update') 
        UpdateButton.grid(column=1, row=propertyNum+1, padx=10, pady=20,sticky='w')
        
        if actiontype=='manual':
            AddChildButton=ttk.Button(attributes, text='Add child Object ') 
            AddChildButton['command' ]=lambda : self.AddChildToAttributeTree() 
            AddChildButton.grid(column=0, row=propertyNum+1, padx=10, pady=20,sticky='w')
            UpdateButton ['command']=lambda : self.UpdateProperties(self.scrollable_frame,currentItem)
        else:
            UpdateButton['command']=lambda : self.UpdateProperties(self.attributetreeValues,currentItem)

    def UpdateProperties(self,treeVal,key):
        self.ObjectPropertyTree.updateObjectDict(treeVal,key)
        
    def updatePOMTree(self,propertyWindow, objDict, actionType=None):
        currItem=self.attributeTree.focus() 
        objectToAdd=objDict[currItem] 
        currObject=objectToAdd
        addToObject='' 
        objList=[currObject.ObjectID] 
        if self.tree==None:
            self.createPOMTree()
        propertyWindow.attributes('-topmost', False)
        if self.tree.exists(currObject.ObjectID):
            messagebox.showinfo( 'Object Present with ID: ='+currObject.ObjectID,'Object Present with ID: '+currObject.ObjectID+ '. \nPlease Change the Name or Update object Directly from Attribute Window' )
        else:
            self.POMTreeView.treeDict[currObject.ObjectID]=currObject 
            while currObject.ParentID!=None and len(currObject.ParentID)>0: 
                if self.tree.exists(currObject.ParentID):
                    addToObject=currObject.ParentID
                    break 
                else:
                    currObject=objDict[currObject.ParentID] 
                    self.POMTreeView.treeDict[currObject.ObjectID]=currObject 
                    objList.insert(0,currObject.ObjectID)
        
        for childtree in objList:
            childObj=objDict[childtree] 
            self.tree.insert(addToObject, 'end', iid=childObj.ObjectID, text=childObj.DisplayName) 
            addToObject=childObj.ObjectID
        propertyWindow.destroy() 
        Util.focusTree(self.tree,objectToAdd.ObjectID)
        print ('Object to Focus :'+currObject.ObjectID)
        
    def AddChildToAttributeTree(self): 
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy() 
        self.addObjectIndentificationFields(self.attributeTree,self.scrollable_frame,'child')
        
    def addobjectPropertiesManually(self):
        self.attributePanelWindow =Toplevel() 
        self.attributePanelWindow.geometry("600x500") 
        self.attributePanelWindow.attributes( '-topmost', True)
        self.attributePanelWindow.title("Object Properties")
        self.attributePanelWindow.grid_columnconfigure(0, weight=1) 
        self.attributePanelWindow.grid_rowconfigure(0, weight=1) 
        top=ttk.Frame(self.attributePanelWindow) 
        top.grid(column=0, row=0, sticky='nsew')
        top.grid_columnconfigure(0,weight=1, uniform="group1") 
        top.grid_columnconfigure(1, weight=1, uniform="group1") 
        top.grid_rowconfigure(0, weight=1)
        self.attributeTreeFrame=Frame(top, borderwidth=1, relief="solid") 
        self.attributetreeValues=Frame (top, borderwidth=1, relief="solid") 
        self.attributeTreeFrame.grid_rowconfigure(0, weight=1) 
        self.attributeTreeFrame.grid_columnconfigure(0, weight=1) 
        self.attributeTreeFrame.grid(row=0, column=0, sticky='nsew') 
        self.attributetreeValues.grid_rowconfigure(0, weight=1) 
        self.attributetreeValues.grid_columnconfigure(0, weight=1) 
        self.attributetreeValues.grid(row=0, column=1, sticky='nsew') 
        self.scrollable_frame=Util.ScrollableFrame(self.attributetreeValues, 'both')
        
        self.attributeTree=ttk.Treeview(self.attributeTreeFrame) 
        self.attributeTree.grid(row=0, column=0, sticky="nsew")
        self.attributeTree.bind("<<TreeviewSelect>>", lambda event: self.displayProperties(self.scrollable_frame, self.ObjectPropertyTree.getObjectDict(), 'manual'))
        footer = ttk.Frame (top, height=120) 
        footer.grid(column=0, row=1, columnspan=2) 
        ttk.Button(footer, text='Cancel', command=self.attributePanelWindow.destroy).grid(column=0, row=1, padx=5, pady=10)
        ttk.Button(footer, text='Add Object', command= lambda : self.updatePOMTree(self.attributePanelWindow, self.ObjectPropertyTree.getObjectDict())).grid(column=1, row=1, padx=5, pady=10)
        self.addObjectIndentificationFields(self.attributeTree, self.scrollable_frame)
        
    def addObjectIndentificationFields (self, objTree,Scrollableframe, objtype=None):
        objectTypeList=[ 'POM_Page'] if len(objTree.get_children())==0 else [ 'POM_frame', 'POM_Object'] 
        ttk.Label(Scrollableframe, text='Object Type', justify='left').grid(column=0, row=0, padx=5, sticky='w') 
        ObjectTypeCombo=ttk.Combobox(Scrollableframe, values=objectTypeList, state='readonly') 
        ObjectTypeCombo.grid(column=1, row=0, sticky='we') 
        ttk.Label(Scrollableframe, text='Display Name', justify="left").grid(column=0, row=1, padx=5, sticky='w') 
        comboExample = ttk.Combobox(Scrollableframe, values=[]) 
        comboExample.grid(column=1, row=1, sticky='we') 
        ObjectTypeCombo.bind("<<ComboboxSelected>>", lambda event: self.getObjectList(Scrollableframe, ObjectTypeCombo, comboExample)) 
        self.addPropertywidget(Scrollableframe, 2,objtype)
    
    def getObjectList(self,Scrollableframe, ObjectTypeCombo, comboExample):
        listObjectName=[] 
        if ObjectTypeCombo.get()=='POM_Page': 
            if self.tree!=None : 
                for child in self.tree.get_children():
                    listObjectName.append(child) 
            comboExample['values']= listObjectName

    def addPropertywidget(self, propertyWindow, addPropRow, objtype=None):
        ttk.Label(propertyWindow, text='  ', justify='left').grid(column=0, row=addPropRow, padx=5, sticky='w')
        ttk.Label(propertyWindow, text='Property Name:', justify='left').grid(column=0, row=addPropRow+1, padx=5,sticky='w') 
        PropertyType=Entry(propertyWindow) 
        PropertyType.grid(column=1, row=addPropRow+1, sticky='we')
        ttk.Label(propertyWindow, text='Property Value:' , justify='left').grid(column=0, row=addPropRow+2, padx=5, sticky='w') 
        PropertyValue=Entry(propertyWindow) 
        PropertyValue.grid(column=1, row=addPropRow+2, sticky='we')
        AddPropButton=ttk.Button(propertyWindow, text='Add Property.. ') 
        AddPropButton.grid(row=addPropRow+3, column=0, padx=5, pady=5, sticky='e')
        AddPropButton['command']= lambda: self.addAttribute (propertyWindow, addPropRow, objtype) 
        buttonFrame=Frame(propertyWindow) 
        buttonFrame.grid(column=0, row=addPropRow+4, columnspan=2) 
        if objtype=='child': 
            ttk.Button(buttonFrame, text='Add to Tree', command= lambda : self.AddManualobjectToTree(propertyWindow,objtype)).grid(column=0, row=0, padx=5, pady=20)
        else:
            ttk.Button(buttonFrame, text='Add to Tree', command=lambda : self.AddManualobjectToTree(propertyWindow)).grid(column=0, row=0, padx=5, pady=20)
        cancelbutton=ttk.Button(buttonFrame, text='Cancel ', command=lambda : self.refreshAddManualobjectPanel())
        cancelbutton.grid(column=1, row=0, padx=5, pady=20)

    def refreshAddManualobjectPanel(self): 
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        if len(self.attributeTree.get_children())>0:
            currItem=self.attributeTree.focus()
            Util.focusTree(self.attributeTree, currItem) 
        else:
            self.addObjectIndentificationFields(self.attributeTree, self.scrollable_frame)

    def addAttribute(self, propertyWindow, addProp, objtype=None):
        PropertyName=(propertyWindow.grid_slaves(addProp+1,1)[0]).get()
        PropertyVal=(propertyWindow.grid_slaves(addProp+2,1)[0]).get() 
        v = Tkinter.IntVar() 
        for i in range(addProp,addProp+5): 
            for w in propertyWindow.grid_slaves(row=i):
                w.grid_forget()

        c=Checkbutton(propertyWindow,text=PropertyName, variable=v) 
        c.grid(column=0, row=addProp, padx=5, sticky='w') 
        c.is_selected=v 
        DefaultVal = StringVar(self.root, value=PropertyVal) 
        Entry(propertyWindow, textvariable=DefaultVal).grid(column=1, row=addProp, sticky='we') 
        self.addPropertywidget(propertyWindow, addProp+1, objtype)
        
    def AddManualobjectToTree(self,treeManual,objtype=None):
        if (treeManual.grid_slaves(0,1)[0]).get()==''or (treeManual.grid_slaves(0,1)[0]).get()==None or (treeManual.grid_slaves(1,1)[0]).get()=='' or (treeManual.grid_slaves(1,1)[0]).get()==None:
            messagebox.showinfo('Object Not Created', 'Please provide Object Name and at least one property to add object.' )
        else:
            if objtype=='child':
                currentItem=self.attributeTree.focus() 
                currParentObj=self.ObjectPropertyTree.objectDict[currentItem] 
                currObj=self.ObjectPropertyTree.createTreeObject(currParentObj)[1]
            else:
                self.ObjectPropertyTree=TreeProcessor.ObjectPropertyTree(self.attributeTree, treevals=treeManual) 
                currObj=self.ObjectPropertyTree.createTreeObject()[1]
            Util.focusTree(self.attributeTree, currObj.ObjectID)
    def createPOMTree (self, processType=None): 
        if self.tree!=None:
            self.tree.destroy() 
        self.tree=Util.scrollableTree(self.treeFrame, 'both') 
        self.tree.heading( '#0', anchor='w') 
        self.tree.grid(row=0, column=0, sticky="nsew") 
        if self.POMTreeView==None: 
            print( 'IT IS NULL') 
        self.POMTreeView.setTree(self.tree) 
        if self.XML.filePath!=None:
            self.POMTreeView.createTree(self.XML, self.tree, processType)
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.displayObjectProperties(event))


    def displayObjectProperties(self, currentItem=None):
        propertyNum=1 
        for widget in self.treeValues.winfo_children():
            widget.destroy()
        self.currentItem=self.tree.focus() 
        self.POMTreeView.ORObject=self.currentItem 
        currObject=self.POMTreeView.ORObject 
        ttk.Label(self.treeValues, text='Display Name', justify='left').grid(column=0, row=0, padx=5, sticky='w') 
        DefaultVal = StringVar(self.treeValues, value=currObject.DisplayName) 
        Entry(self.treeValues, textvariable=DefaultVal, state='readonly').grid(column=1, row=0, sticky='we', columnspan=2)
        ttk.Label(self.treeValues, text='Object ID', justify='left').grid(column=0, row=propertyNum, padx=5, sticky='w') 
        DefaultVal = StringVar(self.treeValues, value=currObject.ObjectID) 
        Entry(self.treeValues, textvariable=DefaultVal, state='readonly').grid(column=1, row=propertyNum, sticky='we', columnspan=2)
        self.treeValues.grid_columnconfigure(1, weight=1)
        for oProperty in currObject.propertyList:
            isPropSelected=oProperty.Selected 
            isUsed = Tkinter.IntVar() 
            propertyCheckButton=ttk.Checkbutton(self.treeValues, text=oProperty.propertyName, variable=isUsed, state='disabled') 
            propertyCheckButton.is_selected=isUsed 
            propertyCheckButton.grid(column=0, row=propertyNum+1, padx=5, sticky='w') 
            DefaultVal = StringVar(self.treeValues, value=oProperty.Value)
            PropertyVal=Entry(self.treeValues, textvariable=DefaultVal, state='readonly')
            PropertyVal.grid(column=1, row=propertyNum+1, sticky='we', columnspan=2) 
            if isPropSelected=='1' or isPropSelected==1:
                propertyCheckButton.var=isUsed 
                propertyCheckButton.var.set(1)
            else:
                propertyCheckButton.var=isUsed
                propertyCheckButton.var.set(0) 
            propertyNum=propertyNum+1
        EditButton=ttk.Button(self.treeValues, text=' Edit ') 
        EditButton['command']=lambda : self.editProperties(EditButton,propertyNum+1) 
        EditButton.grid(column=1, row=propertyNum+1, padx=10, pady=20,sticky='w')
    
    def editProperties (self, EditButton, propertyNum):
        EditButton['text']='Update' 
        EditButton.grid(column=2) 
        ttk.Button(self.treeValues, text='Add Custom Property', command=lambda : self.addCutomProperty()).grid(column=1, row=propertyNum, pady=20,sticky='w') 
        for widget in self.treeValues.winfo_children():
            widget['state']='normal' 
        self.treeValues.grid_slaves(1,1)[0]['state']='readonly' 
        self.isPropertySaved=False 
        EditButton['command']=lambda : self.updateObjectProperty(EditButton)

    def addCutomProperty(self):
        addPropRow=0 
        customAttributeWindow = Toplevel() 
        customAttributeWindow.geometry("300x100") 
        customAttributeWindow.attributes("-topmost", True) 
        customAttributeWindow.title( "Add Property") 
        customAttributeWindow.grid_columnconfigure(1, weight=1) 
        ttk.Label(customAttributeWindow, text='Property Name:', justify='left').grid(column=0, row=addPropRow, padx=5, pady=5, sticky='w') 
        PropertyType=Entry(customAttributeWindow) 
        PropertyType.grid(column=1, row=addPropRow, sticky='we')
        ttk.Label(customAttributeWindow, text='Property Value:' , justify='left').grid(column=0, row=addPropRow+1, padx=5, pady=5, sticky='w') 
        PropertyValue=Entry(customAttributeWindow) 
        PropertyValue.grid(column=1, row=addPropRow+1, sticky='we')
    
        AddPropButton=ttk.Button(customAttributeWindow, text='Add Property')
        AddPropButton.grid(row=addPropRow+2, column=1, padx=5, pady=10, sticky='w')
        currentItem=self.tree.focus() 
        AddPropButton['command']=lambda :self.POMTreeView.addProperty(self.tree, currentItem, customAttributeWindow)
        
    def updateObjectProperty(self, actionType=None):
        currObj=self.POMTreeView.updateObjectProperty(self.tree, self.treeValues, self.currentItem) 
        self.currentItem=currObj.ObjectID 
        Util.focusTree(self.tree, currObj.ObjectID) 
        self.displayObjectProperties()
myApp()
