import maya.cmds as mc
import xpy_ctrlConst as ctc

'''
select a joint chain to create fk style ctrls that are parented to each other
and the joints are parent constrained to the ctrls.
can pass in a start size and a scale factor to adj. size of the ctrls

returns new control transforms as list
'''

def fkCtChain(object=[],startSize=0,scaleFactor=.8):
	
	if not object:
		
		object= mc.ls(sl=True)
	
	fkCtrls=[]

	for o in object:
		#create the ctrl
		fk= ctc.ctrlConst([o])
		
		#store ctrls and groups in vars
		fkCtrls.append(fk[0])
		fkGp= mc.listRelatives (fkCtrls, parent=True)
		fkLen= len(fkCtrls)
		
		#parent groups to previous ctrls
		if fkLen >1:
			mc.parent(fkGp[fkLen-1], fkCtrls[fkLen-2])
			
	#get makeNurb hist to edit radius attrs
	his= mc.listHistory(fkCtrls)
	ctHis=[]#var to store makeNurb his
	for h in his:
		if 'makeNurb' in h:#search items in his to find makeNurb hist. node.
			ctHis.append (h)
		
	#make size of ctrls start bigger then get smaller towards end
	
	startSize+= len(ctHis)

	for c in ctHis:
		mc.setAttr("{0}.radius".format(c),startSize)
		startSize*=scaleFactor#multiply from initial size to make ctrls smaller
		
	mc.select(fkCtrls,replace=True)
	
	return fkCtrls

if __name__=="__main__":
	fkCtChain(startSize=1,scaleFactor=.9)
	