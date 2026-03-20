# -*- coding: utf-8 -*-
import maya.cmds as cmds

def Create_Skeleton() :
    #check if BP_Skeleton exist
    BP_Name = 'BP_Skeleton'
    Skeleton = {}
    if cmds.objExists(BP_Name):
        childs = cmds.listRelatives(BP_Name, ad=True, type='transform')
        guides = [obj for obj in childs if "_Grp" not in obj and "Constraint" not in obj]

        for i in guides :
            joint_name = f"{i}_joint"
            cmds.select(cl=True)
            new_joint = cmds.joint(name= joint_name, radius=0.5)
            short_name = new_joint.split('|')[-1]
            cmds.matchTransform(new_joint, i)
            Skeleton[i] = short_name

    else :
         cmds.warning(f"Oups ! don't find grp {BP_Name}")

    #Parenting
    #Spine
    Spine_Guides = [name for name in Skeleton.keys() if "Spine" in name]
    Spine_Guides.sort()

    for i in range(1, len(Spine_Guides)):
        Childs_Guide = Spine_Guides[i]
        Parents_Guide = Spine_Guides[i-1]

        Childs_Joint = Skeleton[Childs_Guide]
        Parents_Joint = Skeleton[Parents_Guide]

        cmds.parent(Childs_Joint, Parents_Joint)

    #Arm
    Chain_Order_Arm = ['Left_Clav', 'Left_Arm', 'Left_Elbow', 'Left_Wrist']

    for i in range(1, len(Chain_Order_Arm)):
        Childs_Arm = Chain_Order_Arm[i]
        Parents_Arm = Chain_Order_Arm[i-1]

        Child_Joint_Arm = Skeleton[Childs_Arm]
        Parent_Joint_Arm = Skeleton[Parents_Arm]
        cmds.parent(Child_Joint_Arm, Parent_Joint_Arm)

    #Fingers
    Fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    Fingers_chain = {f:[]for f in Fingers}

    for name in Skeleton.keys():
        for f in Fingers:
            if f in name:
                Fingers_chain[f].append(name)
    
    sortable_list = []
    for name in Fingers:
        temp_sort_name = name.replace("End", "04")
        sortable_list.append((temp_sort_name, name))

    for f in Fingers : 
        Chains = sorted(Fingers_chain[f],key=lambda x: x.replace("End", "_04"))

        if not Chains:
            continue

        for i in range(1, len(Chains)):
            Childs_Fingers = Skeleton[Chains[i]]
            Parents_Fingers = Skeleton[Chains[i-1]]
            cmds.parent(Childs_Fingers, Parents_Fingers)

        if "Left_Wrist" in Skeleton:
            cmds.parent(Skeleton[Chains[0]], Skeleton["Left_Wrist"])

    #Leg

    Chain_Order_Leg = ["Left_Leg_loc", "Left_Knee_loc", "Left_Foot_loc", "Left_Toe_loc", "Left_ToeEnd_loc"]
    
    for i in range(1, len(Chain_Order_Leg)):
        Childs_Leg = Chain_Order_Leg[i]
        Parents_Leg = Chain_Order_Leg[i-1]

        Child_Joint_Leg = Skeleton[Childs_Leg]
        Parent_Joint_Leg = Skeleton[Parents_Leg]
        cmds.parent(Child_Joint_Leg, Parent_Joint_Leg)

    "Pense à changer le nom des leg joint bouffon"

    #Head

    Chain_Order_Head = ["Neck_01", "Neck_02", "Head", "HeadEnd"]
    
    for i in range (1,len(Chain_Order_Head)):
        Childs_Head = Chain_Order_Head[i]
        Parent_Head = Chain_Order_Head[i-1]
    
        Child_Joint_Head = Skeleton[Childs_Head]
        Parent_Joint_Head = Skeleton[Parent_Head]
        cmds.parent(Child_Joint_Head, Parent_Joint_Head)
    
    #Constraint and orient
    cmds.makeIdentity(list(Skeleton.values()), apply=True, rotate=True, translate=False, scale=False)
    
    Pelvis = "Pelvis_loc"
    Pelvis_joint = Skeleton[Pelvis]
    Neck = "Neck_01"
    Neck_joint = Skeleton[Neck]
    Clav = "Left_Clav"
    Clav_joint = Skeleton[Clav]
    Spine = "Spine_01"
    Spine_joint = Skeleton[Spine]
    SpineEnd = "Spine_04"
    SpineEnd_joint = Skeleton[SpineEnd]
    Leg = "Left_Leg_loc"
    Leg_joint = Skeleton[Leg]
    
    #joint Orient
    cmds.joint("Pelvis_loc_joint", edit=True, oj="xyz", sao="yup", ch=False, zso=True)
    cmds.joint("Spine_01_joint", edit=True, oj="xyz", sao="yup", ch=True, zso=True)
    cmds.joint("Left_Leg_loc_joint", edit=True, oj="xyz", sao="yup", ch=True, zso=True)
    cmds.joint("Left_ToeEnd_loc_joint", edit=True, oj="none", ch=False, zso=True)

    cmds.parent(Spine_joint, Pelvis_joint)
    cmds.parent(Leg_joint, Pelvis_joint)
    cmds.joint(Pelvis_joint, edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True)

    cmds.parent(Clav_joint, SpineEnd_joint)
    cmds.parent(Neck_joint, SpineEnd_joint)
    # Mirror

    start_joint = [Clav_joint, Leg_joint]

    for joint in start_joint:
    
        # "check if joint have Left or Right in his name"
        if 'Left_' in joint:
            search_string = 'Left_'
            replace_string = 'Right_'
        elif 'Right_' in joint:
            search_string = 'Right_'
            replace_string = 'Left_'
        else:
            cmds.warning("joint selected must have 'Left_' or 'Right_' in his name")
    
    # execution of mirror
    Right_Clav = cmds.mirrorJoint(Clav_joint, mirrorBehavior=True, mirrorYZ=True, searchReplace=(search_string, replace_string))
    Right_Leg = cmds.mirrorJoint(Leg_joint, mirrorBehavior=True, mirrorYZ=True, searchReplace=(search_string, replace_string))

    #IK Legs
    Leg_joint = Skeleton[Leg]
    Left_IK_Leg_Joint = cmds.duplicate(Leg_joint, rc = True)
    Right_IK_Leg_Joint = cmds.duplicate(Right_Leg, rc = True)

    All_IK_Joints = []

    Chain_Rename = [Left_IK_Leg_Joint, Right_IK_Leg_Joint]
    HRC_Group = cmds.group(empty=True, name="HRC_Skeleton")
    for Chain in Chain_Rename:
        Chain_Proper_Name = []
        for joint in Chain:
            New_Name = joint.replace("Left_", "Left_IK_").replace("Right_", "Right_IK_").replace("joint1", "joint")
            Final_Name = cmds.rename(joint, New_Name)
            Chain_Proper_Name.append(Final_Name)

        Knee = Chain_Proper_Name[1]
        
        #Set preferred Angle
        cmds.setAttr(Knee + ".rotateY", 0.1)
        cmds.joint(Knee, edit=True, spa=True)
        cmds.setAttr(Knee + ".rotateY", 0)
        
        cmds.ikHandle(name = "Left_IK_Leg", startJoint = Chain_Proper_Name[0] , endEffector = Chain_Proper_Name[-3], solver="ikRPsolver")
        cmds.parent(Chain_Proper_Name[0], HRC_Group)
    
