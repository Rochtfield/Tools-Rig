# -*- coding: utf-8 -*-

import maya.cmds as cmds
import math
import maya.api.OpenMaya as om
from Skeleton import Create_Skeleton

def clic_buton_Skeleton(*args):
    """Function to create skeleton."""
    Create_Skeleton()

def Skeleton_Parameters_UI():
    """Creates a UI window for creating Skeleton."""
    
    # Name of the window to ensure that there is only one
    window_name = "Skeleton Creator"
    if cmds.window(window_name, exists=True):
       cmds.deleteUI(window_name, window=True)

    window = cmds.window(window_name, title="Skeleton Creator", widthHeight=(100, 150), sizeable=True)

    # Create the main layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    # Button Skeleton
    cmds.button(label="Create Skeleton", command=clic_buton_Skeleton, parent=main_layout)

    # displays the window
    cmds.showWindow(window)

