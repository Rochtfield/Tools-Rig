import maya.cmds as cmds
import math
import maya.api.OpenMaya as om


def DeformersJoint(*args):
    """Function for the main button deformersJoint."""
     # Check that only one joint is selected
    selected_joint = cmds.ls(selection=True, type='joint')

    if not selected_joint or len(selected_joint) > 1:
        cmds.warning("Please select only one joint for this operation.")
        return

    parent_joint = selected_joint[0]
    parent_rot = cmds.xform(parent_joint, query=True, rotation=True, worldSpace=True)

    # Parameters of the new joints
    radius = 2.0
    num_joints = 4
    angle_step = 360.0 / num_joints
    
    new_joints = []
    
    for i in range(num_joints):
        angle_rad = math.radians(i * angle_step)
        
        # 1. Create a temporary group at the position of the parent
        temp_group = cmds.group(empty=True, name=f"{parent_joint}_temp_grp_{i}")
        cmds.parent(temp_group, parent_joint)
        cmds.setAttr(f"{temp_group}.t", 0, 0, 0)
        cmds.setAttr(f"{temp_group}.r", parent_rot[0], parent_rot[1], parent_rot[2])
        
        # 2. Position the group on the circle
        cmds.setAttr(f"{temp_group}.ty", radius * math.cos(angle_rad))
        cmds.setAttr(f"{temp_group}.tz", radius * math.sin(angle_rad))
        
        # 3. Create the joint
        cmds.select(clear=True)
        new_joint = cmds.joint(n=f"{parent_joint}_Deformers_{i+1}")
        
        # 4. Apply the group transformation to the joint
        world_pos = cmds.xform(temp_group, query=True, translation=True, worldSpace=True)
        world_rot = cmds.xform(temp_group, query=True, rotation=True, worldSpace=True)
        
        cmds.xform(new_joint, translation=world_pos, worldSpace=True)
        cmds.xform(new_joint, rotation=world_rot, worldSpace=True)
        
        # 5. Delete the temporary group
        cmds.delete(temp_group)

        # 6. Freeze transformations
        cmds.makeIdentity(new_joint, apply=True, t=1, r=1, s=1, n=0)
        new_joints.append(new_joint)
        
    # 7. Final parentage of the new joints
    for joint in new_joints:
        cmds.parent(joint, parent_joint)
    
    deformer_joints = cmds.ls(type='joint', recursive=True, l=True)
    
    # Filter for joints that contain "Deformers" in their name
    filtered_deformer_joints = [j for j in deformer_joints if 'Deformers' in j]

    if not filtered_deformer_joints:
        cmds.warning("No joints containing 'Deformers' were found.")
        return

    # Loop on each filtered joint and reset its jointOrient
    for joint in filtered_deformer_joints:
        try:
            cmds.setAttr(f'{joint}.jointOrient', 0, 0, 0, type='double3')
            print(f"Orientation of {joint} has been reset.")
        except RuntimeError:
            cmds.warning(f"Unable to reset the orientation of {joint}. The 'jointOrient' attribute may not exist.")

    print(f"creation of {num_joints} joints around the X axis of the joint {parent_joint} finished.")