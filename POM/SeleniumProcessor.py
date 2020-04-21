from selenium import webdriver
from selenium.common import exceptions as SelException
from lxml import html
from lxml.etree import XPathEvalError
import selenium.common.exceptions as SeleniumException
from tkinter import messagebox

class SeleniumDriver: 
    def __init__(self, config, browserName=None):
        self.config=config
        self.browser_navigation_panel_height=None
        self.root=None
        self.strBrowser=None 
        self.currDriver=None
        self.listAttr=[] 
        self.driver=None
        self.objWebElement=None
        if browserName !=None:
            self.driver=browserName
    
    
    def LaunchBrowser(self, browserName, url):
        try:
            if len(url)>3:
                self.driver=browserName
                self.driver.maximize_window() 
                self.driver.get(url)
                self.browser_navigation_panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
            else:
                if self.driver !=None:
                    self.driver.quit()
                messagebox.showinfo('Browser not launched', 'URL not Given.\n Please make sure URL is present in URL Text box.')
        except SeleniumException.InvalidArgumentException:
                messagebox.showinfo('Invalid URL', 'Invalid URL. \nPlease make sure URL is correct.') 
    @property
    def driver(self):
        return self.currDriver
    
    @driver.setter 
    def driver(self, browserType): 
        try: 
            if 'Chrome' ==browserType:
                self.strBrowser='Chrome' 
                options = webdriver.ChromeOptions() 
                options.add_argument('--ignore-certificate-errors') 
                options.add_argument("--test-type")
                self.currDriver = webdriver.Chrome(self.config.configuration[ 'Driver']['Chrome_Driver'], chrome_options=options) 
            if 'IE'==browserType:
                self.currDriver=webdriver.Ie(self.config.configuration['Driver']['ie_driver']) 
        except SeleniumException.WebDriverException as e:
            messagebox.showinfo('WebDriverException',e)
            
    @property 
    def browser(self):
        return self.strBrowser 
    @browser.setter 
    def browser(self, strBrowser):
        print('driver set as : chrome')
        self.strBrowser=strBrowser 
    @property 
    def attributeList(self):
        return self.listAttr 
    @attributeList.setter 
    def attributeList(self, attrList):
        self.listAttr=attrList 
    def webElement(self):
        return self.objWebElement

    def set_webElement(self, coordinates, ScreenCoverWindow=None):
        try:
            self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles)-1]) 
            attrsList=[] 
            pageAttrsDict={}
            frameAttrsDict={} 
            pageAttrsDict['Display Name']=self.driver.title 
            pageAttrsDict['title']=self.driver.title 
            pageAttrsDict['tabindex']=len(self.driver.window_handles) - 1 
            attrsList.append(pageAttrsDict) 
            x,y=coordinates 
            self.objWebElement=self.driver.execute_script('return document.elementFromPoint('+str(x)+', '+str(y-self.browser_navigation_panel_height)+ ');') 
            while self.objWebElement !=None and self.objWebElement.tag_name=='iframe' or self.objWebElement.tag_name=='frame':
                frameXLoc=self.objWebElement.location['x'] 
                frameYLoc=self.objWebElement.location['y'] 
                frameAttrsDict['Display Name']=self.objWebElement.get_attribute('name') 
                frameAttrsDict['name']=self.objWebElement.get_attribute('name') 
                frameAttrsDict['id']=self.objWebElement.get_attribute('id') 
                frameAttrsDict['tag']=self.objWebElement.tag_name 
                attrsList.append(frameAttrsDict) 
                if self.objWebElement.get_attribute('id')!=None:
                    identifyText=self.objWebElement.get_attribute('id') 
                elif self.objWebElement.get_attribute('name')!=None:
                    identifyText=self.objWebElement.get_attribute('name') 
                    self.driver.switch_to.frame(identifyText) 
                    self.objWebElement=self.driver.execute_script('return document.elementFromPoint('+str(x-frameXLoc)+ ', '+str(y-self.browser_navigation_panel_height-frameYLoc)+');') 
            attrsList.append(self.getAttributes()) 
            if len(self.objWebElement.find_elements_by_xpath('.//*'))>0:
                for obj in self.objWebElement.find_elements_by_xpath('.//*'):
                    self.objWebElement=obj
                    attrsList.append(self.getAttributes())
            self.attributeList=attrsList 
            print (attrsList, sep='\n' ) 
            if ScreenCoverWindow !=None :
                ScreenCoverWindow.destroy()
        except SelException.UnexpectedAlertPresentException: 
            if ScreenCoverWindow==None:
                ScreenCoverWindow.destroy()
                messagebox.showinfo('ALERT PRESENT', 'Alert present on the current Window. \nif you want to add object: Please close ale')

    
    
    def getAttributes(self):
        WebObjectAttrsDict={}
        WebObject=self.objWebElement 
        tag=WebObject.tag_name 
        if WebObject.get_attribute('id')!=None and len(WebObject.get_attribute('id'))>1:
            WebObjectAttrsDict['Display Name']=WebObject.get_attribute('id') 
        elif WebObject.get_attribute('name')!=None and len(WebObject.get_attribute('name'))>1:
            WebObjectAttrsDict['Display Name']=WebObject.get_attribute('name') 
        else:
            WebObjectAttrsDict['Display Name']=tag+'_'+WebObject.get_attribute('innerHTML')[:10] 
        xpath='.//'+tag+'[' 
        print(WebObject.get_property('attributes')) 
        for attr in WebObject.get_property('attributes'):
            WebObjectAttrsDict[attr['name']]= attr['value']
            xpath=xpath+'@'+attr['name']+'=\"'+attr['value']+'\' and '
            xpath = xpath[:-4]+']'
            XMLroot = html.fromstring(self.driver.page_source) 
            XMLtree = XMLroot.getroottree() 
        try:
            result=XMLtree.xpath(xpath)
            WebObjectAttrsDict['XPath'] =XMLtree.getpath(result[0]) 
        except XPathEvalError:
            WebObjectAttrsDict['XPath']='NA'
    
        if WebObject.get_attribute('innerHTML')!=None:
            WebObjectAttrsDict['innerHTML']=WebObject.get_attribute('innerHTML') 
        if WebObject.text !=None:
            WebObjectAttrsDict['text']=WebObject.text 
            WebObjectAttrsDict['tag']=tag
        return WebObjectAttrsDict


