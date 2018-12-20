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

def quadRig(rigFile=" "):
    #base file folder path, actual file passed in 'rigFile'
    baseFile = "C:/Users/chanc/Documents/Sync/mobile maya/drgnmnz_Project/scenes"
    
    #open joint base file
    mc.file (baseFile + rigFile, force=True, type="mayaAscii", open=True)
    
    #common variables 
    globalCtSize= 12
    
    spineCtSize= 0
    spineCtScale=.9
    
    tngCtSize= -1.5
    tngCtScale= .9
    
    tailCtSize= -3.8
    tailCtScale= .9
    
    eyeCtDist = 11
    mainEyeCtSize= 2.5
    eyeCtSize= 1
    
    wingCtSize= -.75
    wingCtScale= .9
    
    clavCtSize= 2.75
    armCtSize= 2
    elbowCtSize= 1.5
    handCtSize=2
    
    hipCtSize=3
    legCtSize= 2.25
    kneeCtSize= 1.5
    footCtSize= 2

    sides = ['l','r']
    
    #create global ct
    globCt= mc.circle (c= (0,0,0), nr= (0,1,0), sw= 360, r= globalCtSize, d= 3, ut= 0, tol= 0.01, s= 12, ch= 1, n="global_ct")
    globCtGp= zgp.zeroGp([globCt[0]])
    
    #create root ct curve and parent constrain join to it
    mel.eval('source x_curveLib.mel')
    rootCrv = 'crvCtrl("box","c_root_ct",6)'#create box crv
    rootCt= mel.eval(rootCrv)#run mel command
    rootCtShp= mc.listRelatives(rootCt, s=True)#get shape node of curve
    rootCtShp= mc.rename (rootCtShp, "{0}Shape".format(rootCt))#rename it to match transform name+'Shape'
    al.alignTrans([rootCt],["c_root_jt"])
    rootCtGp = zgp.zeroGp([rootCt])
    mc.parentConstraint(rootCt, "c_root_jt",mo=True)
    
    #setup spine,head,jaw
    spineJts = mc.ls("c_spine*" + "_jt",type= "joint")
    #spineJts.append ("c_neck01_jt")#add head joint for ct setup
    spineJts.append ("c_head01_jt")#add head joint for ct setup
    spineJts.append ("c_jaw01_jt")#add jaw joint for ct setup
    spineCtrls= chain.fkCtChain(spineJts,startSize= spineCtSize,scaleFactor= spineCtScale)
    jawCt= spineCtrls[len(spineCtrls)-1]
    headCt= spineCtrls[len(spineCtrls)-2]
    
    spineCtrlsShp=[]#get shape nodes to add to layer
    for sc in spineCtrls:
        spineCtrlsShp.extend(mc.listRelatives(sc, s=True))
    
    #tng ctrls
    tngJts= mc.ls("c_tng*" + "_jt",type="joint")
    tngCtrls= chain.fkCtChain(tngJts,startSize= tngCtSize,scaleFactor= tngCtScale)
    topTng= mc.listRelatives(tngCtrls[0], p=True)#get tng01 gp
    mc.parent (topTng, jawCt)#parent tng01 gp to jaw ct
    
    #tail ctrls
    tailJts= mc.ls("c_tail*" + "_jt",type="joint")
    tailCtrls= chain.fkCtChain(tailJts,startSize= tailCtSize,scaleFactor= tailCtScale)
    #grn rooster tails
    '''
    leftTailJts= mc.ls("l_tail*" + "_jt",type="joint")
    leftTailCtrls= chain.fkCtChain(leftTailJts,startSize= tailCtSize,scaleFactor= tailCtScale)
    rightTailJts= mc.ls("r_tail*" + "_jt",type="joint")
    rightTailCtrls= chain.fkCtChain(rightTailJts,startSize= tailCtSize,scaleFactor= tailCtScale)
    '''
    #setup eye ctrls
    #main eye ct
    mainEyeCt= cct.circleCt(["c_eye_end"],axis='z',radius= mainEyeCtSize)
    mainEyeZ= mc.getAttr("{0}.tz".format(mainEyeCt[0]))
    mc.setAttr("{0}.tz".format(mainEyeCt[0]),mainEyeZ+eyeCtDist)
    mainEyeZ= mc.getAttr("{0}.tz".format(mainEyeCt[0]))
    mainEyeCtShp= mc.listRelatives(mainEyeCt[0], s=True)
    mainEyeCtGp=zgp.zeroGp([mainEyeCt[0]])
    mc.parent(mainEyeCtGp, headCt)#parent main eye ct gp to head ct
    
    #l and r ctrls for eyes
    for s in sides:
        eyeJt= mc.ls("{0}_eye_jt".format(s), type='joint')
        eyeCt= cct.circleCt(eyeJt,axis='z',radius= eyeCtSize)
        mc.setAttr("{0}.tz".format(eyeCt[0]),mainEyeZ)
        mc.parent(eyeCt[0],mainEyeCt[0])
        eyeCtGp= zgp.zeroGp([eyeCt[0]])
        aim.aimObj([eyeJt[0]],[eyeCt[0]],["c_head01_ct"])
    
    #wing ctrls
    for s in sides:
        wingJts= mc.ls("{0}_wing*".format(s) + "*_jt", type='joint')
        #wingCt= ccon.ctrlConst(wingJts,radius= wingCtSize)
        wingCtrls= chain.fkCtChain(wingJts,startSize= wingCtSize,scaleFactor= wingCtScale)
        
    #clav and hip ctrls
    for s in sides:
        hipJt= mc.ls("{0}_hip_jt".format(s), type='joint')
        clavJt= mc.ls("{0}_clav_jt".format(s), type='joint')
        ccon.ctrlConst(hipJt,radius= hipCtSize)
        ccon.ctrlConst(clavJt,radius= clavCtSize)
        
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
        '''Had to move elbow ct behind arm on prp toad rig'''
        #mc.move(-.1, elbowCt, moveY=True, os=True, r=True)
        
        #hand ct
        handJt = armJts[len(armJts)-2]
        handCt = cct.circleCt([handJt],axis='x',radius= handCtSize,degree=1)
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
        ankleJt= legJts[2]
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
        '''Had to move knee ct behind leg on red hyena rig'''
        #mc.move(-1, kneeCt, moveY=True, os=True, r=True)
        
        #foot ct
        footJt = legJts[len(legJts)-2]
        footCt = cct.circleCt([footJt],axis='x',radius= footCtSize,degree=1)
        footCt= mc.rename(footCt[0], "{0}_foot_ct".format(s))
        footCtGp= zgp.zeroGp([footCt])
        #create ik fk joints for legs(back legs)
        ikFk.ikFkBlend([legJts[0]], [legCt], [globCt[0]])
    
        legIkJts= mc.ls("{0}_leg*".format(s)+"_ik", type='joint')
        legIkh= ik.simpleIk([legIkJts[0]], [legIkJts[3]], [legCt, kneeCt])#create leg ik's
        ft.footSetup([legCt], [footCt], [legIkh[0]], [legIkJts[2],legIkJts[3],legIkJts[4]])

    #Add ctrls to correct layers
    ctrLyrCtrls=[tailCtrls[0],rootCtShp,spineCtrlsShp,tngCtrls[0],mainEyeCtShp]
    leftLyrCtrls=[mc.ls("l_*_ct"), mc.ls ('l_*_fk', type='joint')]
    rightLyrCtrls= [mc.ls("r_*_ct"), mc.ls ('r_*_fk', type='joint')]
    
    for ct in leftLyrCtrls:
        mc.editDisplayLayerMembers ( 'l_ctrls_lyr', ct,noRecurse=True)
    
    for ct in rightLyrCtrls:
        mc.editDisplayLayerMembers ( 'r_ctrls_lyr', ct,noRecurse=True)
            
    for ct in ctrLyrCtrls:
        mc.editDisplayLayerMembers ( 'c_ctrls_lyr', ct,noRecurse=True)
        
    mc.select(cl=True)
    print ('\n'+"{0} Done!".format(rigFile))    
    return rigFile
    
if __name__=="__main__":
    quadRig(r'grnRstr/grnRstr_02_rig.ma')