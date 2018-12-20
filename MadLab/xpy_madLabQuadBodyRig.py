import maya.cmds as mc
import maya.mel as mel

import xpy_circleCt as cct
import xpy_ctrlConst as ccon
import xpy_zeroGp as zgp
import xpy_alignLib as al
import xpy_fkCtChain as chain
import xpy_aimObject as aim
import xpy_ikLib as ik
import xpy_footSetup as ft
import xpy_ikFkBlend as ikFk
import xpy_lockHideAttrs as lock

def madLab_quadBodyRig(rigFile=" "):
    #base file folder path, actual file passed in 'rigFile'
    baseFile = "C:/Users/chanc/Documents/Sync/mobile maya/madLab_Project/scenes/"
    
    #open joint base file
    mc.file (baseFile + rigFile, force=True, type="mayaAscii", open=True)
    
    #common variables 
    globalCtSize= 17
    
    centerHipSize= 4
    centerHipY= 2
    centerHipZ= 0
    
    spineCtSize= 3.5
    spineCtScale=.95
    
    headPosCtSize= 3
    headPosAxis= 'y'
    headPosX= 0 
    headPosY= 2
    headPosZ= 5
    
    tailCtSize= 0
    tailCtScale= .85
       
    wingCtSize= -.75
    wingCtScale= .9
    
    clavCtSize= 2.5
    clavCtDist= 2.5
    
    armCtSize= 3
    elbowCtSize= 1.5
    handCtSize=2.8
    handCtDist= 1.5
    
    hipCtSize=3
    hipCtDist= 3
    
    legCtSize= 3.2
    kneeCtSize= 1.5
    footCtSize= 3
    footCtDist= 1.5
    
    sides = ['l','r']
    
    #create global ct
    globCt= mc.circle (c= (0,0,0), nr= (0,1,0), sw= 360, r= globalCtSize, d= 3, ut= 0, tol= 0.01, s= 12, ch= 1, n="global_ct")
    globCtGp= zgp.zeroGp([globCt[0]])
    
    #create root ct curve and parent constrain join to it
    mel.eval('source x_curveLib.mel')
    rootCrv = 'crvCtrl("box","c_root_ct",8)'#create box crv
    rootCt= mel.eval(rootCrv)#run mel command
    rootCtShp= mc.listRelatives(rootCt, s=True)#get shape node of curve
    rootCtShp= mc.rename (rootCtShp, "{0}Shape".format(rootCt))#rename it to match transform name+'Shape'
    al.alignTrans([rootCt],["c_root_jt"])
    rootCtGp = zgp.zeroGp([rootCt])
    mc.parentConstraint(rootCt, "c_root_jt",mo=True)
    mc.parent (rootCtGp, globCt)
    
    #hip control
    centerHipJt= mc.ls("c_hip_end",type= "joint")
    ctrHipCt= ccon.ctrlConst(centerHipJt, radius= centerHipSize, axis= 'z')
    mc.setAttr(ctrHipCt[1] + ".sections", 3)
    mc.setAttr(ctrHipCt[1] + ".centerY", centerHipY)
    mc.setAttr(ctrHipCt[1] + ".centerZ", centerHipZ)
    ctrHipCtGp= mc.listRelatives(ctrHipCt[0], p=True)#get parent gp
    mc.parent(ctrHipCtGp, rootCt)#parent c_hip_ct_gp to root ct
    ctrHipCtShp= mc.listRelatives(ctrHipCt, s=True)
    
    #setup spine,head,jaw
    spineJts = mc.ls("c_spine*" + "_jt",type= "joint")
        
    spineCtrls= chain.fkCtChain(spineJts,startSize= spineCtSize,scaleFactor= spineCtScale)
    spineCtGp= mc.listRelatives(spineCtrls[0], p=True)
    mc.parent(spineCtGp, rootCt)
    
    spineCtrlsShp=[]#get shape nodes to add to layer
    for sc in spineCtrls:
        spineCtrlsShp.extend(mc.listRelatives(sc, s=True))
        
    #head pos ctrl
    headPosJt= mc.ls("headPos_end", type="joint")
    headPosCt= ccon.ctrlConst(headPosJt, radius= headPosCtSize, axis= headPosAxis)
    mc.setAttr(headPosCt[1] + ".sections", 3)
    mc.setAttr(headPosCt[1] + ".centerY", headPosY)
    mc.setAttr(headPosCt[1] + ".centerX", headPosX)
    mc.setAttr(headPosCt[1] + ".centerZ", headPosZ)
    headPosCtGp= mc.listRelatives(headPosCt[0], p=True)#get parent gp
    mc.parent(headPosCtGp, spineCtrls[3])#parent c_hip_ct_gp to root ct
    headPosCtShp= mc.listRelatives(headPosCt, s=True)
    
    #tail ctrls
    tailJts= mc.ls("c_tail*" + "_jt",type="joint")
    tailCtrls= chain.fkCtChain(tailJts,startSize= tailCtSize,scaleFactor= tailCtScale)
    tailCtGp= mc.listRelatives(tailCtrls[0], p=True)
    mc.parent (tailCtGp, rootCt)
    '''
    #wing ctrls
    for s in sides:
        wingJts= mc.ls("{0}_wing*".format(s) + "*_jt", type='joint')
        #wingCt= ccon.ctrlConst(wingJts,radius= wingCtSize)
        wingCtrls= chain.fkCtChain(wingJts,startSize= wingCtSize,scaleFactor= wingCtScale)
    '''   
    #clav and hip ctrls
    for s in sides:
        hipJt= mc.ls("{0}_hip_jt".format(s), type='joint')
        clavJt= mc.ls("{0}_clav_jt".format(s), type='joint')
        hipCt= ccon.ctrlConst(hipJt,radius= hipCtSize)#left and right hip
        mc.setAttr(hipCt[1]+ ".centerX", hipCtDist)
        if s=='r':
            mc.setAttr(hipCt[1]+ ".centerX",(hipCtDist*-1))
        clavCt= ccon.ctrlConst(clavJt,radius= clavCtSize)#clav
        mc.setAttr(clavCt[1]+ ".centerX", clavCtDist)
        if s=='r':
            mc.setAttr(clavCt[1]+ ".centerX",(clavCtDist*-1))
            
        hipCtGp= mc.listRelatives(hipCt[0], p=True)#parent left/right hip ctrls to ctr hip ct
        mc.parent(hipCtGp, ctrHipCt)
        
        clavCtGp= mc.listRelatives(clavCt[0], p=True)#parent left/right clav ctrls to spine03 ct
        mc.parent(clavCtGp, spineCtrls[2])      
        
    #arms setup
    for s in sides:
        #arm ctrls
        armJts= mc.ls("{0}_arm*".format(s),type='joint')
        wristJt= armJts[2]
        armCt= cct.circleCt([wristJt],axis='y',radius= armCtSize)
        armCt= mc.rename(armCt[0], "{0}_arm_ct".format(s))
        if s=='r':
            mc.setAttr("{0}.s".format(armCt),-1,-1,-1)
        armCtGp= zgp.zeroGp([armCt])
        #pv ct
        elbowJt= armJts[1]
        elbowCt= cct.circleCt([elbowJt],axis='z',radius= elbowCtSize)
        elbowCt= mc.rename(elbowCt[0], "{0}_elbow_ct".format(s))
        if s=='r':
            mc.setAttr("{0}.s".format(elbowCt),-1,-1,-1)
        elbowCtGp= zgp.zeroGp([elbowCt])
        mc.parent (elbowCtGp, armCt)
                
        #hand ct
        handJt = armJts[len(armJts)-2]
        handCt = cct.circleCt([handJt],axis='x',radius= handCtSize,degree=1)
        mc.setAttr(handCt[1] + ".centerX", handCtDist)
        if s=='r':
            mc.setAttr(handCt[1] + ".centerX", (handCtDist*-1))
        handCt= mc.rename(handCt[0], "{0}_hand_ct".format(s))
        handCtGp= zgp.zeroGp([handCt])
        
        ikFk.ikFkBlend([armJts[0]], [armCt], [globCt[0]])
        
        #ikh and foot setup
        armIkJts= mc.ls("{0}_arm*".format(s)+"_ik", type='joint')
        armIkh= ik.simpleIk([armIkJts[0]],[armIkJts[2]],[armCt, elbowCt])#create arm ik's
        ft.footSetup([armCt], [handCt],[ armIkh[0]], [armIkJts[2],armIkJts[3],armIkJts[4]]) 
    
        #leg setup
    for s in sides:
        #leg ctrls
        legJts= mc.ls("{0}_leg*".format(s),type='joint')
        ankleJt= legJts[3]
        legCt= cct.circleCt([ankleJt],axis='y',radius= legCtSize)
        legCt= mc.rename(legCt[0], "{0}_leg_ct".format(s))
        if s=='r':
            mc.setAttr("{0}.s".format(legCt),-1,-1,-1)
        legCtGp= zgp.zeroGp([legCt])
        
        #pv ct
        kneeJt= legJts[1]
        kneeCt= cct.circleCt([kneeJt],axis='x',radius= kneeCtSize)
        kneeCt= mc.rename(kneeCt[0], "{0}_knee_ct".format(s))
        
        if s=='r':
            mc.setAttr("{0}.s".format(kneeCt),-1,-1,-1)
        kneeCtGp= zgp.zeroGp([kneeCt])
        mc.parent(kneeCtGp, legCt)
        
        #foot ct
        footJt = legJts[len(legJts)-2]
        footCt = cct.circleCt([footJt],axis='x',radius= footCtSize,degree=1)
        mc.setAttr(footCt[1] + ".centerX", footCtDist)
        if s=='r':
            mc.setAttr(footCt[1] + ".centerX", (footCtDist*-1))
        footCt= mc.rename(footCt[0], "{0}_foot_ct".format(s))
        footCtGp= zgp.zeroGp([footCt])
        #create ik fk joints for legs(back legs)
        ikFk.ikFkBlend([legJts[0]], [legCt], [globCt[0]])
    
        legIkJts= mc.ls("{0}_leg*".format(s)+"_ik", type='joint')
        legIkh= ik.simpleIk([legIkJts[0]], [legIkJts[3]], [legCt, kneeCt])#create leg ik's
        ft.footSetup([legCt], [footCt], [legIkh[0]], [legIkJts[3],legIkJts[4],legIkJts[5]])

    #Add ctrls to correct layers
    ctrLyrCtrls=[tailCtrls[0],rootCtShp,spineCtrlsShp,ctrHipCtShp,headPosCtShp]
    leftLyrCtrls=[mc.ls("l_*_ct"), mc.ls ('l_*_fk', type='joint')]
    rightLyrCtrls= [mc.ls("r_*_ct"), mc.ls ('r_*_fk', type='joint')]
    
    for ct in leftLyrCtrls:
        mc.editDisplayLayerMembers ( 'l_ctrls_lyr', ct,noRecurse=True)
    
    for ct in rightLyrCtrls:
        mc.editDisplayLayerMembers ( 'r_ctrls_lyr', ct,noRecurse=True)
            
    for ct in ctrLyrCtrls:
        mc.editDisplayLayerMembers ( 'c_ctrls_lyr', ct,noRecurse=True)
    
    #lock and hide attrs on controls
    #rotation controls
    rotCtrls= ["l_hand_ct","r_hand_ct","l_foot_ct","r_foot_ct",ctrHipCt[0]]
    lock.lockHideAttrs(tailCtrls,attrs=['t','s','v'])
    lock.lockHideAttrs(spineCtrls,attrs=['t','s','v'])
    lock.lockHideAttrs(rotCtrls,attrs=['t','s','v'])
    
    #translate controls
    posCtrls= ["l_elbow_ct","r_elbow_ct","l_knee_ct","r_knee_ct"]
    lock.lockHideAttrs(posCtrls,attrs=['r','s','v'])
    
    #trans and rot ctrls
    posRotCtrls= [rootCt,headPosCt[0],globCt[0], "l_arm_ct","r_arm_ct","l_leg_ct","r_leg_ct","l_clav_ct","r_clav_ct","l_hip_ct","r_hip_ct"]
    lock.lockHideAttrs(posRotCtrls,attrs=['s','v'])
    
    mc.select(cl=True)
    print ('\n'+"{0} Done!".format(rigFile))    
    return rigFile
    
if __name__=="__main__":
    madLab_quadBodyRig(r'spino/spino_02_rig.ma')