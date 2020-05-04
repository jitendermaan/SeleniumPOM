## SeleniumPOM
Tool to create Object Repository for Selenium projects

This projet is created to simplify and standardize the way we are using Page Object Model or Object Repository in Selenium. As we know in selenium does not provide any native Object repository manager as we have in other paid automation tools like UFT or RFT.  
Indeed we can use different approach to create and manage Page Objects in Selenium like:  
1. Page Object Model (Using Class\Object)
2. Excel sheet (Adding Object Property to Excel and read it while execution)
3. XML file (Adding Object Properties in XML format)
or any you can save object attributes in flat file or any other type of files.

In all the above approach there are few common issues that can surface while creating Object Repository:
1. #### Adding Object
   1. We have to find Object Property in Chrome and add it manually to the Object Repository file
   2. Adding multiple attribute for a object is even more cumbersome. It is not easy to remove or add a single attribute for identifying Object
2. #### Standard Approach
   1. When multiple team members are working on the same project, it is possible that someone uses different approach to add obejct attributes which might not in line with the defined standards
3. #### Managing Objects
   1. As the size of Objects and pages increased it is becoming more dificult to handle the objects. Finding an object itself is a daunting task in large collection of pages. 
   2. Modifying\Adding new objects becomes more dificult with increase in size of Object Repository.

We thought that it can considerably reduce the Object identification and Object Management hassles and efforts if we have a UI based tool that can address all the above issues.

SeleniumPOM tool is created to overcome all the obove issues:
1. #### Adding Object : This tool makes it quick and hassle free to add new object with multiple properties and you can select a single property or a group of properties to identify object
   1. We can add object directly by clicking on the object on browser, this will fetch all the properties of the object and you can select which property to use by selecting the checkbox
   2. Delay Add: We can add drop down menu items or other objects just by using delay add feature. It will wait for 5 second and then add the object under cursor
   3. Add object manually: We can add Objects, their hierarchy and properties manually also, In case it can not be identifiied by tool or if it is a non GUI Object
   
2. #### Standard Approach: This tool has defined XML pattern which consists of Page-->Frame(if it is present)-->Object heirarchy to manage objects. All Heirarchies have there own properties for identifications

3. #### Managing Objects: This tool represents the Object collection XML in an interactive GUI application where you can add new object, modify objects with just one click, add\remove or update object properties.
   1. This tool makes it easier to read the Object Repository. It represents all the pages and its object as a tree structure and you can easily select the object to view its properties.
   2. It is easier to edit or add object properties with just few clicks
   3. XML file can be easily shared with the team
   



[PreRequisite to execute this project](./PreRequisite.md)

* ### Guide to Use Selenium POM
Once you have cloned the project. Run Object Model file in your IDE

1. [Create New Page Object Model](#Create-new-Page-Object-Model)  
2. [Add Object from WebPage](#Add-Object-from-WebPage)
3. [Add Object with Delay](#Add-Object-with-Delay)
4. [Add Object Manually](#Add-Object-Manually)


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

4. Update Object Property: If you want to update anhy property or display name for the object then update property directly on the window and click on update button.This will update object property beofre adding it to POM Repository.  
Ex: in below example, i have updated the display name of the img_ to img_NewDisplayName  
![Click WebObject](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/ClickOnWebObject.jpg)
![Update Object](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/UpdateNewAddedObjectProperties.jpg)

5. Click on Add Object: This will add the object in POM Repository.
![Update Object](https://github.com/jitendermaan/SeleniumPOM-Executable/blob/master/images/ObjectAdded.jpg)

### Add Object with Delay
It is helpful when you have to select any dropdown or any other object that will disappear when focus is moved from that object. like Dropdown Menu items. This will wait for 5 seconds and add the object based on mouse pointer location. Please make sure that cursor is on the object that you want to add.

1. Launch browser using the tool and Click on Add object with Delay:   
It will start a 5 sec counter on top left of your screen. Before that timer hits to 0 move your mouse pointer to the object you want to add.
