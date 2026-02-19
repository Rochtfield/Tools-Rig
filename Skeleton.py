# -*- coding: utf-8 -*-
import maya.cmds as cmds

def Create_Skeleton() :
     
    #check if BP_Skeleton exist
    BP_Name = 'BP_Skeleton'
    if cmds.objExists(BP_Name):
        childs = cmds.listRelatives(BP_Name, ad=True, type='transform')
        guides = [obj for obj in childs if "_Grp" not in obj and "Constraint" not in obj]
    
        for i in guides :
            joint_name = f"{i}_joint"
            cmds.select(cl=True)
            new_joint = cmds.joint(name= joint_name, radius=0.5)
            cmds.matchTransform(new_joint, i)
    
    else :
         cmds.warning(f"Oups ! don't find grp {BP_Name}")