## SeleniumPOM
Tool to create Object Repository for Selenium projects

[PreRequisite to execute this project](./PreRequisite.md)

* ### Guide to Use Selenium POM
Once you have cloned the project. Run Object Model file in your IDE

1. [Create New Page Object Model](#Create-new-Page-Object-Model)  
2. [Add Object from WebPage](#Add-Object-from-WebPage)

#### Create new Page Object Model:
*   Click on File-->Create New POM..  
![CreateNewFile](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/CreateNewFile.jpg)  

*   Provide POM name and click on save  
![SaveNewFile](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/CreateNewFileSave.jpg)  

*   New POM file will be displayed as header  
![NewFileCreated](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/CreatedNewFile.jpg)  

### Add Object from WebPage:
1. Launch URL: Provide URL in Enter Base URL text box and select browser to launch from dropdown  
   *(Note : Make sure that you have provided driver path in settings)*
  ![Launch URL](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/LaunchURL.jpg) 

2. Click on Launch Button: it will launch the URL in the specified browser
    ![URL Launched](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/URLOpened.jpg)
   
3. Click on Add Object button and click on Web Object you want to add: This will get the details of all the attributes related to the object and displays it in new window.  
Left side of screen will diaplay object and its parent.
If a object has multiple frames than it will display the complete Heirarchy.
Heirarchy will always start from Page and ends at webobject, it will also include any Frame in between.
Right side of screen will display properties of the selected object from left side tree.
    ![Add New Object Click](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/AddNewObjectClick.jpg)  
    ![Click WebObject](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/ClickOnWebObject.jpg)

4. 
