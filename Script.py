import maya.cmds as cmds
import math
import maya.api.OpenMaya as om

# --- define button ---
def clic_bouton_Skeleton(*args):
    """Fonction pour le bouton principal 1."""
    # Create the root joint
    Root_joint = cmds.joint(name='Root_joint')

    # Create the pelvis joint
    Pelvis_joint = cmds.joint(name='Pelvis_joint')

    # Create the spine joints
    Spine_joints = []
    for i in range(1, 5):
            joint_name = 'Spine_{}'.format(i)
            Spine_joint = cmds.joint(p= (0,1,0), r=True, n=joint_name)
            Spine_joints.append(Spine_joint)
    
    # Create the neck joint
    Neck_joint = cmds.joint(p= (0,1,0), r=True, name='Neck_joint')

    # Create the head joint
    Head_joint = cmds.joint(p= (0,1,0), r=True, name='Head_joint')

    cmds.joint (Pelvis_joint, e=True, ch=True,zso=True, oj='xyz', sao="zdown")
    cmds.joint (Spine_joints[3], e=True, ch=True,zso=True, oj='none')

    # Create the shoulder joints
    cmds.select (clear=True)

    Left_Clav_joint = cmds.joint(name='Left_Clav_joint')

    Left_Shoulder_joint = cmds.joint(name='Left_Shoulder_joint')

    # Create elbow joint
    Left_Elbow_joint = cmds.joint(p= (1,0,0),r=True, name='Left_Elbow_joint')

    # Create wrist joint
    Left_Wrist_joint = cmds.joint(p= (1,0,0),r=True, name='Left_Wrist_joint')

    # Create the left Index joints
    Left_Index_joints = []
    Left_Index_1 = cmds.joint(p= (1,0,0),r=True, name='Left_Index_1')
    Left_Index_joints.append(Left_Index_1)

    for i in range(2, 5):
        joint_name = 'Left_Index_{}'.format(i)
        Index_joint = cmds.joint(p= (1,0,0),r=True, name=joint_name)
        Left_Index_joints.append(Index_joint)

    
    cmds.select (clear=True)

    cmds.parent (Left_Clav_joint, Spine_joints[3])

    # Create the hip joints
    cmds.select (clear=True)

    Left_Leg_joint = cmds.joint(name='Left_Leg_joint')

    # Create the left leg joints
    Left_Leg_joints = []
    Left_Leg_1 = cmds.joint(p= (0,-1,0),r=True, name='Left_Leg_1')
    Left_Leg_joints.append(Left_Leg_1)
    
    Left_Knee_joint = cmds.joint(p= (0,-1,0),r=True, name='Left_Knee_joint')

    Left_Ankle_joint = cmds.joint(p= (0,-1,0),r=True,  oj='none', name='Left_Ankle_joint')    
    
    cmds.select (clear=True)

    cmds.parent (Left_Leg_joint, Pelvis_joint)

    cmds.joint (Left_Leg_joint, e=True, ch=True,zso=True, oj='xyz', sao="zdown")

def clic_Button_JointBend(*args):
    """
    Main function to insert joints between two selected joints.
    It displays a dialog window to ask for the number of joints.
    """
    
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
            insert_joints(start_joint_name, end_joint_name, number_of_joints_to_insert)
            
        except ValueError:
            cmds.warning("The input must be a valid integer.")
            return

def insert_joints(start_joint_name, end_joint_name, number_of_joints_to_insert):
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

def clic_bouton_DeformersJoint(*args):
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

def clic_Button_MirrorJoint(*args):
    """for MirrorJoint"""
    
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

def clic_Buton_ControlerParam(*args):
    """Creates a UI window for creating controllers with shape options."""
    
    # Name of the window to ensure that there is only one
    window_name = "ctrl_creator_ui"
    if cmds.window(window_name, exists=True):
       cmds.deleteUI(window_name, window=True)

    window = cmds.window(window_name, title="Controler Param", widthHeight=(300, 200), sizeable=False)

    # Create the main layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    # Check if a joint is selected to pre-fill the name
    selected_joints = cmds.ls(selection=True, type='joint')
    ctrl_name = "Ctrl"
    if selected_joints:
        joint_name = selected_joints[0]
        ctrl_name = joint_name.replace('joint', 'ctrl')

    # Create the elements of the UI
    cmds.text(label="Name Controler:", parent=main_layout)
    name_field = cmds.textField(text=ctrl_name, parent=main_layout)
    
    cmds.text(label="Shape Controler:", parent=main_layout)
    shape_menu = cmds.optionMenu(parent=main_layout)
    cmds.menuItem(label="Circle")
    cmds.menuItem(label="Square")
    cmds.menuItem(label="Cube")
    cmds.menuItem(label="Directional Arrow")

     # Adding the color selection menu
    cmds.text(label="Color Controler:", parent=main_layout)
    Color_Ctrl = cmds.optionMenu(parent=main_layout)
    cmds.menuItem(label="Yellow (17)")
    cmds.menuItem(label="Blue (6)")
    cmds.menuItem(label="Red (13)")
    cmds.menuItem(label="Green (14)")
    
    cmds.button(label="Create Controler", command=lambda *args: create_controller_logic(name_field, shape_menu, selected_joints, Color_Ctrl, window_name), parent=main_layout)
    
    cmds.showWindow(window)

def create_controller_logic(name_field, shape_menu, selected_joints, Color_Ctrl, window_name):
    """
    Logic for creating the controller.
    Called by the UI window button.
    """
    ctrl_name = cmds.textField(name_field, query=True, text=True)
    shape = cmds.optionMenu(shape_menu, query=True, value=True)
    color_label = cmds.optionMenu(Color_Ctrl, query=True, value=True)
    
    # Extract the color index from the menu label (ex : "Yellow (17)")
    color_index = int(color_label.split('(')[-1].replace(')', ''))
    
    if not ctrl_name:
        cmds.warning("Please enter a valid name.")
        return

    # 1. Create the parent group (Offset)
    offset_grp = cmds.group(empty=True, name=f"{ctrl_name}_Ctrl_Grp")
    
    # 2. Create the main group (Ctrl)
    ctrl_grp = cmds.group(empty=True, name=f"{ctrl_name}_Offset_Grp")
    
    # 3. Set the Ctrl group to the Offset group
    cmds.parent(ctrl_grp, offset_grp)
    
    # 4. Create the shape of the controller according to the chosen option
    ctrl_shape = None
    if shape == "Circle":
        ctrl_shape = cmds.circle(name=f"{ctrl_name}_Ctrl", normal=[1, 0, 0])[0]
    elif shape == "Square":
        # Create a square
        square_shape = cmds.curve(d=1, p=[(0, 1, 1), (0, 1, -1), (0, -1, -1), (0, -1, 1), (0, 1, 1)], k=[0, 1, 2, 3, 4], n=f"{ctrl_name}_Ctrl")
        ctrl_shape = square_shape
    # Add other shapes here (Cube, Directional Arrow)
    
    # 5. Parent the shape to the group Ctrl
    if ctrl_shape:
        cmds.parent(ctrl_shape, ctrl_grp, relative=True, shape=True)
        # Remove the transformation of the circle to keep the hierarchy clean
        cmds.delete(ctrl_shape, constructionHistory=True)

        # Apply the color to the controller shape
        shape_node = cmds.listRelatives(ctrl_shape, shapes=True)[0]
        cmds.setAttr(f"{shape_node}.overrideEnabled", 1)
        cmds.setAttr(f"{shape_node}.overrideColor", color_index)
    
    # If a joint is selected, place the controller hierarchy at its position and rotation
    if selected_joints:
        joint_pos = cmds.xform(selected_joints[0], query=True, translation=True, worldSpace=True)
        joint_rot = cmds.xform(selected_joints[0], query=True, rotation=True, worldSpace=True)
        
        cmds.xform(offset_grp, translation=joint_pos, worldSpace=True)
        cmds.xform(offset_grp, rotation=joint_rot, worldSpace=True)
        
    print(f"Controller '{ctrl_name}' created with the form '{shape}'.")

    # 6. Close the UI window
    cmds.deleteUI(window_name, window=True)

# --- Main function for UI ---
def create_main_window():
    """Create the main window with buttons and a drop-down menu."""
    
    # Destroy the old window if it exists
    window_name = "Window"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    
    # Create window
    window = cmds.window(window_name, title="Mutaux Arthur", widthHeight=(250, 150))
    
    # Create layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    
    # Add elements on interface
    cmds.text(label="control Pannel", parent=main_layout)
    
    # Button Skeleton
    cmds.button(label="Skeleton", command=clic_bouton_Skeleton, parent=main_layout)
    
    # Button Bend Joint
    cmds.button(label="Bend Joints", command=clic_Button_JointBend, parent=main_layout)
    
    # Button Derformers muscles joint
    cmds.button(label="Deformers Joints", command=clic_bouton_DeformersJoint, parent=main_layout)

    # Button Mirror Joint
    cmds.button(label="Mirror Joints", command=clic_Button_MirrorJoint, parent=main_layout)

    # Dopdown Menu
    cmds.text(label="Select Controlers :", parent=main_layout)
    
    cmds.button(label="Controler Params", command=clic_Buton_ControlerParam, parent=main_layout)

    # displays the window
    cmds.showWindow(window)

# --- Call The function for create interface ---
create_main_window()