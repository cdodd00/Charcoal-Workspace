import maya.cmds as mc
import xpy_stringLib as sl
'''
Creates simple ik handle. 
Select first and last joint, ik ctrl, and pv ctrl

returns ik handle and end effector
'''
def simpleIk(startJt=[],endJt=[],ctrls=[]):
	
	if not startJt:
		
		sel= mc.ls(sl=True)
		startJt.append(sel[0])
		endJt.append(sel[1])
		ctrls.append(sel[2])#leg/arm ik ct
		ctrls.append(sel[3])#knee/elbow(pv) ct
	
	side= sl.returnSide(startJt[0])
	name= sl.returnName(ctrls[0])
	
	legIkh= mc.ikHandle(sol='ikRPsolver', sj= startJt[0], ee= endJt[0],n= "{0}_{1}_ikh".format(side,name))
	endEf= mc.rename(legIkh[1], "{0}_{1}_endEff".format(side,name))
	mc.poleVectorConstraint(ctrls[1], legIkh[0], n= "{0}_{1}_pvConst".format(side,name))
	
	mc.parent(legIkh[0],ctrls[0])
	
	result= (legIkh[0],endEf)
	
	return result
	
if __name__=="__main__":
	#simpleIk(['l_leg01_jt'],['l_leg04_jt'],['l_leg_ct','l_knee_ct'])
	#simpleIk(['l_arm01_jt'],['l_arm04_jt'],['l_arm_ct','l_elbow_ct'])
	simpleIk()
	
	