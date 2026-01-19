# -*- coding: utf-8 -*-

import maya.cmds as cmds
import math
import maya.api.OpenMaya as om

def Create_BlueprintSkeleton():
    pelvis_sphere = cmds.polySphere (name='Pelvis_loc' , radius=0.5)[0]
    
    Color = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{Color}.color", 1.0 , 1.0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Blue_ShaderSG")
    cmds.connectAttr(f"{Color}.outColor", f"{sg}.surfaceShader")
    cmds.sets(pelvis_sphere, edit=True, forceElement=sg)
    cmds.select(clear=True)