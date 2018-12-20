import maya.cmds as mc
import xpy_alignLib as al
import xpy_stringLib as sl

'''
Creates nurbs circle, select or pass the object to create the ctrl for
Can set normal axis, radius, and degree (1 or 3) 

returns the created nurbs circle transform at even index i.e. 0,2,4etc.
and makeNurb node at odd index.
'''

def circleCt(object=[], axis='x', radius=2, degree=3):
	
	if not object:
		
		object=mc.ls (sl = True)
	
	result = []
	
	for o in object:
		#get side and name for each object
		side = sl.returnSide(o)
		name = sl.returnName(o)
		#create the crv and align it
		if axis =='x':
			
			ct = mc.circle (c= (0,0,0), nr= (1,0,0), sw= 360, r= radius, d= degree, ut= 0, tol= 0.01, s= 8, ch= 1, n = "{}_{}_ct".format(side,name))
			
			result.extend (ct)
			al.alignTrans([ct[0]],[o])
			al.alignRot([ct[0]],[o])
						
		elif axis =='y':
			
			ct = mc.circle (c= (0,0,0), nr= (0,1,0), sw= 360, r= radius, d= degree, ut= 0, tol= 0.01, s= 8, ch= 1, n = "{}_{}_ct".format(side,name))
			
			result.extend (ct)
			al.alignTrans([ct[0]],[o])
			al.alignRot([ct[0]],[o])
					
		elif axis =='z':
			
			ct = mc.circle (c= (0,0,0), nr= (0,0,1), sw= 360, r= radius, d= degree, ut= 0, tol= 0.01, s= 8, ch= 1, n = "{}_{}_ct".format(side,name))
			
			result.extend (ct)
			al.alignTrans([ct[0]],[o])
			al.alignRot([ct[0]],[o])
						
			
	mc.select(cl=True)
	
	return result
	
if __name__=="__main__":
	#circleCt(["l_arm02_jt","l_arm03_jt"])
	circleCt(axis='x')
	
	