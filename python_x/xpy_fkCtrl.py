import maya.cmds as mc
import xpy_circleCt as cir
import xpy_lockHideAttrs as lock
'''
select or pass a list of joints/objects to create a nurbs circle
and parent the shape to the joint
Can pass in normal, radius size and 1 or 3 for degree of circle
returns the shape that was attached.
'''
#----------------------
def fkCtrl(object=[], axis='x', radius=2, degree=3):
	if not object:
		
		object = mc.ls (selection = True)
	
	result=[]
	
	for o in object:
		
		fkCt= cir.circleCt([o],axis=axis,radius=radius,degree=degree)
		mc.parent ("{0}Shape".format(fkCt[0]), o, r=True, s=True)
		result.append(o)
		mc.delete (fkCt[0])#delete just the empty transform
		
		if mc.ls(o, type='joint'):
			lock.lockHideAttrs([o],['radi'])
					
	return result
	
if __name__=="__main__":
	#fkCtrl(['l_arm01_jt','l_arm03_jt'],degree=1,radius=2)
	fkCtrl()
	
		
		
