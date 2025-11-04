import maya.cmds as cmds
    
def MirrorJoints():
    selected_joints = cmds.ls(selection=True, type='joint')

    if not selected_joints:
        cmds.warning("select a joint before clic button")
        return
    
    start_joint = selected_joints[0]
    
    # "check if joint have Left or Right in his name"
    if 'Left_' in start_joint:
        search_string = 'Left_'
        replace_string = 'Right_'
    elif 'Right_' in start_joint:
        search_string = 'Right_'
        replace_string = 'Left_'
    else:
        cmds.warning("joint selected must have 'Left_' or 'Right_' in his name")
        return
    
    # execution of mirror
    cmds.mirrorJoint(start_joint, mirrorBehavior=True, mirrorYZ=True, searchReplace=(search_string, replace_string))

    print(f"the selection {start_joint} has been edited sucesfuly")