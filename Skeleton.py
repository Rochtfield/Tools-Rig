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
    