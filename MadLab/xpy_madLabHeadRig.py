def madLab_headRig (rigFile=" "):
    #base file folder path, actual file passed in 'rigFile'
    baseFile = "C:/Users/chanc/Documents/Sync/mobile maya/madLab_Project/scenes/"
    
    #open joint base file
    mc.file (baseFile + rigFile, force=True, type="mayaAscii", open=True)
    
    #control vars
    headCtSize=6
    headCtScale=.9
    
    tngCtSize= 0
    tngCtScale= .9
    
    eyeCtDist = 17
    mainEyeCtSize= 5.4
    eyeCtSize= 1.5
    
    sides = ['l','r']
    #setup head,jaw
    headJts= ["c_headBase_end","c_head01_jt","c_jaw01_jt"] 
    
    headCtrls= chain.fkCtChain(headJts,startSize= headCtSize,scaleFactor=headCtScale)
    jawCt= headCtrls[2]
    headCt= headCtrls[1]
   
    headCtrlsShp=[]#get shape nodes to add to layer
    for hc in headCtrls:
        headCtrlsShp.extend(mc.listRelatives(hc, s=True))
    
    #tng ctrls
    tngJts= mc.ls("c_tng*" + "_jt",type="joint")
    tngCtrls= chain.fkCtChain(tngJts,startSize= tngCtSize,scaleFactor=tngCtScale)
    topTng= mc.listRelatives(tngCtrls[0], p=True)#get tng01 gp
    mc.parent (topTng, jawCt)#parent tng01 gp to jaw ct
    
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
        mc.addAttr (eyeCt,ln= "upLid", k=True, at="double", min= 0, max= 10, dv= 0)
        mc.addAttr (eyeCt,ln= "loLid", k=True, at="double", min= 0, max= 10, dv= 0)
        mc.setAttr("{0}.tz".format(eyeCt[0]),mainEyeZ)
        mc.parent(eyeCt[0],mainEyeCt[0])
        eyeCtGp= zgp.zeroGp([eyeCt[0]])
        aim.aimObj([eyeJt[0]],[eyeCt[0]],["c_head01_ct"])
        
    #Add ctrls to correct layers
    headLyrCtrls= [headCtrlsShp]
    tngLyrCtrls=[topTng]
    eyeLyrCtrls= [mainEyeCt[0]]
    
    for tngCt in tngLyrCtrls:
        mc.editDisplayLayerMembers ( 'tngCtrls_lyr', tngCt,noRecurse=True)
    
    for eCt in eyeLyrCtrls:
        mc.editDisplayLayerMembers ( 'eyeCtrls_lyr', eCt,noRecurse=True)
            
    for hdCt in headLyrCtrls:
        mc.editDisplayLayerMembers ( 'headCtrls_lyr', hdCt,noRecurse=True)
    
    mc.select(cl=True)
    print ('\n'+"{0} Done!".format(rigFile))          
    return rigFile
        
if __name__=="__main__":
    madLab_headRig(r'spino\spinoHead_02_rig.ma')