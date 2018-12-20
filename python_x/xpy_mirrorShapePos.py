import maya.cmds as mc

def x_mirrorShpPos (objects=[]):
    
    if not objects:
		
		objects= mc.ls (sl=True)
        
    #get makeNurb hist to edit radius attrs
    ct01His= mc.listHistory(objects[0])
    ct02His= mc.listHistory(objects[1])
    
    ct01MkNrb=[]#var to store ct01 makeNurb his
    for h in ct01His:
        if 'makeNurb' in h:#search items in his to find makeNurb hist. node.
            ct01MkNrb.append(h)
            
    for ct in ct01MkNrb:#get attrs
       cenX= mc.getAttr ("{0}.centerX".format(ct))
       cenY= mc.getAttr ("{0}.centerY".format(ct))
       cenZ= mc.getAttr ("{0}.centerZ".format(ct))
       ctRad= mc.getAttr ("{0}.radius".format(ct))
       ctDeg= mc.getAttr ("{0}.degree".format(ct))
       ctSect= mc.getAttr ("{0}.sections".format(ct))
    
    ct02MkNrb=[]#var to store ct02 makeNurb his
    for his in ct02His:
        if 'makeNurb' in his:#search items in his to find makeNurb hist. node.
            ct02MkNrb.append(his)
     
    mc.setAttr ("{0}.centerX".format(ct02MkNrb[0]), (cenX * -1))
    mc.setAttr ("{0}.centerY".format(ct02MkNrb[0]), cenY * -1)
    mc.setAttr ("{0}.centerZ".format(ct02MkNrb[0]), cenZ * -1)
    mc.setAttr ("{0}.radius".format(ct02MkNrb[0]), ctRad)
    mc.setAttr ("{0}.degree".format(ct02MkNrb[0]), ctDeg)
    mc.setAttr ("{0}.sections".format(ct02MkNrb[0]), ctSect)
    
if __name__=="__main__":
	x_mirrorShpPos()