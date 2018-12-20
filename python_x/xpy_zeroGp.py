import maya.cmds as mc
'''
select objects/ctrls to create a parent group to zero transforms
on passed object

Returns the new parent group
'''
#-------------

def zeroGp(ctrl=[]):

	if not ctrl:

		ctrl= mc.ls (sl = True)
		
	
	for obj in ctrl:
		
		#get parent of obj
		objParent = mc.listRelatives (obj, p= True)
		#create null set it up
		null = mc.group (empty = True, name = 'empty')
		mc.parent (null, obj, relative =True)
		null = mc.rename (null, (obj + '_gp#'))

		if objParent > 0:#obj has parent

			mc.parent (null, objParent)#parent obj back to original parent            
			mc.parent (obj, null)

		else:#child of world

			mc.parent (null, world = True)
			mc.parent (obj, null)

			mc.select (clear = True)

	newGroup = mc.listRelatives (ctrl, p=True)    
	return newGroup

if __name__=="__main__":
	zeroGp()