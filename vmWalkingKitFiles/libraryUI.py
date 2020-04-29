from maya import cmds
from collections import OrderedDict

# This is not done like this when shipping the tool.
# Watch from 5:30 of video 57
import walkLibrary
reload(walkLibrary)  # TODO: delete this when shipping.

# TODO: Substitute 'PySide2' with 'Qt' when shipping the tool.
# This is only for developing purposes
from Qt import QtWidgets, QtCore, QtGui
from functools import partial
import Qt
import logging
from maya import OpenMayaUI as omui

# Setting up logger
logger = logging.getLogger('WalkLibraryUI')
logger.setLevel(logging.DEBUG) # TODO: change to logging.INFO when shipping
logging.basicConfig()

# This makes sure that all import statements work regardless of what Python library it's been used for Qt

if Qt.__binding__ == 'PySide': # If we are using PySide
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
elif Qt.__binding__.startswith('PyQt'): # If we are using PyQt4 or PyQt5
    logger.debug('Using PyQt with sip')
    from sip import wrapInstance as wrapInstance
else: # If we are using PySide2 (Maya 2017 and above)
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance


class WalkLibraryUI(QtWidgets.QWidget):
    """
    The WalkLibraryUI is a dialog that lets us control all the walkTool parameters.
    """

    # Saving initial BodyBeat and ArmsBeat indices for adapting others parameters accordingly
    prevBodyIndex = 2
    prevArmsIndex = 2

    def __init__(self, dock=True):

        # Delete UI if it already exists
        try:
            cmds.deleteUI('walktool')
        except:
            logger.debug('No previous UI exists.')

        # If dock mode is queried the parent will be the docked window
        # If not, the parent will be the main Maya window
        # TODO: explain this dock(bool) option in the documentation of the tool
        if dock:
            parent = getWindowDock()
        else:
            deleteWindowDock()
            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('walktool')
            parent.setWindowTitle('vmWalkingKit')
            layout = QtWidgets.QVBoxLayout(parent)

        # Now that our parent is set we can initialize it
        super(WalkLibraryUI, self).__init__(parent=parent)

        # Set default size of the window
        self.resize(400, 350)

        # The Library variable points to an instance of our controller library
        self.library = walkLibrary.WalkLibrary()

        # Dropdown options list
        self.frameOptions = ["8f", "12f", "16f"]
        self.rangeOptions = ["Low", "Mid", "High"]
        self.handOptions = ["Relaxed", "Fist"]
        self.faceOptions = ["Happy", "Angry", "Sad", "Cocky", "Scared"]
        self.paramWidgets = OrderedDict()

        # Prefixes
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt", "HeadUpDown", "HeadPigeon",
                         "HeadEgoist", "HeadNodding", "HeadTilt", "FaceExpression", "BackCurvature",
                         "PelvisYRotation", "PelvisWeightShift", "ChestYRotation", "ChestUpDown",
                         "ArmsWidth", "ElbowsDrag", "HandsDrag", "HandsPose"]

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()
        self.onReset()

        # Add ourself (QtWidgets.QWidget) to the parent's layout
        self.parent().layout().addWidget(self)

        # If docked mode is off, directly show our parent
        if not dock:
            parent.show()

    def initParamLayersData(self):
        """
        Initializes all the data structures needed for controlling animation layers and parameters.
        """

        # Get the names and weights of all the animation layers in the scene
        layersNames, layersWeights = self.library.getCurrentAnimationLayers()
        print layersNames
        # Create ordered dictionaries to store the parameters data

        # TODO: automate this below
        # BodyBeat
        bodyBeatDict = OrderedDict()
        bodyBeatDict[layersNames[0]] = layersWeights[0]
        bodyBeatDict[layersNames[1]] = layersWeights[1]
        bodyBeatDict[layersNames[2]] = layersWeights[2]

        # ArmsBeat
        armsBeatDict = OrderedDict()
        armsBeatDict[layersNames[3]] = layersWeights[3]
        armsBeatDict[layersNames[4]] = layersWeights[4]
        armsBeatDict[layersNames[5]] = layersWeights[5]

        # UpDown
        upDownDict = OrderedDict()
        upDownDict[layersNames[6]] = layersWeights[6]

        # BodyTilt
        bodyTiltDict = OrderedDict()
        bodyTiltDict[layersNames[7]] = layersWeights[7]

        # HeadUpDown
        headUpDownDict = OrderedDict()
        headUpDownDict[layersNames[8]] = layersWeights[8]

        # HeadPigeon
        headPigeonDict = OrderedDict()
        headPigeonDict[layersNames[9]] = layersWeights[9]

        # HeadEgoist
        headEgoistDict = OrderedDict()
        headEgoistDict[layersNames[10]] = layersWeights[10]

        # HeadNodding
        headNoddingDict = OrderedDict()
        headNoddingDict[layersNames[11]] = layersWeights[11]

        # HeadNodding
        headTiltDict = OrderedDict()
        headTiltDict[layersNames[12]] = layersWeights[12]

        # FaceExpression
        faceExpressionDict = OrderedDict()
        faceExpressionDict[layersNames[13]] = layersWeights[13]
        faceExpressionDict[layersNames[14]] = layersWeights[14]
        faceExpressionDict[layersNames[15]] = layersWeights[15]
        faceExpressionDict[layersNames[16]] = layersWeights[16]
        faceExpressionDict[layersNames[17]] = layersWeights[17]

        # BackCurvature
        backCurvatureDict = OrderedDict()
        backCurvatureDict[layersNames[18]] = layersWeights[18]

        # PelvisYRotation
        pelvisYRotationDict = OrderedDict()
        pelvisYRotationDict[layersNames[19]] = layersWeights[19]

        # PelvisWeightShift
        pelvisWeightShiftDict = OrderedDict()
        pelvisWeightShiftDict[layersNames[20]] = layersWeights[20]

        # ChestYRotation
        chestYRotationDict = OrderedDict()
        chestYRotationDict[layersNames[21]] = layersWeights[21]

        # ChestUpDown
        chestUpDownDict = OrderedDict()
        chestUpDownDict[layersNames[22]] = layersWeights[22]

        # ArmsWidth
        armsWidthDict = OrderedDict()
        armsWidthDict[layersNames[23]] = layersWeights[23]

        # ElbowsDrag
        elbowsDragDict = OrderedDict()
        elbowsDragDict[layersNames[24]] = layersWeights[24]

        # HandsDrag
        handsDragDict = OrderedDict()
        handsDragDict[layersNames[25]] = layersWeights[25]

        # HandsPose
        handsPoseDict = OrderedDict()
        handsPoseDict[layersNames[26]] = layersWeights[26]
        handsPoseDict[layersNames[27]] = layersWeights[27]

        # Create main data list with all the layers information sorted by parameter

        self.paramLayers = OrderedDict([
            (self.prefixes[0],  bodyBeatDict),
            (self.prefixes[1],  armsBeatDict),
            (self.prefixes[2],  upDownDict),
            (self.prefixes[3],  bodyTiltDict),
            (self.prefixes[4],  headUpDownDict),
            (self.prefixes[5],  headPigeonDict),
            (self.prefixes[6],  headEgoistDict),
            (self.prefixes[7],  headNoddingDict),
            (self.prefixes[8],  headTiltDict),
            (self.prefixes[9],  faceExpressionDict),
            (self.prefixes[10], backCurvatureDict),
            (self.prefixes[11], pelvisYRotationDict),
            (self.prefixes[12], pelvisWeightShiftDict),
            (self.prefixes[13], chestYRotationDict),
            (self.prefixes[14], chestUpDownDict),
            (self.prefixes[15], armsWidthDict),
            (self.prefixes[16], elbowsDragDict),
            (self.prefixes[17], handsDragDict),
            (self.prefixes[18], handsPoseDict)
        ])

    # UI METHODS

    # UI creation methods

    def createUI(self):
        """This method creates the UI"""

        # This is the master layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create menu bar
        self.createMenuBar()

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setUsesScrollButtons(True)
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.createGeneralTab()
        self.createHeadTab()
        self.createTrunkTab()
        self.createArmsTab()
        self.createLegsTab()
        self.createSettingsTab()

        # Create bottom buttons
        self.createBottomBtns()

    def createMenuBar(self):
        """
        Creates the top menu bar.
        """

        # Creates the menu bar widges and add it to the master layout
        menubar = QtWidgets.QMenuBar()
        self.layout.addWidget(menubar)

        # Add the main menu options
        actionFile = menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

    def createGeneralTab(self):
        """
        Creates the general tab.
        """

        # Add general tab
        tabGeneral = self.addTab("General")

        # Create General tab parameters
        self.addDropDownParam(tabGeneral, "Body beat", self.frameOptions, 0, self.prefixes[0], "onDropDownBodyBeatChanged")
        self.addDropDownParam(tabGeneral, "Arms beat", self.frameOptions, 1, self.prefixes[1], "onDropDownArmsBeatChanged")
        self.addSliderParam(tabGeneral, "Up & Down", 2, self.prefixes[2], "onSliderChanged")
        self.addSliderParam(tabGeneral, "Body Tilt", 3, self.prefixes[3], "onSliderChanged")

    def createHeadTab(self):
        """
        Creates the head tab
        """

        # Add tab for the head
        tabHead = self.addTab("Head")

        # Create Head tab parameters
        self.addSliderParam(tabHead, "Head up-down", 0, self.prefixes[4], "onSliderChanged")
        self.addSliderParam(tabHead, "Head pigeon", 1, self.prefixes[5], "onSliderChanged")
        self.addSliderParam(tabHead, "Head egoist", 2, self.prefixes[6], "onSliderChanged")
        self.addSliderParam(tabHead, "Head nodding", 3, self.prefixes[7], "onSliderChanged")
        self.addSliderParam(tabHead, "Head tilt", 4, self.prefixes[8], "onSliderChanged", 500)
        self.addDropDownParam(tabHead, "Facial expression", self.faceOptions, 5, self.prefixes[9], "onDropDownChanged")

    def createTrunkTab(self):
        """
        Creates the trunk tab
        """

        # Add tab for the trunk
        tabTrunk = self.addTab("Trunk")

        # TODO: do a ++i for the ui IDs

        # Create Trunk tab parameters
        self.addSliderParam(tabTrunk, "Back curvature", 0, self.prefixes[10], "onSliderChanged", 500)
        self.addSliderParam(tabTrunk, "Pelvis Y-rotation", 1, self.prefixes[11], "onSliderChanged")
        self.addSliderParam(tabTrunk, "Pelvis weight shift", 2, self.prefixes[12], "onSliderChanged")
        self.addSliderParam(tabTrunk, "Chest Y-rotation", 3, self.prefixes[13], "onSliderChanged")
        self.addSliderParam(tabTrunk, "Chest up-down", 4, self.prefixes[14], "onSliderChanged")

    def createArmsTab(self):
        """
        Creates the arms tab
        """

        # Add tab for the arms
        tabArms = self.addTab("Arms")

        # Create Arms tab parameters
        self.addSliderParam(tabArms, "Arms swing", 0, self.prefixes[1], "onSliderChanged", 500)
        self.addSliderParam(tabArms, "Arms separation", 1, self.prefixes[15], "onSliderChanged", 500)
        self.addSliderParam(tabArms, "Elbows drag", 2, self.prefixes[16], "onSliderChanged", 500)
        self.addSliderParam(tabArms, "Hands drag", 3, self.prefixes[17], "onSliderChanged", 500)
        self.addDropDownParam(tabArms, "Hands pose", self.handOptions, 4, self.prefixes[18], "onDropDownChanged")

    def createLegsTab(self):
        """
        Creates the legs tab
        """

        # Add tab for the legs
        tabLegs = self.addTab("Legs")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createSettingsTab(self):
        """
        Creates the settings tab
        """

        # Add tab for the head
        tabSettings = self.addTab("Settings")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createBottomBtns(self):
        """
        Creates the bottom buttons.
        """

        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        self.layout.addWidget(btnWidget)

        # Create buttons, connect them to a slot and add them to our btnLayout

        # Save button
        saveBtn = QtWidgets.QPushButton('Save preset')
        # saveBtn.clicked.connect(self.onSave)
        btnLayout.addWidget(saveBtn)

        # Read button
        importBtn = QtWidgets.QPushButton('Import preset')
        #importBtn.clicked.connect(self.onImport)
        btnLayout.addWidget(importBtn)

        # Reset
        resetBtn = QtWidgets.QPushButton('Reset')
        resetBtn.clicked.connect(self.onReset)
        btnLayout.addWidget(resetBtn)

    # UI functionality methods

    def addTab(self, tabName):
        """
        Creates a tab with the given name.
        Args:
            tabName(str): name of the tab to create.

        Returns:
            newTab(QtWidgets.QWidget): a reference to the new created tab.
        """

        # Create a new tab and add it to the QTabWidget
        newTab = QtWidgets.QWidget()
        self.tabs.addTab(newTab, tabName)

        # Set a QGridLayout for the new tab
        newTab.layout = QtWidgets.QGridLayout(newTab)
        newTab.layout.setContentsMargins(4, 4, 4, 4)
        newTab.setLayout(newTab.layout)

        # Create the scroll widget that will contain all the parameters of this new tab
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        # Set the scroll layout
        self.scrollLayout = QtWidgets.QGridLayout(scrollWidget)

        # Create the scroll area to add the new tab
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        newTab.layout.addWidget(scrollArea, 1, 0, 5, 5)

        return newTab

    def addDropDownParam(self, tab, paramName, options, id, prefix, slotName=None):

        widget = QtWidgets.QComboBox()
        for i in range(0, len(options)):
            widget.addItem(options[i])

        widget.setCurrentIndex(1)  # TODO: not hardcode this? Maybe read from JSON default preset file

        if prefix == 'BodyBeat' or prefix == 'ArmsBeat':
            widget.currentIndexChanged.connect(partial(getattr(self, slotName)))
        else:
            widget.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id)

    def addSliderParam(self, tab, paramName, id, prefix, slotName=None, defaultValue=200):

        widget = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        widget.setMinimum(0)
        widget.setMaximum(1000)
        widget.setValue(defaultValue)
        widget.valueChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id)

    def setUpParamWidget(self, prefix, widget, paramName, id):

        if prefix == self.prefixes[1] and self.prefixes[1] not in self.paramWidgets:
            self.paramWidgets[prefix] = [widget, None]
        elif prefix == self.prefixes[1] and self.prefixes[1] in self.paramWidgets:
            self.paramWidgets[prefix][1] = widget
        else:
            self.paramWidgets[prefix] = widget

        # Set parameter layout
        paramText = QtWidgets.QLabel(paramName)

        self.scrollLayout.addWidget(paramText, id, 0, 1, 3)
        paramText.setMinimumHeight(25)
        self.scrollLayout.addWidget(QtWidgets.QLabel(" "), id, 3, 1, 1)
        self.scrollLayout.addWidget(widget, id, 4, 1, 3)

    # SLOT METHODS

    def onDropDownChanged(self, prefix, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly.

        Args:
            prefix:(string): prefix of the layer associated with this parameter.
            index (int): index of the current selected option in the dropdown
        """

        # Convert the index into a string and inside a [1-3] range to match the animation layer naming convention
        indStr = str(index + 1)

        # Change animation layers mute state according to the current index
        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)

                if self.prefixes[1] in layerName:
                    self.library.changeLayerWeight(layerName, 0.5)
                    currWeight = self.paramLayers[prefix][layerName]
                    self.paramWidgets[prefix][1].setValue(currWeight*1000.0)
            else:
               self.library.changeLayerMuteState(layerName, True)

        # Retrieve the current BodyBeat and ArmsBeat indices by iterating the current active layers and
        # checking for the unmuted ones
        activeLayers, weights = self.library.getActiveAnimationLayers()
        indices = []

        for i in range(0, len(activeLayers)):

            # Once we got both indices we break out of the for loop
            if len(indices) == 2:
                break

            # Split layer name into prefix and index
            splitStr = activeLayers[i].split("_")

            # If we find 'BodyBeat' or 'ArmsBeat' we store their indices
            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

        # Calculate the playback range according to the current indices retrieved above. Body and arms beat dictate
        # the length of the whole walk cycle animation. This allows for a minimum playback time while always allowing
        # the animation to be looped properly.
        self.library.calculatePlaybackRange(indices)

    def onDropDownBodyBeatChanged(self, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of the
        UpDown_1 layer in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the dropdown
        """

        prefix = 'BodyBeat'

        # Convert the index into a string and inside a [1-3] range to match the animation layer naming convention
        indStr = str(index + 1)

        # Change animation layers mute state according to the current index
        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        # Retrieve the current BodyBeat and ArmsBeat indices by iterating the current active layers and
        # checking for the unmuted ones
        indices = []
        activeLayers, weights = self.library.getActiveAnimationLayers()

        for i in range(0, len(activeLayers)):

            # Once we got both indices we break out of the for loop
            if len(indices) == 2:
                break

            # Split layer name into prefix and index
            splitStr = activeLayers[i].split("_")

            # If we find 'BodyBeat' or 'ArmsBeat' we store their indices
            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

        # Calculate the playback range according to the current indices retrieved above. Body and arms beat dictate
        # the length of the whole walk cycle animation. This allows for a minimum playback time while always allowing
        # the animation to be looped properly.
        self.library.calculatePlaybackRange(indices)

        # Query the current BodyBeat index
        currBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

        if currBodyIndex is not None:
            # Create the ty attribute of the controller that handles the up and down body movement
            attrGeneralUpDown = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateY'
            self.library.offsetKeyframes(attrGeneralUpDown, 'UpDown_1', self.prevBodyIndex, currBodyIndex)

            attrPelvisYRotation = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.rotateY'
            self.library.offsetKeyframes(attrPelvisYRotation, 'PelvisYRotation_1',  self.prevBodyIndex, currBodyIndex)

            attrPelvisWeightShift = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateX'
            self.library.offsetKeyframes(attrPelvisWeightShift, 'PelvisWeightShift_1', self.prevBodyIndex, currBodyIndex)

            attrHeadPigeon = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateZ'
            self.library.offsetKeyframes(attrHeadPigeon, 'HeadPigeon_1',  self.prevBodyIndex, currBodyIndex)

            attrHeadUpDown = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateY'
            self.library.offsetKeyframes(attrHeadUpDown, 'HeadUpDown_1',  self.prevBodyIndex, currBodyIndex)

            attrheadEgoist = 'Mr_Buttons:Mr_Buttons_Neck_01FKCtrl.rotateZ'
            self.library.offsetKeyframes(attrheadEgoist, 'HeadEgoist_1',  self.prevBodyIndex, currBodyIndex)

            attrHeadNodding = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.library.offsetKeyframes(attrHeadNodding, 'HeadNodding_1',  self.prevBodyIndex, currBodyIndex)

            attrHeadTilt = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.library.offsetKeyframes(attrHeadTilt, 'HeadTilt_1',  self.prevBodyIndex, currBodyIndex)

            attrChestUpDown = 'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.translateY'
            self.library.offsetKeyframes(attrChestUpDown, 'ChestUpDown_1',  self.prevBodyIndex, currBodyIndex)

            attrChestYRotation = 'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.rotateY'
            self.library.offsetKeyframes(attrChestYRotation, 'ChestYRotation_1',  self.prevBodyIndex, currBodyIndex)

        # Store the previous BodyBeat index for the next calculation
        WalkLibraryUI.prevBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

    def onDropDownArmsBeatChanged(self, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of the
        UpDown_1 layer in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the dropdown
        """

        prefix = 'ArmsBeat'

        # Convert the index into a string and inside a [1-3] range to match the animation layer naming convention
        indStr = str(index + 1)

        # Change animation layers mute state according to the current index
        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        # Retrieve the current BodyBeat and ArmsBeat indices by iterating the current active layers and
        # checking for the unmuted ones
        indices = []
        activeLayers, weights = self.library.getActiveAnimationLayers()

        for i in range(0, len(activeLayers)):

            # Once we got both indices we break out of the for loop
            if len(indices) == 2:
                break

            # Split layer name into prefix and index
            splitStr = activeLayers[i].split("_")

            # If we find 'BodyBeat' or 'ArmsBeat' we store their indices
            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

        # Calculate the playback range according to the current indices retrieved above. Body and arms beat dictate
        # the length of the whole walk cycle animation. This allows for a minimum playback time while always allowing
        # the animation to be looped properly.
        self.library.calculatePlaybackRange(indices)

        # Query the current ArmsBeat index
        currArmsIndex = self.paramWidgets[prefix][0].currentIndex() + 1

        if currArmsIndex is not None:
            attrElbowsDragRight = 'Mr_Buttons:Mr_Buttons_r_Arm_ElbowFKCtrl.rotateY'
            self.library.offsetKeyframes(attrElbowsDragRight, 'ElbowsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrElbowsDragLeft = 'Mr_Buttons:Mr_Buttons_l_Arm_ElbowFKCtrl.rotateY'
            self.library.offsetKeyframes(attrElbowsDragLeft, 'ElbowsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrHandsDragRight = 'Mr_Buttons:Mr_Buttons_r_Arm_WristFKCtrl.rotateY'
            self.library.offsetKeyframes(attrHandsDragRight, 'HandsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrHandsDragLeft = 'Mr_Buttons:Mr_Buttons_l_Arm_WristFKCtrl.rotateY'
            self.library.offsetKeyframes(attrHandsDragLeft, 'HandsDrag_1', self.prevArmsIndex, currArmsIndex)

        # Store the previous ArmsBeat index for the next calculation
        WalkLibraryUI.prevArmsIndex = self.paramWidgets[prefix][0].currentIndex() + 1

    def onSliderChanged(self, prefix, value):
        """
        Calculates the normalized slider value and applies it to the layer's weight
        Args:
            prefix(str): prefix of the layer associated with the slider
            value(float): current value of the slider
        """

        currIndex = 0

        if prefix == self.prefixes[1]:
            currIndex = self.paramWidgets[prefix][0].currentIndex()

        layerName = list(self.paramLayers[prefix].keys())[currIndex]
        weight = value / 1000.0
        self.library.changeLayerWeight(layerName, weight)

    def onSave(self, name=None, directory=None):
        """
        Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.
        Args:
            name(str): name of the preset file to import.
            directory(str): directory where the preset file to import is stored
        """

        if name is None and directory is None:
            self.library.savePreset()
        elif name is not None and directory is None:
            self.library.savePreset(name)
        elif name is not None and directory is not None:
            self.library.savePreset(name, directory)
        else:
            logger.debug("If a directory is given a name must be given as well.")

    def onReset(self):
        """
        Resets the tool parameters to their default state.
        """

        # Import the default preset and query the layer names and weights
        defaultLayers, defaultWeights = self.library.importPreset()

        # TODO: make this a method of wallkLibrary
        # Set default playback options
        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=24)
        cmds.playbackOptions(animationStartTime=1)

        # For each parameter apply the default layers data to the parameter
        if defaultLayers is not None and defaultWeights is not None:
            for i in range(0, len(defaultLayers)):

                # Get layer prefix
                splitStr = defaultLayers[i].split("_")
                prefix = splitStr[0]
                # Get the widget type

                if prefix == self.prefixes[1]:
                    index = int(splitStr[1]) - 1
                    self.paramWidgets[prefix][0].setCurrentIndex(index)
                    self.onDropDownChanged(prefix, index)

                    self.paramWidgets[prefix][1].setValue(defaultWeights[i]*1000.0)
                    self.onSliderChanged(prefix, defaultWeights[i]*1000.0)
                elif prefix != "Corrective":
                    widgetType = type(self.paramWidgets[prefix]).__name__

                    # Set the current index or change the slider value accordingly
                    if widgetType == 'QComboBox':
                        index = int(splitStr[1]) - 1
                        self.paramWidgets[prefix].setCurrentIndex(index)
                        if prefix == self.prefixes[0]:
                            self.onDropDownBodyBeatChanged(index)
                        else:
                            self.onDropDownChanged(prefix, index)
                    elif widgetType == 'QSlider':
                        self.paramWidgets[prefix].setValue(defaultWeights[i]*1000.0)
                        self.onSliderChanged(prefix, defaultWeights[i]*1000.0)
        else:
            logger.debug("Query for default preset file failed.")

    def onImport(self, name=None, directory=None):
        """
        Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.
        Args:
            name(str): name of the preset file to import.
            directory(str): directory where the preset file to import is stored
        """

        if name is None and directory is None:
            self.library.importPreset()
        elif name is not None and directory is None:
            self.library.importPreset(name)
        elif name is not None and directory is not None:
            self.library.importPreset(name, directory)
        else:
            logger.debug("If a directory is given a name must be given as well.")

# MAYA WINDOWS FUNCTIONS

def getMayaMainWindow():
    """
    Get the main Maya windows (which is also built with Qt).

    Returns:
        ptr(QtWidgets.QMainWindow): The Maya MainWindow
    """

    # With OpenMayaUI API we query a reference to Maya's MainWindow
    win = omui.MQtUtil_mainWindow()

    # We cast the queried window to QMainWindow so it's manageable within our Python code
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)

    return ptr

def getWindowDock(name='WalkToolWinDock'):
    """
    Create dock with the given name.
    Args:
        name(str): name of the dock to create.

    Returns:
        ptr(QtWidget.QWidget): The dock's widget
    """

    # Delete older dock
    deleteWindowDock(name)

    # Create a dock and query its name
    ctrl = cmds.workspaceControl(name, tabToControl=('AttributeEditor', 2), label='vmWalkingKit', vis=True)

    # Query the correspondent QtWidget associated with the dock
    qtCtrl = omui.MQtUtil_findControl(name)

    # We cast the queried window to QWidget so it's manageable within our Python code
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    return ptr

def deleteWindowDock(name='WalkToolWinDock'):
    """
    Deletes the given dock if this exists.
    Args:
        name(str): name of the window to delete
    """

    if cmds.workspaceControl(name, exists=True):
        cmds.deleteUI(name)


# Call it in Maya's Script Editor
#from vmWalkingKit.vmWalkingKitFiles import libraryUI
#reload(libraryUI)

#libraryUI.WalkLibraryUI()
