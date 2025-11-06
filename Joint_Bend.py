# -*- coding: utf-8 -*-
import maya.cmds as cmds
import math
import maya.api.OpenMaya as om

def Target_Joints():
    # get joints
    selected_joints = cmds.ls(selection=True, type='joint')
    
    # check if two joint selected
    if len(selected_joints) != 2:
        cmds.warning("Please select exactly two joints for this operation.")
        return
        
    start_joint_name = selected_joints[0]
    end_joint_name = selected_joints[1]
    
    # Show a Window for ask how many joint you want
    result = cmds.promptDialog(
        title="Insert Joints",
        message="Numbers of joints :",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel"
    )

    if result == "OK":
        try:
            # try to conveter in full number
            number_of_joints_to_insert = int(cmds.promptDialog(query=True, text=True))
            
            if number_of_joints_to_insert <= 0:
                cmds.warning("Please try with a positif number upper than 0.")
                return

            # Call the function for append joints
            Insert_Joints(start_joint_name, end_joint_name, number_of_joints_to_insert)
            
        except ValueError:
            cmds.warning("The input must be a valid integer.")
            return

def Insert_Joints(start_joint_name, end_joint_name, number_of_joints_to_insert):
    """Inserts equidistant joints with correct orientation for mirror chains."""

 # Save the hierarchy to not break it
    end_joint_parent = cmds.listRelatives(end_joint_name, parent=True, fullPath=True)
    if end_joint_parent:
        end_joint_parent = end_joint_parent[0]

    # Get the world positions
    start_pos = cmds.xform(start_joint_name, query=True, translation=True, worldSpace=True)
    end_pos = cmds.xform(end_joint_name, query=True, translation=True, worldSpace=True)
    
    start_vec = om.MVector(start_pos)
    end_vec = om.MVector(end_pos)
    
    total_distance = (end_vec - start_vec).length()
    number_of_segments = number_of_joints_to_insert + 1
    segment_length = total_distance / number_of_segments
    
    # Create and position the new joints
    current_parent_joint = start_joint_name
    new_joints = []

    # Get the orient of the starting joint
    start_joint_orient = cmds.getAttr(f'{start_joint_name}.jointOrient')[0]
    
    for i in range(number_of_joints_to_insert):
        # Calculate the position of the new joint in the world space
        current_distance = segment_length * (i + 1)
        direction_vec = (end_vec - start_vec).normal()
        new_world_pos_vec = start_vec + direction_vec * current_distance
        
        cmds.select(clear=True)

        # Creation of the joint in world space
        new_joint = cmds.joint(p=(new_world_pos_vec.x, new_world_pos_vec.y, new_world_pos_vec.z), n=f"{start_joint_name}_Bend_{i+1}")
        
        cmds.parent(new_joint, current_parent_joint)

        cmds.setAttr(f'{new_joint}.jointOrient', 0, 0, 0)
        
        current_parent_joint = new_joint
        new_joints.append(new_joint)

    # Reset the rotation of the joints so that the jointOrient is correct
    for joint in [start_joint_name] + new_joints:
        cmds.setAttr(f"{joint}.rotate", 0, 0, 0)
        
    # Re-parent the end joint at the end of the new chain :
        cmds.parent(end_joint_name, start_joint_name)
    
    # Finish
    if end_joint_parent:
        cmds.parent(end_joint_name, end_joint_parent)
    
    cmds.select(clear=True)
    print(f"{number_of_joints_to_insert} joints inserted at equal distance between {start_joint_name} and {end_joint_name}.")