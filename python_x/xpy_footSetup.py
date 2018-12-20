import maya.cmds as mc

import xpy_alignLib as al
import xpy_stringLib as sl
'''
need leg/arm ik ct, foot/hand ct, ikh, ankle/wrist,
ball/wrist, and toe/hand_end joints
and leg/arm ikh already created.
'''
def footSetup(legCt=[],footCt=[],legIkh=[],joints=[]):
	if not legCt:
		sel= mc.ls(sl=True)
		legCt.append(sel[0])
		footCt.append(sel[1])
		legIkh.append(sel[2])
		joints.extend([sel[3],sel[4],sel[5]])#extend to add a list of objects to a new list
	
	side= sl.returnSide(legCt[0])
	name= sl.returnName(legCt[0])
	#legIkh= mc.ls ("{0}_{1}_ikh".format(side, name), type='ikHandle')
	mc.setAttr("{0}.v".format(legIkh[0]),0)
	#heel loc
	heelLoc=mc.spaceLocator(name="{0}_{1}Rot01_loc".format(side,name))
	al.alignRot([heelLoc[0]],[legCt])
	al.alignTrans([heelLoc[0]],[legCt])
	mc.parent(heelLoc[0], legCt)
	mc.setAttr("{0}Shape.localScale".format(heelLoc[0]), 2,2,2)
	#ball loc
	ballLoc=mc.spaceLocator(name="{0}_{1}Rot02_loc".format(side,name))
	al.alignRot([ballLoc[0]],[legCt[0]])
	al.alignTrans([ballLoc[0]],[joints[1]])
	mc.parent(ballLoc[0], legCt)
	mc.parent(legIkh, ballLoc[0])#parent original leg ikh to loc
	mc.setAttr("{0}Shape.localScale".format(ballLoc[0]), 0,0,0)
	
	#ball ikh
	ballIkh= mc.ikHandle(sol='ikRPsolver', sj=joints[0], ee=joints[1], n="{0}_{1}Rot01_ikh".format(side,name))
	foot01Eef= mc.rename(ballIkh[1], "{0}_{1}Rot01_endEff".format(side,name))
	mc.parent(ballIkh[0], ballLoc[0])
	mc.setAttr("{0}.v".format(ballIkh[0]),0)
	
	#toe ikh
	toeIkh= mc.ikHandle(sol='ikRPsolver', sj=joints[1], ee=joints[2], n="{0}_{1}Rot02_ikh".format(side,name))
	foot02Eef= mc.rename(toeIkh[1], "{0}_{1}Rot02_endEff".format(side,name))
	mc.parent(toeIkh[0], footCt)
	mc.setAttr("{0}.v".format(toeIkh[0]),0)
	
	#create driver drivens
	mc.addAttr (legCt, ln="heel", at= 'double', k=True, min= -100, max= 100, dv=0)

	mc.setDrivenKeyframe ("{0}.rz".format(heelLoc[0]), dv= 0, v= 0, cd= "{0}.heel".format(legCt[0]))
	mc.setDrivenKeyframe ("{0}.rz".format(heelLoc[0]), dv= 100, v= 100, cd= "{0}.heel".format(legCt[0]))
	mc.setDrivenKeyframe ("{0}.rz".format(ballLoc[0]), dv= 0, v= 0, cd= "{0}.heel".format(legCt[0]))
	mc.setDrivenKeyframe ("{0}.rz".format(ballLoc[0]), dv= -100, v= -100, cd= "{0}.heel".format(legCt[0]))
	
	mc.select(heelLoc[0],r=True)
	
if __name__=="__main__":
	#footSetup(['l_leg_ct'],['l_foot_ct'],['l_leg_ikh'],['l_leg04_ik','l_leg05_ik','l_leg06_ik'])
	#footSetup(['l_arm_ct'],['l_hand_ct'],['l_arm_ikh'],['l_arm04_ik','l_arm05_ik','l_arm06_ik'])
	footSetup()