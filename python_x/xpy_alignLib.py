import maya.cmds as mc

'''
aligns the first selected or passed in object to the second.
parents the obj to the source, set attrs to zero then unparents

returns the orginal objects
'''

#aling tranlates, parent unparent method returns child object
def alignTrans(obj=[],source=[]):
	
	if not source:
				
		sel=mc.ls (sl = True)
		obj.append(sel[0])
		source.append(sel[1])
		

	mc.parent(obj[0], source[0])
	mc.setAttr ("{0}.t".format (obj[0]), 0,0,0)
	mc.parent (obj[0], w=True)
	
	return obj
	
#aling rotates, parent unparent method, returns child object
def alignRot(obj=[],source=[]):
	
	if not obj:
		
		sel=mc.ls (sl = True)
		obj.append(sel[0])
		source.append(sel[1])
	
	mc.parent(obj[0], source[0])
	mc.setAttr ("{0}.r".format (obj[0]), 0,0,0)
	mc.parent (obj[0], w=True)
	
	return obj
	
if __name__ == "__main__":
	#alignTrans()
	alignRot()