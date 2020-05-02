# vmWalkingKit
 
In this README you’ll find all the steps needed in order to make the vmWalkingKit work inside Maya. The steps are the following ones: 

1. Download the latest release .zip from the release section of the repository (https://github.com/nintervik/vmWalkingKit/releases) and unzip it anywhere on your computer.
2. Inside, you’ll find four things:
   a. A folder called vmWalkingKit. 
   b. A script called Qt.py
   c. This README file
   d. A LICENSE file
Move a. and b. (the folder and the .py script) to the next directory:    
C:\Users\UserName\Documents\maya\version\scripts
Where:
   - C: is the drive where Windows is installed.
   - UserName is the name of your user in Windows
   - version is the version number of Maya that you want to use (2017→2019)
3. Open the Maya version corresponding to where you’ve put the files.
4. Go to File→Set Project and navigate to the vmWalkingKitFolder. Inside you’ll find another folder called mayaProject. Set that folder as the project. 
5. In Maya, go to File→Open Scene (Ctrl+O) and open the characterScene_# where # is the Maya version you’re using.
6. Open the Script Editor by clicking on the bottom right button with the {;} or by going to Windows→General Editors→Script Editor.
7. Click on the + icon on the tabs section to open up a new tab. Choose Python as the executer source language.
8. In this tab, paste the following code:     

from vmWalkingKit.vmWalkingKitFiles import libraryUI

reload(libraryUI)

libraryUI.WalkLibraryUI()

9. Open the Custom tab in Maya’s Shelf. If the the Shelf is not visible, go to Windows→UI Elements→Shelf.  
10. Still with the this tab opened and inside the Script Editor, go to File→Save Script To Shelf…, write a name for it (e.g. vmWalkingKit) and click Ok. An icon with the chosen name should have appeared in the Custom Shelf tab.
11. Now, you can click on that icon once and the tool will be opened. You can customize the window size or dock it anywhere. And that’s it. You can start playing around with the tool. Have fun! 
