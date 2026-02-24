import maya.cmds as cmds
import maya.api.OpenMaya as om

def Add_Attribute(LongName, ctrl_shape, AttributeType, EnumName="", MinValue=None, MaxValue=None):
    if AttributeType == 'enum':
        cmds.addAttr(
            ctrl_shape,
            longName=LongName,
            attributeType=AttributeType,
            enumName=EnumName,
            defaultValue=0,
            keyable=True,
            )
    else: 
        cmds.addAttr(
            ctrl_shape,
            longName=LongName,
            attributeType=AttributeType,
            defaultValue=0.0,
            keyable=True,
        ) 
        if MinValue is not None:
            cmds.addAttr(f"{ctrl_shape}.{LongName}", edit=True, minValue=MinValue)
        if MaxValue is not None:
            cmds.addAttr(f"{ctrl_shape}.{LongName}", edit=True, maxValue=MaxValue) 