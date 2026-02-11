# -*- coding: utf-8 -*-

import maya.cmds as cmds
import math
import maya.api.OpenMaya as om

def Create_BlueprintSkeleton():
    #Pelvis
    pelvis_sphere = cmds.polySphere (name='Pelvis_loc' , radius=0.5)[0]
    cmds.setAttr(f"{pelvis_sphere}.translate", 0, 50, 0, type='double3')
    cmds.setAttr(f"{pelvis_sphere}.rotateAxis", -90, 0, 90, type='double3')
    grpPelvis=cmds.group(empty=True, name='BP_Skeleton')

    #Spine
    spine_spheres = []
    spines_grp = []
    for i in range(1, 5):
        name_spine_sphere = f"Spine_{i:02d}"
        y_pos = 60 + (i -1) * 10
        sphere = cmds.polySphere(name=name_spine_sphere, radius=0.5)[0]
        cmds.setAttr(f"{sphere}.translate", 0, y_pos, 0, type='double3')
        cmds.setAttr(f"{sphere}.rotate", -90, 0, 90, type='double3')
        grp_spine = cmds.group(empty=True, name = name_spine_sphere + "_Grp")
        cmds.matchTransform(grp_spine, sphere)
        cmds.parent(sphere, grp_spine)
        cmds.parent(grp_spine, grpPelvis)
        
        spine_spheres.append(sphere)
        spines_grp.append(grp_spine)

    cmds.pointConstraint(pelvis_sphere, spine_spheres[1], spines_grp[0],  maintainOffset=True)
    cmds.pointConstraint(spine_spheres[3], spine_spheres[1], spines_grp[2], maintainOffset=True)
    
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

    #arm
    arm_Sphere = []
    arm_Grp = []
    spine_spheres.append(sphere)
    name_arm = ["Left_Clav", "Left_Arm", "Left_Elbow", "Left_Wrist"]
    for i in range (0,4):
        name_arm_sphere = name_arm [i]
        x_pos = 10 + (i) * 10
        arm_sphere = cmds.polySphere(name=name_arm_sphere, radius=0.5)[0]
        cmds.setAttr(f"{arm_sphere}.translate", x_pos, 90, 0, type='double3')
        cmds.setAttr(f"{arm_sphere}.rotate", -90, 0, 0, type='double3')
        grp_arm =cmds.group(empty=True, name = name_arm_sphere + "_Grp")
        cmds.matchTransform(grp_arm, arm_sphere)
        cmds.parent(arm_sphere, grp_arm)
        arm_Grp.append(grp_arm)
        arm_Sphere.append(arm_sphere)

    cmds.parentConstraint (spine_spheres[4], arm_Grp[0], maintainOffset=True)
    cmds.select(clear=True)

    #head
    spine_spheres.append(sphere)
    for i in range(1,3):
        name_neck_sphere = f"Neck_{i:02d}"
        y_pos = 100 + (i -1) * 5
        neck_sphere = cmds.polySphere(name=name_neck_sphere, radius=0.5)[0]
        cmds.setAttr(f"{neck_sphere}.translate", 0, y_pos, 0, type='double3')
        cmds.setAttr(f"{neck_sphere}.rotate", -90, 0, 90, type='double3')
        grp_neck = cmds.group(empty=True, name = name_neck_sphere + "_Grp")
        cmds.matchTransform(grp_neck, neck_sphere)
        cmds.parent(neck_sphere, grp_neck)
        cmds.parent(grp_neck, spine_spheres[4])
    
    cmds.select(clear=True) 

    # color
    arm_Grp.append(grp_arm)
    LeftSpheres = [leftLeg_sphere, leftKnee_sphere, leftFoot_sphere, leftToe_sphere, leftToeEnd_sphere,]
    Color = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{Color}.color", 1.0 , 0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Red_Shader")
    cmds.connectAttr(f"{Color}.outColor", f"{sg}.surfaceShader")
    cmds.sets(LeftSpheres, edit=True, forceElement=sg)
    cmds.sets(arm_Grp, edit=True, forceElement=sg)
    cmds.select(clear=True)

    color_node = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{color_node}.color", 1.0, 1.0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Yellow_Shader")
    cmds.connectAttr(f"{color_node}.outColor", f"{sg}.surfaceShader")
    cmds.sets(spine_spheres, edit=True, forceElement=sg)
    cmds.select(clear=True)

    Color = cmds.shadingNode('lambert', asShader=True, name="Color_Shader")
    cmds.setAttr(f"{Color}.color", 1.0 , 1.0, 0, type='double3')
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="_Shader")
    cmds.connectAttr(f"{Color}.outColor", f"{sg}.surfaceShader")
    cmds.sets(pelvis_sphere, edit=True, forceElement=sg)
    cmds.select(clear=True)

    # Constraint all under Pelvis
    # Arm
    arm_Grp.append(grp_arm)
    arm_Sphere.append(arm_sphere)
    cmds.parent(arm_Grp[3], arm_Sphere[0])
    cmds.parent(arm_Grp[2], arm_Sphere[0])
    cmds.parent(arm_Grp[1], arm_Sphere[0])
    cmds.pointConstraint(arm_Sphere[1], arm_Sphere[3], arm_Grp[2],  maintainOffset=True)
    cmds.select(clear=True)
    
    # Legs
    cmds.pointConstraint(leftLeg_sphere, leftFoot_sphere, grp,  maintainOffset=True)
    cmds.parent(leftToeEnd_sphere, leftToe_sphere)
    cmds.parent(leftToe_sphere, leftFoot_sphere)
    cmds.parent(leftLeg_sphere, pelvis_sphere)
    cmds.parent(grp,pelvis_sphere)
    #Pelvis
    cmds.parent(pelvis_sphere, grpPelvis)
    cmds.parent(leftFoot_sphere, grpPelvis)