import maya.cmds as mc
import xpy_circleCt as cct
import xpy_zeroGp as zgp
'''
creates a simple fk style ctrl on selected objects and parent const.
the objects to the ctrl

Returns the ct transform index 0(evens) and makeNurb node at index 1(odds)
'''
def ctrlConst(object=[],radius=1,axis='x'):
	
	if not object:
		
		object= mc.ls(sl=True)
	
	result=[]
	#run circleCt on each item and parent constrain the object to the ct
	for o in object:
		ct = cct.circleCt([o], axis=axis, radius=radius, degree=1)
		
		mc.parentConstraint (ct[0],o)
		zgp.zeroGp([ct[0]])
		result.extend(ct)
		
	return result

if __name__=="__main__":
	ctrlConst(radius=3)