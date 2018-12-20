import maya.cmds as mc

'''
Find diffent parts of names of objects
return the name, prefix, suffix etc. of object's name
Pass in string
'''

def returnSide(object=""):#returns first section of name i.e. prefix
	
	split = object.split ("_")
	side = split[0]
	# print "Side:'" + side + "'"
	return side

def returnName(object=""):#returns second section of string
	
	split= object.split ("_")
		
	if len(split)<3:
		
		name= split[0]
		
	else:
		
		name= split[1]
		
	# print "Name:'"+ name + "'"
	return name

if __name__=="__main__":
	returnName('l_test_ct')