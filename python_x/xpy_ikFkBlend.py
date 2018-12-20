import maya.cmds as mc
import maya.mel as mel
import xpy_stringLib as sl
import xpy_fkCtChain as chain
import xpy_lockHideAttrs as lock
import xpy_fkCtrl as fkc
'''
Creates duplicates of selected joint for ik fk switching
Just select the first parent joint and it will duplicate
everything beneath it
Pass in parent joint, leg/arm ik ct, and ctrl to have switch attr added

'''
def ikFkBlend(prntJt=[],ctrl=[],switchCt=[]):
	
	if not prntJt:
		sel= mc.ls(sl=True)
		prntJt.append(sel[0])
		ctrl.append(sel[1])
		switchCt.append(sel[2])

	#bind jts, using dag searches for all connected not just the next child
	bndJts=mc.ls(prntJt[0],dag=True)
	side = sl.returnSide(prntJt[0])
	name = sl.returnName(ctrl[0])
	jtName= sl.returnName(prntJt[0])
	ikJts= []
	
	#create custom attr on switch ct and rev node for vis control
	mc.addAttr(switchCt,ln="{0}_{1}IkFkBlend".format(side,name),at='double',k=True,min=0,max=1,dv=1)
	
	revNode= mc.createNode('reverse', n="{0}_{1}CtVis_rev".format(side,name))
	mc.connectAttr("{0}.{1}_{2}IkFkBlend".format(switchCt[0],side,name) ,"{0}.inputX".format(revNode))
	
	
	#duplicate joints for ik joint chain	
	dupJts = mc.duplicate(prntJt[0],renameChildren=True, name ="{0}_{1}_ik".format(side,jtName))
	mc.select(dupJts[0], replace=True)
	mel.eval ('searchReplaceNames "_jt1" "_ik" "hierarchy"')
	mel.eval ('searchReplaceNames "_end1" "_ik" "hierarchy"')
	#grab ik joints in var	
	ikJts= mc.ls(dupJts[0],dag=True)
	
	#ikJts = mc.ls("{0}_{1}".format(side,name)+"*_ik",type="joint")
	
	#dup for fk joints
	dupJts = mc.duplicate(prntJt[0],renameChildren=True, name ="{0}_{1}_fk".format(side,jtName))
	mc.select(dupJts[0], replace=True)
	mel.eval ('searchReplaceNames "_jt1" "_fk" "hierarchy"')
	mel.eval ('searchReplaceNames "_end1" "_fk" "hierarchy"')
	#fk joints
	fkJts= mc.ls(dupJts[0],dag=True)
	
	#parent constrain original 'jt' joints to each new joint chain
	i=0
	
	for b in bndJts:
		parCon= mc.parentConstraint(ikJts[i],fkJts[i],bndJts[i])
		
		#setup switch control to parent const. weights
		mc.connectAttr("{0}.{1}_{2}IkFkBlend".format(switchCt[0],side,name),"{0}.{1}W0".format(parCon[0],ikJts[i]))
		mc.connectAttr("{0}.outputX".format(revNode),"{0}.{1}W1".format(parCon[0],fkJts[i]))
		
		i+=1
	
	#create fk ct curves
	fkCtrls=[]
	fkCtrls.extend(fkJts)
	fkCtrls=fkCtrls[:len(fkCtrls)-1]
	
	fkCtrls= fkc.fkCtrl(fkCtrls,axis='x',radius=2,degree=1)#attach shapes to the fk joints
	#fkCtrls= chain.fkCtChain(fkCtrls,startSize=-2,scaleFactor=.9)
	
	#setup vis for ctrls
	mc.connectAttr("{0}.outputX".format(revNode), "{0}.v".format(fkCtrls[0]))
	mc.connectAttr("{0}.{1}_{2}IkFkBlend".format(switchCt[0],side,name), "{0}.v".format(ctrl[0]))
	
	#hide fk ctrls attrs and ik fk joints
	lock.lockHideAttrs(fkCtrls,['t','s','v'])
	mc.setAttr("{0}.v".format(ikJts[0]),0)
	#mc.setAttr("{0}.v".format(fkJts[0]),0)
	
if __name__=="__main__":
	#ikFkBlend(["l_hip_jt"],["l_leg_ct"],["global_ct"])
	ikFkBlend()
	