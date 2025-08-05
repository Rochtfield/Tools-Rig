import maya.cmds as cmds

# --- Définition des fonctions pour les boutons ---
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


    # Create the left arm joints
    Left_Arm_joints = []
    Left_Arm_1 = cmds.joint(p= (1,0,0),r=True, name='Left_Arm_1')
    Left_Arm_joints.append(Left_Arm_1)

    for i in range(2, 4):
        joint_name = 'Left_Arm_{}'.format(i)
        Arm_joint = cmds.joint(p= (1,0,0),r=True, name=joint_name)
        Left_Arm_joints.append(Arm_joint)

    # Create elbow joint
    Left_Elbow_joint = cmds.joint(p= (1,0,0),r=True, name='Left_Elbow_joint')

    # Create end_arm_joint
    Left_End_Arm_joints = []
    Left_End_Arm_1 = cmds.joint(p= (1,0,0),r=True, name='Left_End_Arm_1')
    Left_End_Arm_joints.append(Left_Arm_1)

    for i in range(2, 4):
        joint_name = 'Left_End_Arm_{}'.format(i)
        End_arm_joint = cmds.joint(p= (1,0,0),r=True, name=joint_name)
        Left_End_Arm_joints.append(Arm_joint)

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

    cmds.mirrorJoint(Left_Clav_joint, mb=True, myz=True, sr=('Left','Right'))

    # Create the hip joints
    cmds.select (clear=True)

    Left_Leg_joint = cmds.joint(name='Left_Leg_joint')

    # Create the left leg joints
    Left_Leg_joints = []
    Left_Leg_1 = cmds.joint(p= (0,-1,0),r=True, name='Left_Leg_1')
    Left_Leg_joints.append(Left_Leg_1)

    for i in range(2, 4):
        joint_name = 'Left_Leg_{}'.format(i)
        Leg_joint = cmds.joint(p= (0,-1,0),r=True, name=joint_name)
        Left_Leg_joints.append(Leg_joint)
    
    Left_Knee_joint = cmds.joint(p= (0,-1,0),r=True, name='Left_Knee_joint')

    # Create the left endleg joints
    Left_End_Leg_joints = []
    Left_End_Leg_1 = cmds.joint(p= (0,-1,0),r=True, name='Left_End_Leg_1')
    Left_End_Leg_joints.append(Left_End_Leg_1)

    for i in range(2, 4):
        joint_name = 'Left_End_Leg_{}'.format(i)
        End_Leg_joint = cmds.joint(p= (0,-1,0),r=True, name=joint_name)
        Left_End_Leg_joints.append(Left_Knee_joint)

    Left_Ankle_joint = cmds.joint(p= (0,-1,0),r=True,  oj='none', name='Left_Ankle_joint')    
    
    cmds.select (clear=True)

    cmds.parent (Left_Leg_joint, Pelvis_joint)

    cmds.joint (Left_Leg_joint, e=True, ch=True,zso=True, oj='xyz', sao="zdown")

    cmds.mirrorJoint(Left_Leg_joint, mb=True, myz=True, sr=('Left','Right'))

    
def clic_bouton_JointBend(*args):
    """Fonction pour le bouton principal 2."""

def clic_bouton_DeformersJoint(*args):
    """Fonction pour le bouton principal 2."""

def action_dropdown_1(*args):
    """Fonction pour le premier élément du menu déroulant."""
    cmds.circle(name="monCercleSimple")
    
def action_dropdown_2(*args):
    """Fonction pour le deuxième élément du menu déroulant."""

    def create_square_controller():
        """
        Crée un contrôleur en forme de carré avec des points de contrôle (CVs).
        """
        square_points = [
            (-1, 0, -1),  # Point 1 (coin en bas à gauche)
            (-1, 0, 1),   # Point 2 (coin en haut à gauche)
            (1, 0, 1),    # Point 3 (coin en haut à droite)
            (1, 0, -1),   # Point 4 (coin en bas à droite)
            (-1, 0, -1)   # Point 5 (retour au premier point pour fermer le carré)
        ]

        cmds.curve(d=1, p=square_points, n='square_ctrl')

    # Appelle la fonction pour créer le carré
    create_square_controller()
    
def action_dropdown_3(*args):
    """Fonction pour le troisième élément du menu déroulant."""

    def create_cube_controller():
        """
        Crée un contrôleur en forme de cube en utilisant la commande cmds.curve().
        La courbe est de degré 1 (linéaire) pour avoir des arêtes droites.
        """
    
        # Coordonnées des 8 sommets d'un cube de 2x2x2 unités, centré sur l'origine
        points = [
            # Face du bas
            (-1, -1, -1),  # 0
            (1, -1, -1),   # 1
            (1, -1, 1),    # 2
            (-1, -1, 1),   # 3
            (-1, -1, -1),  # 0 (ferme la face du bas)
        
            # Arêtes verticales
            (-1, -1, 1),   # 3
            (-1, 1, 1),    # 4
            (1, 1, 1),     # 5
            (1, -1, 1),    # 2
        
            # Face du haut
            (1, 1, 1),     # 5
            (1, 1, -1),    # 6
            (-1, 1, -1),   # 7
            (-1, 1, 1),    # 4
        
            # Arête restante
            (-1, 1, -1),   # 7
            (1, 1, -1),    # 6
            (1, -1, -1)    # 1 (retourne au point initial pour fermer)
    ]
        cmds.curve(d=1, p=points, n='cube_ctrl')

    # Appelle la fonction pour créer le cube
    create_cube_controller()

def action_dropdown_4(*args):
    """Fonction pour le quatrième élément du menu déroulant."""
    cmds.confirmDialog(title="Info", message="Option 4 sélectionnée !", button=["OK"])


# --- Fonction principale pour créer l'interface ---
def create_main_window():
    """Crée la fenêtre principale avec des boutons et un menu déroulant."""
    
    # Détruit l'ancienne fenêtre si elle existe
    window_name = "Window"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)
    
    # Crée la fenêtre
    window = cmds.window(window_name, title="Mutaux Arthur", widthHeight=(250, 150))
    
    # Crée le layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")
    
    # Ajoute les éléments de l'interface
    cmds.text(label="control Pannel", parent=main_layout)
    
    # Bouton Skeleton
    cmds.button(label="Skeleton", command=clic_bouton_Skeleton, parent=main_layout)
    
    # Bouton Bend Joint
    cmds.button(label="Bend Joint", command=clic_bouton_JointBend, parent=main_layout)
    
    # Bouton Derformers muscles joint
    cmds.button(label="Deformers Joint", command=clic_bouton_DeformersJoint, parent=main_layout)

    # --- Menu déroulant (dropdown) ---
    cmds.text(label="Select Controlers :", parent=main_layout)
    
    option_menu = cmds.optionMenu(changeCommand=lambda item: handle_selection(item), parent=main_layout)
    cmds.menuItem(label="Circle", parent=option_menu)
    cmds.menuItem(label="Square", parent=option_menu)
    cmds.menuItem(label="Cube", parent=option_menu)
    cmds.menuItem(label="Directional Arrow", parent=option_menu)

    # Gère la sélection du menu
    def handle_selection(item_label):
        if item_label == "Circle":
            action_dropdown_1()
        elif item_label == "Square":
            action_dropdown_2()
        elif item_label == "Cube":
            action_dropdown_3()
        elif item_label == "Directional Arrow":
            action_dropdown_4()

    # Affiche la fenêtre
    cmds.showWindow(window)

# Appelle la fonction pour lancer l'interface
create_main_window()