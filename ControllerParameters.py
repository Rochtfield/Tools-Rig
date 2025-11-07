# -*- coding: utf-8 -*-
import maya.cmds as cmds

def Controller_Parameters_UI():
    """Creates a UI window for creating controllers with shape options."""
    
    # Name of the window to ensure that there is only one
    window_name = "ctrl_creator_ui"
    if cmds.window(window_name, exists=True):
       cmds.deleteUI(window_name, window=True)

    window = cmds.window(window_name, title="Controler Param", widthHeight=(600, 1000), sizeable=True)

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
    
    # Ajout d'un séparateur pour créer de l'espace avant la nouvelle section
    cmds.separator(height=15, style='in', parent=main_layout) 
    cmds.text(label="Extras Attributes:", parent=main_layout, align='center', font='boldLabelFont')

    # --- Création de la case à cocher ---
    IK_FK_Checkbox_Name = cmds.checkBox(
        label="IK FK",
        value=False,
        parent=main_layout,
    )

    FootRoll_Checkbox_Name = cmds.checkBox(
        label="FootRoll",
        value=False,
        parent=main_layout,
    )
    
    cmds.button(label="Create Controler", command=lambda *args: create_controller_logic(name_field, shape_menu, selected_joints, Color_Ctrl, IK_FK_Checkbox_Name,FootRoll_Checkbox_Name, window_name), parent=main_layout)
    
    cmds.showWindow(window)

def create_controller_logic(name_field, shape_menu, selected_joints, Color_Ctrl,IK_FK_Checkbox_Name,FootRoll_Checkbox_Name, window_name):
    """
    Logic for creating the controller.
    Called by the UI window button.
    """
    ctrl_name = cmds.textField(name_field, query=True, text=True)
    shape = cmds.optionMenu(shape_menu, query=True, value=True)
    color_label = cmds.optionMenu(Color_Ctrl, query=True, value=True)
    is_ikfk_checked = cmds.checkBox(IK_FK_Checkbox_Name, query=True, value=True)
    is_footroll_checked = cmds.checkBox(FootRoll_Checkbox_Name, query=True, value=True)

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
        square_shape = cmds.curve(d=1, p=[(0, 1, 1), (0, 1, -1), (0, -1, -1), (0, -1, 1), (0, 1, 1)], k=[0, 1, 2, 3, 4], n=f"{ctrl_name}_Ctrl")
        ctrl_shape = square_shape
    # Add other shapes here (Cube, Directional Arrow)
    
    # Add Extra Attribute IKFK
    attribute_name = "IK_FK_Switch" # Utilisez un nom de variable Python propre
    full_attr_name = f"{ctrl_name}.{attribute_name}"

    if is_ikfk_checked is True:
        attribute_name = "IK_FK_Switch" 
        full_attr_name = f"{ctrl_shape}.{attribute_name}"
        
        # Le reste du code est correct pour créer l'attribut
        if not cmds.objExists(full_attr_name):
            cmds.addAttr(
                ctrl_shape, 
                longName="IK_FK", 
                attributeType='float', 
                minValue=0.0, 
                maxValue=1.0, 
                defaultValue=0.0, 
                keyable=True,
                niceName="IKFK Switch"
            )
        

    # Add Extra Attribute Reversefoot
    attribute_name = "FootRoll" # Utilisez un nom de variable Python propre
    full_attr_name = f"{ctrl_name}.{attribute_name}"

    if is_footroll_checked is True:
        attribute_name = "FootRoll" 
        full_attr_name = f"{ctrl_shape}.{attribute_name}"
        
        # Le reste du code est correct pour créer l'attribut
        if not cmds.objExists(full_attr_name):
            cmds.addAttr(
                ctrl_shape, 
                longName="FootRoll", 
                attributeType='float', 
                minValue=0.0, 
                maxValue=1.0, 
                defaultValue=0.0, 
                keyable=True,
                niceName="FootRoll"
            )
        
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