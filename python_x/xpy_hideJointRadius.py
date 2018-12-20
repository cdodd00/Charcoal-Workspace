'''
Hides radius attr on all joints in scene
'''

import maya.cmds as mc
#-------------

def hideJointRadius():
   
    allJoints = mc.ls (type="joint")

    for jt in allJoints:
        
        mc.setAttr ((jt + ".radius"), cb = 0)
        
    print 'Done!'