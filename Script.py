# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math
import maya.api.OpenMaya as om
from Joint_Bend import Target_Joints, Insert_Joints
from Deformers_Joint import DeformersJoint
from Mirror import MirrorJoints
import ControllerParameters
import UI_Skeleton

# --- define button ---
def clic_bouton_Skeleton(*args):
    """Function to create skeleton."""
    UI_Skeleton.Skeleton_Parameters_UI()

def clic_Button_JointBend(*args):
    """
    Main function to insert joints between two selected joints.
    It displays a dialog window to ask for the number of joints.
    """
    Target_Joints()
    Insert_Joints()

def clic_bouton_DeformersJoint(*args):
    """Function for the main button deformersJoint."""
    DeformersJoint()

def clic_Button_MirrorJoint(*args):
    """for MirrorJoint"""
    MirrorJoints()

def clic_Buton_ControlerParam(*args):
    """Creates a UI window for creating controllers with shape options."""
    
    ControllerParameters.Controller_Parameters_UI()


# --- Main function for UI ---
def create_main_window():
    """Create the main window with buttons and a drop-down menu."""
    
    # Destroy the old window if it exists
    window_name = "Window"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    
    # Create window
    window = cmds.window(window_name, title="Mutaux Arthur", widthHeight=(250, 150))
    
    # Create layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    
    # Add elements on interface
    cmds.text(label="control Pannel", parent=main_layout)
    
    # Button Skeleton
    cmds.button(label="Skeleton", command=clic_bouton_Skeleton, parent=main_layout)
    
    # Button Bend Joint
    cmds.button(label="Bend Joints", command=clic_Button_JointBend, parent=main_layout)
    
    # Button Derformers muscles joint
    cmds.button(label="Deformers Joints", command=clic_bouton_DeformersJoint, parent=main_layout)

    # Button Mirror Joint
    cmds.button(label="Mirror Joints", command=clic_Button_MirrorJoint, parent=main_layout)

    # Dopdown Menu
    cmds.text(label="Select Controlers :", parent=main_layout)
    
    cmds.button(label="Controler Params", command=clic_Buton_ControlerParam, parent=main_layout)

    # displays the window
    cmds.showWindow(window)

# --- Call The function for create interface ---
create_main_window()