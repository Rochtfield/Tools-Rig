# -*- coding: utf-8 -*-

import maya.cmds as cmds
import math
import maya.api.OpenMaya as om

def Create_BlueprintSkeleton():
        #Pelvis
    pelvis_sphere = cmds.polySphere (name='Pelvis_loc' , radius=0.5)[0]
    cmds.setAttr(f"{pelvis_sphere}.translate", 0, 50, 0, type='double3')
    cmds.setAttr(f"{pelvis_sphere}.rotateAxis", -90, 0, 90, type='double3')

    Color = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{Color}.color", 1.0 , 1.0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Blue_ShaderSG")
    cmds.connectAttr(f"{Color}.outColor", f"{sg}.surfaceShader")
    cmds.sets(pelvis_sphere, edit=True, forceElement=sg)
    cmds.select(clear=True)

    #Spine
    spine_spheres = []
    for i in range(1, 5):
        name = f"Spine_{i:02d}"
        y_pos = 65 + (i -1) * 10
    
        sphere = cmds.polySphere(name=name, radius=0.5)[0]
        cmds.setAttr(f"{sphere}.translate", 0, y_pos, 0, type='double3')
        cmds.setAttr(f"{sphere}.rotate", -90, 0, 90, type='double3')

        spine_spheres.append(sphere)
    
    color_node = cmds.shadingNode('lambert', asShader=True, name="Spine_Yellow_Shader")
    cmds.setAttr(f"{color_node}.color", 1.0, 1.0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Yellow_ShaderSG")
    cmds.connectAttr(f"{color_node}.outColor", f"{sg}.surfaceShader")
    cmds.sets(spine_spheres, edit=True, forceElement=sg)
    cmds.select(clear=True)
    
    #legs 
    leftLeg_sphere = cmds.polySphere (name ='Left_Leg_loc' , radius=0.5)[0]
    cmds.setAttr(f"{leftLeg_sphere}.translate", 10, 45, 0, type='double3')
    cmds.setAttr(f"{leftLeg_sphere}.rotateAxis", 0, 180, 90, type='double3')

    leftKnee_sphere = cmds.polySphere (name ='Left_Knee_loc' , radius=0.5)[0]
    cmds.setAttr(f"{leftKnee_sphere}.translate", 10, 25, 0, type='double3')
    cmds.setAttr(f"{leftKnee_sphere}.rotateAxis", 0, 180, 90, type='double3')
    
    grp = cmds.group(empty=True, name='Left_Knee_loc_Grp')
    cmds.matchTransform(grp, leftKnee_sphere)
    cmds.setAttr(f"{grp}.rotateAxis", 0, 180, 90, type='double3')
    cmds.parent(leftKnee_sphere, grp)

    leftFoot_sphere = cmds.polySphere (name ='Left_Foot_loc' , radius=0.5)[0]
    cmds.setAttr(f"{leftFoot_sphere}.translate", 10, 5, 0, type='double3')
    cmds.setAttr(f"{leftFoot_sphere}.rotateAxis", 0, 180, 90, type='double3')

    leftToe_sphere = cmds.polySphere (name ='Left_Toe_loc' , radius=0.5)[0]
    cmds.setAttr(f"{leftToe_sphere}.translate", 10, 0 , 5, type='double3')
    cmds.setAttr(f"{leftToe_sphere}.rotateAxis", 0, -90, 0, type='double3')

    leftToeEnd_sphere = cmds.polySphere (name ='Left_ToeEnd_loc' , radius=0.5)[0]
    cmds.setAttr(f"{leftToeEnd_sphere}.translate", 10, 0, 10, type='double3')
    cmds.setAttr(f"{leftToeEnd_sphere}.rotateAxis", 0, -90, 0, type='double3')

    LeftSpheres = [leftLeg_sphere, leftKnee_sphere, leftFoot_sphere, leftToe_sphere, leftToeEnd_sphere]
    Color = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{Color}.color", 1.0 , 0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Blue_ShaderSG")
    cmds.connectAttr(f"{Color}.outColor", f"{sg}.surfaceShader")
    cmds.sets(LeftSpheres, edit=True, forceElement=sg)
    cmds.select(clear=True)

    cmds.pointConstraint(leftLeg_sphere, leftFoot_sphere, grp,  maintainOffset=True)
    cmds.parent(leftToeEnd_sphere, leftToe_sphere)
    cmds.parent(leftToe_sphere, leftFoot_sphere)
    cmds.parent(leftLeg_sphere, pelvis_sphere)
    cmds.parent(grp,pelvis_sphere)

    grpPelvis=cmds.group(empty=True, name='BP_Skeleton')
    cmds.parent(pelvis_sphere, grpPelvis)
    cmds.parent(leftFoot_sphere, grpPelvis) 