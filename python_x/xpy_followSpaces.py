import maya.cmds as mc
import xpy_alignLib as al
import xpy_stringLib as sl

def follow(object=[],spaceCtrls=[],type='parent'):
    
    ctName= sl.returnName(object[0])
    ctSide = sl.returnSide(object[0])
    spaceNames=[]
    objectParent= mc.listRelatives(object, p=True)
    objectAllParent= mc.listRelatives(objectParent, p=True)

    for s in spaceCtrls:
        spaceNames.append(sl.returnName(s))

    #create parent loc
    ctLoc= mc.spaceLocator(n= "{0}_{1}Space_loc".format(ctSide,ctName))
    al.alignTrans(ctLoc,object)
    al.alignRot(ctLoc,object)
    mc.parent(objectParent, ctLoc)
    #if objects parent had a parent, parent the ct loc to that
    if objectAllParent:
        mc.parent(ctLoc, objectAllParent)
        
    #add a ':' to the space names list
    attrNames=[]
    for sp in spaceNames:
        attrNames.append("{0}:".format(sp))
        
    #turn list into string and remove extra char's
    attrNames= str(attrNames)
    attrNames= attrNames.replace("\'","")
    attrNames= attrNames.replace(",","")
    attrNames= attrNames.replace(" ","")
    attrNames= attrNames.replace("[","")
    attrNames= attrNames.replace("]","")
    
    #create follow attr on object
    mc.addAttr(object, ln='follow', k=1, at='enum',en=attrNames)
    
    #create locs for each ctrl space
    spaceLocs=[]#list of locators for the different spaces
    for ct in spaceCtrls:
        loc= mc.spaceLocator(n= "{0}Space_loc".format(ct))
        al.alignTrans(loc,[ct])
        al.alignRot(loc,[ct])
        mc.parent(loc, ct)
        spaceLocs.append(loc) 
        
    #parent constrain ct loc to space locs
    const=[]#var for created constraint
    constWts=[]#var for const weights
    for spLoc in spaceLocs: 
        if type=='parent':
            const= mc.parentConstraint(spLoc,ctLoc,mo=True)
            constWts= mc.parentConstraint(const, q=True, wal=True)
        elif type=='orient':
            const= mc.orientConstraint(spLoc,ctLoc,mo=True)
            constWts= mc.orientConstraint(const, q=True, wal=True)
            
    for weight in constWts:#set all parent weight values to 0
        mc.setAttr("{0}.{1}".format(const[0],weight),0)
       
    for r in range(len(constWts)):
        mc.setAttr("{0}.follow".format(object[0]),r)#set follow attr
        
        for weight in constWts:#key all weights for current follow to 0
            mc.setDrivenKeyframe ("{0}.{1}".format(const[0],weight), v= 0, cd= "{0}.follow".format(object[0]))
        #key only current weight const value to 1
        mc.setDrivenKeyframe ("{0}.{1}".format(const[0],constWts[r]), v= 1, cd= "{0}.follow".format(object[0]))
    
    #clean up
    for loc in spaceLocs:
        mc.setAttr("{0}.v".format(loc[0]),0)
    
    mc.setAttr("{0}Shape.localScaleX".format(ctLoc[0]),0)
    mc.setAttr("{0}Shape.localScaleY".format(ctLoc[0]),0)
    mc.setAttr("{0}Shape.localScaleZ".format(ctLoc[0]),0)
    mc.setAttr("{0}Shape.template".format(ctLoc[0]),1)
    
    mc.setAttr("{0}.follow".format(object[0]),0)
    mc.select(cl=True)
    
    print ('\n'+"Spaces Created for {0}!".format(object[0]))
    
if __name__=="__main__":
    follow(['l_follow_ct'],['c_main_ct','c_head_ct','global_ct'],type='parent')
    