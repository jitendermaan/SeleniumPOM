'''
Created on Feb 16, 2020

@author: maan
'''
from tkinter import Toplevel 
import os 
import configparser 
import Util 
from tkinter import Tk 

import tkinter as Tkinter
import tkinter.ttk as ttk 
from tkinter import filedialog, Frame, Label, Entry, LabelFrame

class Setting:
    def __init__(self,root=None):
        self.CONFIG_PATH=os.path.abspath('../Resources/Settings.ini') 
        self.root=root 
        self.config=None 
        self.configDict={} 
        self.configuration=self.CONFIG_PATH 
        self.settingWindow=None
    
    def displaySettingPanel(self):
        self.settingWindow=Toplevel() 
        self.settingWindow.geometry("600x400") 
        self.settingWindow.attributes('-topmost', True) 
        self.settingWindow. title("Settings") 
        self.settingWindow.grid_columnconfigure(0, weight=1) 
        self.displayDriverSettings() 
        buttonFrame=Frame(self.settingWindow) 
        buttonFrame.grid(row=1, column=0) 
        ttk.Button(buttonFrame, text= 'Save', command=self.saveConfig).grid(row=1,column=0, pady=20, padx=20) 
        ttk.Button(buttonFrame, text= 'Cancel', command=self.settingWindow.destroy).grid(row=1,column=1, pady=20, padx=20)
        
    def displayDriverSettings (self):
        SettingFrame=LabelFrame(self.settingWindow, text= 'Driver Settings ') 
        SettingFrame.grid(column=0, row=0, padx=5, pady=5, sticky= 'nsew') 
        SettingFrame.grid_columnconfigure(1, weight=1)
        chromePathVar=Tkinter.StringVar() 
        chromePathVar.trace( 'w',lambda name, index, mode, sv=chromePathVar: self.updateConfigFromEntry(sv, 'chrome_driver'))
        IEPathVar=Tkinter.StringVar() 
        IEPathVar.trace('w',lambda name, index, mode, sv=IEPathVar: self.updateConfigFromEntry(sv,'ie_driver'))
        FFPathVar=Tkinter.StringVar() 
        FFPathVar.trace('w',lambda name, index, mode, sv=FFPathVar: self.updateConfigFromEntry(sv, 'firefox_driver'))
        
        Label(SettingFrame, text= 'Chrome Driver ').grid(column=0, row=0, sticky= '', padx=5, pady=5) 
        ChromeDriverPath = Entry(SettingFrame, textvariable=chromePathVar) 
        ChromeDriverPath.grid(row=0, column=1, padx=5, sticky= 'we',pady=5 ) 
        ChromeDriverPath.insert(0, self.config['Driver']['chrome_driver']) 
        ChromebrowseButton=ttk.Button(SettingFrame, text= 'Browse', command= lambda: self.getDriverPath(ChromeDriverPath)) 
        ChromebrowseButton.grid(row=0, column=2, padx=5, pady=5)
        
        Label(SettingFrame, text='IE Driver'). grid(column=0, row=1, sticky= 'we', padx=5, pady=5) 
        IEDriverPath = Entry(SettingFrame, textvariable=IEPathVar) 
        IEDriverPath.grid(row=1, column=1, padx=5, sticky='we', pady=5) 
        IEDriverPath.insert(0, self.config[ 'Driver']['ie_driver']) 
        IEbrowseButton=ttk.Button(SettingFrame, text= 'Browser', command= lambda: self.getDriverPath(IEDriverPath)) 
        IEbrowseButton.grid(row=1, column=2, padx=5, pady=5)
        Label(SettingFrame, text='Firefox Driver').grid(column=0, row=2, sticky='we', padx=5, pady=5) 
        FireFoxDriverPath = Entry(SettingFrame, textvariable=FFPathVar) 
        FireFoxDriverPath.grid(row=2, column=1, padx=5, sticky="we", pady=5) 
        FireFoxDriverPath.insert(0,self.config['Driver']['firefox_driver'])
        FireFoxbrowseButton=ttk.Button (SettingFrame, text="Browse", command= lambda: self.getDriverPath(FireFoxDriverPath)) 
        FireFoxbrowseButton.grid(row=2, column=2, padx=5,pady=5)
        
    def updateConfigFromEntry(self, sv, key):
        self.config.set( 'Driver',key,sv.get())
        
    def getDriverPath(self, pathEntry):
        self.settingWindow.attributes('-topmost',False) 
        filePath = filedialog.askopenfilename() 
        pathEntry.delete(0, 'end') 
        pathEntry.insert(0, filePath) 
        self.settingWindow.attributes('-topmost',True)
        
    def saveConfig(self):
        cfgfile = open(self.CONFIG_PATH, 'w') 
        self.config.write(cfgfile) 
        cfgfile.close() 
        self.settingWindow.destroy()
        
    @property 
    def configuration(self):
        return self.config 
    @configuration.setter 
    def configuration(self,configPath):
        config = configparser.ConfigParser() 
        config.read(configPath) 
        self.config= config
        
    def addConfig(self, section, key, value): 
        if not self.config.has_section(section):
            self.config.add_section(section) 
        self.config.set(section, key, value) 
        cfgfile = open(self.CONFIG_PATH, 'w') 
        self.config.write(cfgfile) 
        cfgfile.close()

        
