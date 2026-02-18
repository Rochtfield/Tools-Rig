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
        grp_arm = cmds.group(empty=True, name = name_arm_sphere + "_Grp")
        cmds.matchTransform(grp_arm, arm_sphere)
        cmds.parent(arm_sphere, grp_arm)
        arm_Grp.append(grp_arm)
        arm_Sphere.append(arm_sphere)

    #Fingers
    Thumb_Sphere = []
    Index_Sphere = []
    Middle_Sphere = []
    Ring_Sphere = []
    Pinky_Sphere = []
    Thumb_Grp = []
    Index_Grp = []
    Middle_Grp = []
    Ring_Grp = []
    Pinky_Grp = []

    name_finger_Thumb = ["Left_Thumb_01", "Left_Thumb_02", "Left_Thumb_03", "Left_ThumbEnd"]
    name_finger_Index = ["Left_Index_01", "Left_Index_02", "Left_Index_03", "Left_IndexEnd"]
    name_finger_Middle = ["Left_Middle_01", "Left_Middle_02", "Left_Middle_03", "Left_MiddleEnd"]
    name_finger_Ring = ["Left_Ring_01", "Left_Ring_02", "Left_Ring_03", "Left_RingEnd"]
    name_finger_Pinky = ["Left_Pinky_01", "Left_Pinky_02", "Left_Pinky_03", "Left_PinkyEnd"]
    for i in range (0,4):
        name_thumb_sphere = name_finger_Thumb [i]
        Z_pos_Thumb = 5 + (i) * 2
        thumb_sphere = cmds.polySphere(name=name_thumb_sphere, radius=0.5)[0]
        cmds.setAttr(f"{thumb_sphere}.translate", 42, 90, Z_pos_Thumb, type='double3')
        cmds.setAttr(f"{thumb_sphere}.rotate", -90, -90, 0, type='double3')
        grp_thumb = cmds.group(empty=True, name = name_thumb_sphere + "_Grp")
        cmds.matchTransform (grp_thumb, thumb_sphere)
        cmds.parent (thumb_sphere, grp_thumb)

        name_index_sphere = name_finger_Index [i]
        x_pos_Index = 45 + (i) * 2
        index_sphere = cmds.polySphere(name=name_index_sphere, radius=0.5)[0]
        cmds.setAttr(f"{index_sphere}.translate", x_pos_Index, 90, 2, type='double3')
        cmds.setAttr(f"{index_sphere}.rotate", -90, 0, 0, type='double3')
        grp_index = cmds.group(empty=True, name = name_index_sphere + "_Grp")
        cmds.matchTransform (grp_index, index_sphere)
        cmds.parent (index_sphere, grp_index)

        name_middle_sphere = name_finger_Middle [i]
        x_pos_Middle = 45 + (i) * 2
        middle_sphere = cmds.polySphere(name=name_middle_sphere, radius=0.5)[0]
        cmds.setAttr(f"{middle_sphere}.translate",  x_pos_Middle, 90, 0, type='double3')
        cmds.setAttr(f"{middle_sphere}.rotate", -90, 0, 0, type='double3')
        grp_middle = cmds.group(empty=True, name = name_middle_sphere + "_Grp")
        cmds.matchTransform (grp_middle, middle_sphere)
        cmds.parent (middle_sphere, grp_middle)

        name_ring_sphere = name_finger_Ring [i]
        x_pos_Ring = 45 + (i) * 2
        ring_sphere = cmds.polySphere(name=name_ring_sphere, radius=0.5)[0]
        cmds.setAttr(f"{ring_sphere}.translate",  x_pos_Ring, 90, -2, type='double3')
        cmds.setAttr(f"{ring_sphere}.rotate", -90, 0, 0, type='double3')
        grp_ring = cmds.group(empty=True, name = name_ring_sphere + "_Grp")
        cmds.matchTransform (grp_ring, ring_sphere)
        cmds.parent (ring_sphere, grp_ring)

        name_pinky_sphere = name_finger_Pinky [i]
        x_pos_Pinky = 45 + (i) * 2
        pinky_sphere = cmds.polySphere(name=name_pinky_sphere, radius=0.5)[0]
        cmds.setAttr(f"{pinky_sphere}.translate",  x_pos_Pinky, 90, -4, type='double3')
        cmds.setAttr(f"{pinky_sphere}.rotate", -90, 0, 0, type='double3')
        grp_pinky = cmds.group(empty=True, name = name_pinky_sphere + "_Grp")
        cmds.matchTransform (grp_pinky, pinky_sphere)
        cmds.parent (pinky_sphere, grp_pinky)
        
        Thumb_Sphere.append(thumb_sphere)
        Index_Sphere.append(index_sphere)
        Middle_Sphere.append(middle_sphere)
        Ring_Sphere.append(ring_sphere)
        Pinky_Sphere.append(pinky_sphere)
        Thumb_Grp.append(grp_thumb)
        Index_Grp.append(grp_index)
        Middle_Grp.append(grp_middle)
        Ring_Grp.append(grp_ring)
        Pinky_Grp.append(grp_pinky)

    #neck
    Neck_Sphere = []
    Neck_Grp = []
    spine_spheres.append(sphere)
    for i in range(1,3):
        name_neck_sphere = f"Neck_{i:02d}"
        y_pos = 95 + (i -1) * 5
        neck_sphere = cmds.polySphere(name=name_neck_sphere, radius=0.5)[0]
        cmds.setAttr(f"{neck_sphere}.translate", 0, y_pos, 0, type='double3')
        cmds.setAttr(f"{neck_sphere}.rotate", -90, 0, 90, type='double3')
        grp_neck = cmds.group(empty=True, name = name_neck_sphere + "_Grp")
        cmds.matchTransform(grp_neck, neck_sphere)
        cmds.parent(neck_sphere, grp_neck)
        Neck_Sphere.append(neck_sphere)
        Neck_Grp.append(grp_neck)

    #head
    Head_Sphere = []
    Head_Grp = []
    name_head = ["Head", "HeadEnd"]
    for i in range(0,2):
        name_head_sphere = name_head [i]
        Y_pos = 105+ i * 2
        head_sphere = cmds.polySphere(name=name_head_sphere, radius=0.5)[0]
        cmds.setAttr(f"{head_sphere}.translate", 0, Y_pos, 0, type='double3')
        cmds.setAttr(f"{head_sphere}.rotate", -90, 0, 90, type='double3')
        grp_head = cmds.group(empty=True, name = name_head_sphere + "_Grp")
        cmds.matchTransform (grp_head, head_sphere)
        cmds.parent (head_sphere, grp_head)
        Head_Sphere.append(head_sphere)
        Head_Grp.append(grp_head)

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
    cmds.parent (arm_Grp[0], spine_spheres[4])
    cmds.parent(arm_Grp[3], arm_Sphere[0])
    cmds.parent(arm_Grp[2], arm_Sphere[0])
    cmds.parent(arm_Grp[1], arm_Sphere[0])
    cmds.pointConstraint(arm_Sphere[1], arm_Sphere[3], arm_Grp[2],  maintainOffset=True)

    #Fingers

    #Thumb
    cmds.parent(Thumb_Grp[3], Thumb_Sphere[2])
    cmds.parent(Thumb_Grp[2], Thumb_Sphere[1])
    cmds.parent(Thumb_Grp[1], Thumb_Sphere[0])
    cmds.parent(Thumb_Grp[0], arm_Sphere[3])
    #Index
    cmds.parent(Index_Grp[3], Index_Sphere[2])
    cmds.parent(Index_Grp[2], Index_Sphere[1])
    cmds.parent(Index_Grp[1], Index_Sphere[0])
    cmds.parent(Index_Grp[0], arm_Sphere[3])
    #Middle
    cmds.parent(Middle_Grp[3], Middle_Sphere[2])
    cmds.parent(Middle_Grp[2], Middle_Sphere[1])
    cmds.parent(Middle_Grp[1], Middle_Sphere[0])
    cmds.parent(Middle_Grp[0], arm_Sphere[3])
    #Ring
    cmds.parent(Ring_Grp[3], Ring_Sphere[2])
    cmds.parent(Ring_Grp[2], Ring_Sphere[1])
    cmds.parent(Ring_Grp[1], Ring_Sphere[0])
    cmds.parent(Ring_Grp[0], arm_Sphere[3])
    #Pinky
    cmds.parent(Pinky_Grp[3], Pinky_Sphere[2])
    cmds.parent(Pinky_Grp[2], Pinky_Sphere[1])
    cmds.parent(Pinky_Grp[1], Pinky_Sphere[0])
    cmds.parent(Pinky_Grp[0], arm_Sphere[3]) 

    # Legs
    cmds.pointConstraint(leftLeg_sphere, leftFoot_sphere, grp,  maintainOffset=True)
    cmds.parent(leftToeEnd_sphere, leftToe_sphere)
    cmds.parent(leftToe_sphere, leftFoot_sphere)
    cmds.parent(leftLeg_sphere, pelvis_sphere)
    cmds.parent(grp,pelvis_sphere)
    
    #Head - Neck
    cmds.parent(Neck_Grp[1], Neck_Sphere[0])
    cmds.parent(Neck_Grp[0], spine_spheres[4])
    
    cmds.parent(Head_Grp[1], Head_Sphere[0])
    cmds.parent(Head_Grp[0], Neck_Sphere[1])
    
    #Pelvis
    cmds.parent(pelvis_sphere, grpPelvis)
    cmds.parent(leftFoot_sphere, grpPelvis)