import maya.cmds as mc

def lockHideAttrs(object=[],attrs=""):
	
	if not object:

		object=mc.ls (sl = True)
		
	for o in object:
		
		for a in attrs:
			
			if a== 't':
			
				mc.setAttr("{0}.tx".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.ty".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.tz".format (o), lock=True, keyable=False, channelBox=False)
							
				# print "Locked and hid translates."
			
			elif a== 'r':
				
				mc.setAttr("{0}.rx".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.ry".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.rz".format (o), lock=True, keyable=False, channelBox=False)
				
				# print "Locked and hid rotates."
			
			elif a == 's':
				
				mc.setAttr("{0}.sx".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.sy".format (o), lock=True, keyable=False, channelBox=False)
				mc.setAttr("{0}.sz".format (o), lock=True, keyable=False, channelBox=False)
				
				# print "Locked and hid scales."
			
			else:#default attr, mostly used for "v" or visibility
				
				mc.setAttr("{0}.{1}".format (o,a), lock=True, keyable=False, channelBox=False)
				
				# print "Locked and hid {0} attr".format(a)

if __name__=="__main__":
	lockHideAttrs(attrs=['scaleX'])
			