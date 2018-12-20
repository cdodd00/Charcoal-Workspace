import maya.cmds as mc
import xpy_alignLib as al
import xpy_stringLib as sl
'''
creates aim const on the object to the ctrl.
select object to aim then ctrls
Uses a locator to maintain up direction. 
useful for eye setups
'''
def aimObj(object=[],ctrl=[],parentCt=[]):
	if not object:
		
		sel= mc.ls(sl=True)
		object.append(sel[0])#object to aim
		ctrl.append(sel[1])#object to aim at		
		parentCt.append(sel[2])#parent object for 'up' locs
	
	side= sl.returnSide(object[0])
	#create loc and move to position
	loc = mc.spaceLocator(name="{0}_up_loc#".format(side))
	al.alignTrans(loc,object)
	mc.move(1, loc[0], y=True, relative=True)
	#create aim const.
	mc.aimConstraint(ctrl[0], object[0], aimVector=(0,0,1), upVector=(0,1,0), worldUpType="object", worldUpObject=loc[0])
	#parent loc to 'parent' var and hide it
	mc.parent(loc[0], parentCt[0])
	mc.setAttr("{0}.v".format(loc[0]),0)
	

if __name__=="__main__":
	#aimObj(["l_eye_jt"],["l_eye_ct"],["c_head01_ct"])
	aimObj()