# vizard imports
import viz
import vizjoy
import vizshape
# python imports
import math
import random
import time
import pdb

MATCH_DISTANCE = .5

class Move:
	NONE=0
	RIGHT=1
	LEFT=2
	FORWARD=3
	BACK=4
	UP=5
	DOWN=6
	
class Rotate:
	NONE=0
	CW=1
	CCW=2
	
class Navigation:
	walk = Move.NONE
	strafe = Move.NONE
	fly = Move.NONE
	yaw = Rotate.NONE
	pitch = Rotate.NONE
	roll = Rotate.NONE
	TRANSLATION_SPEED = 10
	ROTATION_SPEED = 30
	rotation_speed = ROTATION_SPEED
	translation_speed = TRANSLATION_SPEED
	walk_speed = TRANSLATION_SPEED
	strafe_speed = TRANSLATION_SPEED
	half_speed = False

class Colors:
	BLACK       = [0.0,0.0,0.0]
	WHITE       = [1.0,1.0,1.0]
	RED         = [1.0,0.0,0.0]
	GREEN       = [0.0,1.0,0.0]
	BLUE        = [0.0,0.0,1.0]
	YELLOW      = [1.0,1.0,0.0]
	ORANGE      = [1.0,0.5,0.0]
	GREY        = [0.5,0.5,0.5]
	LIGHT_GREY  = [0.75,0.75,0.75]
	DARK_GREY   = [0.25,0.25,0.25]
	LIGHT_BLUE  = [0.2,0.5,0.9]
	
	highlight    = YELLOW
	puzzleEmpty  = LIGHT_GREY
	puzzleFilled = GREEN

class Attr:
	puzzleIndices = [-1 for i in range(5)] #used to identify spaces to be marked filled/unfilled
	placed = False #used to determine win

#-------------------------------------------------------------------------------
# createQuad(left_bot,left_top,right_bot,right_top)
#-------------------------------------------------------------------------------
def createQuad(left_bot,left_top,right_bot,right_top):
	viz.startlayer(viz.QUADS) 
	viz.vertexcolor(0,0,0)
	viz.vertex(left_bot)
	viz.vertex(left_top)
	viz.vertex(right_top)
	viz.vertex(right_bot)
	return viz.endlayer()

#-------------------------------------------------------------------------------
# createSolidBox(min,max)
#-------------------------------------------------------------------------------
def createSolidBox(min,max):
	viz.startlayer(viz.QUADS, 'top') 
	viz.vertexcolor(1.0,0.5,0.0)
	
	#top
	#viz.vertexcolor(0.0,1.0,0.0)
	viz.normal(0,1,0)
	viz.vertex( max[0], max[1], min[2])
	viz.vertex( min[0], max[1], min[2])
	viz.vertex( min[0], max[1], max[2])
	viz.vertex( max[0], max[1], max[2])

	viz.startlayer(viz.QUADS,'bottom') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#bottom
	#viz.vertexcolor(1.0,0.5,0.0)
	viz.normal(0,-1,0)
	viz.vertex( max[0], min[1], max[2])
	viz.vertex( min[0], min[1], max[2])
	viz.vertex( min[0], min[1], min[2])
	viz.vertex( max[0], min[1], min[2])

	viz.startlayer(viz.QUADS,'front') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#front
	#viz.vertexcolor(1.0,0.0,0.0)
	viz.normal(0,0,1)
	viz.vertex( max[0], max[1], max[2])
	viz.vertex( min[0], max[1], max[2])
	viz.vertex( min[0], min[1], max[2])
	viz.vertex( max[0], min[1], max[2])

	viz.startlayer(viz.QUADS,'back') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#back
	#viz.vertexcolor(1.0,1.0,0.0)
	viz.normal(0,0,-1)
	viz.vertex( max[0], min[1], min[2])
	viz.vertex( min[0], min[1], min[2])
	viz.vertex( min[0], max[1], min[2])
	viz.vertex( max[0], max[1], min[2])

	viz.startlayer(viz.QUADS,'left') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#left
	#viz.vertexcolor(0.0,0.0,1.0)		
	viz.normal(-1,0,0)
	viz.vertex( min[0], max[1], max[2])	
	viz.vertex( min[0], max[1], min[2])	
	viz.vertex( min[0], min[1], min[2])	
	viz.vertex( min[0], min[1], max[2])	

	viz.startlayer(viz.QUADS,'right') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#right
	#viz.vertexcolor(1.0,0.0,1.0)
	viz.normal(1,0,0)
	viz.vertex( max[0], max[1], min[2])	
	viz.vertex( max[0], max[1], max[2])	
	viz.vertex( max[0], min[1], max[2])	
	viz.vertex( max[0], min[1], min[2])	
	
	return viz.endlayer()

#-------------------------------------------------------------------------------
# createWireBox(min,max)
#-------------------------------------------------------------------------------
def createWireBox(min,max):
	viz.startlayer(viz.LINE_LOOP, 'top') 
	viz.vertexcolor(0.0,0.0,0.0)
	viz.linewidth(2.0)
	
	#top
	#viz.vertexcolor(0.0,1.0,0.0)
	#viz.normal(0,1,0)
	viz.vertex( max[0], max[1], min[2])
	viz.vertex( min[0], max[1], min[2])
	viz.vertex( min[0], max[1], max[2])
	viz.vertex( max[0], max[1], max[2])

	viz.startlayer(viz.LINE_LOOP,'bottom') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#bottom
	#viz.vertexcolor(1.0,0.5,0.0)
	#viz.normal(0,-1,0)
	viz.vertex( max[0], min[1], max[2])
	viz.vertex( min[0], min[1], max[2])
	viz.vertex( min[0], min[1], min[2])
	viz.vertex( max[0], min[1], min[2])

	viz.startlayer(viz.LINE_LOOP,'front') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#front
	#viz.vertexcolor(1.0,0.0,0.0)
	#viz.normal(0,0,1)
	viz.vertex( max[0], max[1], max[2])
	viz.vertex( min[0], max[1], max[2])
	viz.vertex( min[0], min[1], max[2])
	viz.vertex( max[0], min[1], max[2])

	viz.startlayer(viz.LINE_LOOP,'back') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#back
	#viz.vertexcolor(1.0,1.0,0.0)
	#viz.normal(0,0,-1)
	viz.vertex( max[0], min[1], min[2])
	viz.vertex( min[0], min[1], min[2])
	viz.vertex( min[0], max[1], min[2])
	viz.vertex( max[0], max[1], min[2])

	viz.startlayer(viz.LINE_LOOP,'left') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#left
	#viz.vertexcolor(0.0,0.0,1.0)		
	#viz.normal(-1,0,0)
	viz.vertex( min[0], max[1], max[2])	
	viz.vertex( min[0], max[1], min[2])	
	viz.vertex( min[0], min[1], min[2])	
	viz.vertex( min[0], min[1], max[2])	

	viz.startlayer(viz.LINE_LOOP,'right') 
	viz.vertexcolor(.5,.5,0.0)
	viz.linewidth(2.0)
	
	#right
	#viz.vertexcolor(1.0,0.0,1.0)
	#viz.normal(1,0,0)
	viz.vertex( max[0], max[1], min[2])	
	viz.vertex( max[0], max[1], max[2])	
	viz.vertex( max[0], min[1], max[2])	
	viz.vertex( max[0], min[1], min[2])	
	
	return viz.endlayer()

#-------------------------------------------------------------------------------
# createPuzzleCube()
#-------------------------------------------------------------------------------
def createPuzzleCube(boxR=1,boxG=1,boxB=1,outR=0,outG=0,outB=0):	
	# create the solid box
	box = createSolidBox([-0.5,-0.5,-0.5],[0.5,0.5,0.5])
	box.color(boxR,boxG,boxB)
	box.alpha(0.8)
	
	# create the box outline
	wire = createWireBox([-0.5,-0.5,-0.5],[0.5,0.5,0.5])
	wire.parent(box)
	wire.color(outR,outG,outB)
	wire.alpha(1.0)
	
	return box

#-------------------------------------------------------------------------------
# buildPuzzle(x,y,z)
#-------------------------------------------------------------------------------
def buildPuzzle(x,y,z):
	global shape
	global blockState
	global pieces
	global pieceAttr
	global placeable
	
	placeable = False
	blockState = []
	pieceAttr = []
	
	#Build puzzle space
	for i in range(x):
		for j in range(y):
			for k in range(z):
				box = createSolidBox([-0.5,-0.5,-0.5],[0.5,0.5,0.5])
				box.color(Colors.LIGHT_GREY)
				box.alpha(0.0)
				box.parent(shape)
				box.setPosition([0.5+i,0.5+j,0.5+k])
				blockState.append(False)
	wire = createWireBox([-1.5,-1.5,-1.5],[1.5,1.5,1.5])
	wire.color(0,0,0)
	wire.alpha(1.0)
	wire.setPosition([1.5, 1.5, 1.5])

	# piece 1 - L shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+2.0,0.5])
	piece1.setPosition([-3.0,0.0,0.0])
	pieces.append(piece1)
				
	# piece 2 - T shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5-1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	piece1.setPosition([-6.0,0.0,0.0])
	pieces.append(piece1)
				
	# piece 3 - small L shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	piece1.setPosition([-10.0,0.0,0.0])
	pieces.append(piece1)
				
	# piece 4 - Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5-1.0,0.5+1.0,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	piece1.setPosition([-13.0,0.0,0.0])
	pieces.append(piece1)
				
	# piece 5 - curved Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5-1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	piece1.setPosition([-17.0,0.0,0.0])
	pieces.append(piece1)
				
	# piece 6 - curved Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5+1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5+1.0])
	piece1.setPosition([7.0,0.0,0.0])
	pieces.append(piece1)
	
	# piece 7 - curved T shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5+1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	piece1.setPosition([4.0,0.0,0.0])
	pieces.append(piece1)
	
	#build the parallel pieceAttrs (piece attributes) array
	for p in pieces:
		tmp = Attr()
		tmp.puzzleIndices = [-1 for i in range( len(p.getChildren()) )]
		pieceAttr.append(tmp)
	
#-------------------------------------------------------------------------------
# buildSideBar()
#-------------------------------------------------------------------------------
def buildSideBar():
	global pieces
	global sidebar
	global sidebarBG
				
	# piece 1 - L shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+2.0,0.5])
	sidebar.append(piece1)
				
	# piece 2 - T shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5-1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	sidebar.append(piece1)
				
	# piece 3 - small L shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	sidebar.append(piece1)
				
	# piece 4 - Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5-1.0,0.5+1.0,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	sidebar.append(piece1)
				
	# piece 5 - curved Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5-1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	sidebar.append(piece1)
				
	# piece 6 - curved Z shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5+1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5+1.0])
	sidebar.append(piece1)
	
	# piece 7 - curved T shaped
	piece1 = viz.add(viz.GROUP,viz.WORLD)
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5+1.0,0.5,0.5])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5,0.5+1.0])
	box = createPuzzleCube(0.2,0.5,0.8)
	box.parent(piece1)
	box.setPosition([0.5,0.5+1.0,0.5])
	sidebar.append(piece1)
	
#-------------------------------------------------------------------------------
# keyDown(whichKey)
#-------------------------------------------------------------------------------
def keyDown(whichKey):
	global debug
	global cursorPos
	global highlightedObj
	global highlightedObjType
	global selectedObj
	global selectedObjType
	global selectedIndex
	global blockState
	
	#print 'The following key was pressed: ', whichKey
	
	if whichKey == 'x':
		debug = not debug

	# navigation
	if whichKey == viz.KEY_UP:
		viz.MainView.move(0,0,Navigation.translation_speed*viz.elapsed(),viz.BODY_ORI)
	elif whichKey == viz.KEY_DOWN:
		viz.MainView.move(0,0,-Navigation.translation_speed*viz.elapsed(),viz.BODY_ORI)
	if whichKey == viz.KEY_LEFT:
		Navigation.yaw = Rotate.CCW
	elif whichKey == viz.KEY_RIGHT:
		Navigation.yaw = Rotate.CW
	if whichKey == ']':
		Navigation.pitch = Rotate.CCW
	elif whichKey == '[':
		Navigation.pitch = Rotate.CW
	if whichKey == '}':
		Navigation.roll = Rotate.CCW
	elif whichKey == '{':
		Navigation.roll = Rotate.CW
	if whichKey == 'i':
		Navigation.fly = Move.UP
	elif whichKey == 'k':
		Navigation.fly = Move.DOWN
		
	# cursor
	if whichKey == 'w':
		cursorPos[1] += 0.05 
	elif whichKey == 's':
		cursorPos[1] -= 0.05
	if whichKey == 'a':
		cursorPos[0] -= 0.05 
	elif whichKey == 'd':
		cursorPos[0] += 0.05
	if whichKey == 'e':
		cursorPos[2] += 0.05 
	elif whichKey == 'q':
		cursorPos[2] -= 0.05
		
	# selection
	if whichKey == viz.KEY_RETURN:
		#picking a piece up
		if selectedObj == None and highlightedObj != None:
			if highlightedObjType == 'piece':
				for i in pieceAttr[selectedIndex].puzzleIndices:
					blockState[i] = False
				selectedObj = highlightedObj
				selectedObjType = highlightedObjType
				selectedIndex = pieces.index(selectedObj)
				pieceAttr[selectedIndex].placed = False

		# piece placement (try to drop a piece)
		elif selectedObj != None:
			if place_piece(): 
				check_for_win()
				selectedObj = None
				selectedObjType = None
				selectedIndex = -1
	# selection #2 (up/down piece selection)
	if whichKey == 'm':
		cycle_select(forward = True)
	elif whichKey == 'n':
		cycle_select(forward = False)
		
	
	# translation of the selected object is done by moving the cursor
	# orientation
	if selectedObj != None:
		if whichKey == 't':
			selectedObj.setEuler(0,90,0,viz.REL_LOCAL)#yaw,pitch,roll
		elif whichKey == 'g':
			selectedObj.setEuler(0,-90,0,viz.REL_LOCAL)#yaw,pitch,roll
		if whichKey == 'f':
			selectedObj.setEuler(90,0,0,viz.REL_LOCAL)#yaw,pitch,roll
		elif whichKey == 'h':
			selectedObj.setEuler(-90,0,0,viz.REL_LOCAL)#yaw,pitch,roll
		if whichKey == 'y':
			selectedObj.setEuler(0,0,90,viz.REL_LOCAL)#yaw,pitch,roll
		elif whichKey == 'r':
			selectedObj.setEuler(0,0,-90,viz.REL_LOCAL)#yaw,pitch,roll

#-------------------------------------------------------------------------------
# cycle_select
#-------------------------------------------------------------------------------
def cycle_select(forward = True):
	global selectedObj
	global selectedIndex
	global selectedObjType
	global pieces
	global pieceAttr
	
	if forward:
		while True:
			selectedIndex += 1
			if selectedIndex >= len(pieces):
				selectedIndex = -1
				break
			if not pieceAttr[selectedIndex].placed:
				break
	else:
		while True:
			selectedIndex -= 1
			if selectedIndex < -1:
				selectedIndex = len(pieces)
				continue
			if selectedIndex == -1:
				break
			if not pieceAttr[selectedIndex].placed:
				break
	if selectedIndex == -1:
		selectedObj.setPosition([25, 25, 25], viz.ABS_GLOBAL)
		selectedObj.visible(False)
		selectedObj = None
		selectedObjType = None
	else:
		if selectedObj != None:
			selectedObj.setPosition([25, 25, 25], viz.ABS_GLOBAL)
			selectedObj.visible(False)
		selectedObj = pieces[selectedIndex]
		selectedObj.visible(True)
		selectedObjType = 'piece'

#-------------------------------------------------------------------------------
# keyUp(whichKey)
#-------------------------------------------------------------------------------
def keyUp(whichKey):
	#print 'The following key was released: ', whichKey
	if whichKey == viz.KEY_UP or whichKey == viz.KEY_DOWN:
		Navigation.walk = Move.NONE
	if whichKey == viz.KEY_LEFT or whichKey == viz.KEY_RIGHT:
		Navigation.yaw = Rotate.NONE
	if whichKey == ']' or whichKey == '[':
		Navigation.pitch = Rotate.NONE
	if whichKey == '}' or whichKey == '{':
		Navigation.roll = Rotate.NONE
	if whichKey == 'i' or whichKey == 'k':
		Navigation.fly = Move.NONE

#-------------------------------------------------------------------------------
# place_piece
#-------------------------------------------------------------------------------
def place_piece():
	global selectedObj
	global blockState
	global deltaVector
	global stateIndices
	global placeable

	if selectedObj != None:
		if placeable:
			pieceAttr[selectedIndex].placed = True
			for i in pieceAttr[selectedIndex].puzzleIndices:
				blockState[i] = True
			for block in selectedObj.getChildren():
				block.color(Colors.GREEN)
			pos = selectedObj.getPosition(viz.ABS_GLOBAL)
			selectedObj.setPosition([pos[0]+deltaVector[0], pos[1]+deltaVector[1], pos[2]+deltaVector[2]], viz.ABS_GLOBAL)
			return True
	return False
	
#-------------------------------------------------------------------------------
# check_for_win
#-------------------------------------------------------------------------------
def check_for_win():
	global blockState
	global won
	count = 0
	for p in pieceAttr:
		if p.placed is not True:
			print count
			return False
		count += 1
	print "You win"
	won = True

#-------------------------------------------------------------------------------
# updateView()
#-------------------------------------------------------------------------------
def updateView():
	if Navigation.walk == Move.FORWARD:
		viz.MainView.move(0,0,Navigation.translation_speed*viz.elapsed(),viz.BODY_ORI)
	elif Navigation.walk == Move.BACK: 
		viz.MainView.move(0,0,-Navigation.translation_speed*viz.elapsed(),viz.BODY_ORI)
	
	if Navigation.yaw == Rotate.CW: #right
		viz.MainView.setEuler([Navigation.rotation_speed*viz.elapsed()*2.0,0,0],viz.BODY_ORI,viz.REL_PARENT)
	elif Navigation.yaw == Rotate.CCW: #left
		viz.MainView.setEuler([-Navigation.rotation_speed*viz.elapsed()*2.0,0,0],viz.BODY_ORI,viz.REL_PARENT)
		
	if Navigation.pitch == Rotate.CW: #down
		viz.MainView.setEuler([0,Navigation.rotation_speed*viz.elapsed(),0],viz.HEAD_ORI,viz.REL_LOCAL)
	elif Navigation.pitch == Rotate.CCW: #up
		viz.MainView.setEuler([0,-Navigation.rotation_speed*viz.elapsed(),0],viz.HEAD_ORI,viz.REL_LOCAL)
	
	if Navigation.roll == Rotate.CW: #right
		viz.MainView.setEuler([0,0,Navigation.rotation_speed*viz.elapsed()],viz.HEAD_ORI,viz.REL_LOCAL)
	elif Navigation.roll == Rotate.CCW: #left
		viz.MainView.setEuler([0,0,-Navigation.rotation_speed*viz.elapsed()],viz.HEAD_ORI,viz.REL_LOCAL)

	if Navigation.fly == Move.UP:
		viz.MainView.move(0,Navigation.TRANSLATION_SPEED/2*viz.elapsed(),0,viz.BODY_ORI)
	elif Navigation.fly == Move.DOWN:
		viz.MainView.move(0,-Navigation.TRANSLATION_SPEED/2*viz.elapsed(),0,viz.BODY_ORI)
			
#-------------------------------------------------------------------------------
# updateCursor()
#-------------------------------------------------------------------------------
def updateCursor():
	global cursor
	global cursorPos
	global shape
	global highlightedObj
	global highlightedObjType
	global selectedObj
	global selectedObjType
	global selectedIndex
	global deltaVector
	global blockState
	global pieceAttr
	global placeable

	# update cursor position
	cursor.setMatrix(viz.MainView.getMatrix(), viz.ABS_GLOBAL)
	cursor.setPosition(cursorPos, viz.REL_LOCAL)
	absPos = cursor.getPosition(viz.ABS_GLOBAL)

	# Using the Cursor
	if selectedObj == None:
		# check if cursor is inside any of the pieces
		highlightedObj = None
		highlightedObjType = None
		isInside = False
		for i, piece in enumerate(pieces):
			children = piece.getChildren()
			
			# have to check each one of the individual boxes of the piece
			for box in children:
				pos = box.getPosition(viz.ABS_GLOBAL)
				if absPos[0] >= pos[0]-0.5 and absPos[0] <= pos[0]+0.5 and absPos[1] >= pos[1]-0.5 and absPos[1] <= pos[1]+0.5 and absPos[2] >= pos[2]-0.5 and absPos[2] <= pos[2]+0.5:
					isInside = True
					highlightedObj = piece
					highlightedObjType = 'piece'
					#selectedIndex = i
					break
			
			# if the cursor is inside any of the boxes, highlight them all
			if isInside == True or piece == selectedObj:
				for box in children:
					box.color(Colors.highlight)
				break
			else:
				for box in children:
					box.color(Colors.LIGHT_BLUE)

	#Dragging a piece
	else:
		placeable = True
		deltaVector = [10,10,10]
		
		#check each block of the piece against each box in the puzzle space
		for i, pieceBox in enumerate(selectedObj.getChildren()):
			pbc = pieceBox.getBoundingBox(viz.ABS_GLOBAL).center
			pieceAttr[selectedIndex].puzzleIndices[i] = -1
			for j, shapeBox in enumerate(shape.getChildren()):
				sbc = shapeBox.getBoundingBox(viz.ABS_GLOBAL).center
				vec = [sbc[0]-pbc[0], sbc[1]-pbc[1], sbc[2]-pbc[2]]
				mag = magnitude(vec)
				if mag <= MATCH_DISTANCE and blockState[j] != True:
					pieceAttr[selectedIndex].puzzleIndices[i] = j
					if mag < magnitude(deltaVector): 
						deltaVector = vec #everything is orthogonal, so all vectors will be the same size
					break
			if pieceAttr[selectedIndex].puzzleIndices[i] == -1:
				#box is outsize of puzzle or in an already filled space
				placeable = False
				pieceBox.color(Colors.RED)
				
		if placeable:
			for box in selectedObj.getChildren():
				box.color(Colors.highlight)
			
def magnitude(vec):
	return math.sqrt( (vec[0]*vec[0]) + (vec[1]*vec[1]) + (vec[2]*vec[2]))

#-------------------------------------------------------------------------------
# updateSelectedObj()
#-------------------------------------------------------------------------------
def updateSelectedObj():
	global cursor
	global selectedObj
	global selectedObjType
	global deltaVector
	global placeable

	# update selected object position
	if selectedObj != None:
		selectedObj.setPosition(0,0,0,viz.ABS_GLOBAL)
		cpos = cursor.getPosition(viz.ABS_GLOBAL)
		center = selectedObj.getBoundingBox(viz.ABS_GLOBAL).center
		selectedObj.setPosition([cpos[0]-center[0],cpos[1]-center[1],cpos[2]-center[2]], viz.ABS_GLOBAL)


#-------------------------------------------------------------------------------
# updateSideBar()
#-------------------------------------------------------------------------------
def updateSideBar():
	global sidebar
	global sidebarBG
	global animRot
	global identity
	
	# start off by setting up the background based on the current user's position
	user_position = viz.MainView.getPosition()
	distance = 100
	
	line = viz.screentoworld(0.85,1.0)
	dir_vector = line.dir
	length = math.sqrt(dir_vector[0]*dir_vector[0] + dir_vector[1]*dir_vector[1] + dir_vector[2]*dir_vector[2])
	dir_vector = (dir_vector[0]/length),(dir_vector[1]/length),(dir_vector[2]/length)
	left_top = [user_position[0]+dir_vector[0]*distance,user_position[1]+dir_vector[1]*distance,user_position[2]+dir_vector[2]*distance]
	
	line = viz.screentoworld(0.85,0.0)
	dir_vector = line.dir
	length = math.sqrt(dir_vector[0]*dir_vector[0] + dir_vector[1]*dir_vector[1] + dir_vector[2]*dir_vector[2])
	dir_vector = (dir_vector[0]/length),(dir_vector[1]/length),(dir_vector[2]/length)
	left_bot = [user_position[0]+dir_vector[0]*distance,user_position[1]+dir_vector[1]*distance,user_position[2]+dir_vector[2]*distance]
	
	line = viz.screentoworld(1.0,1.0)
	dir_vector = line.dir
	length = math.sqrt(dir_vector[0]*dir_vector[0] + dir_vector[1]*dir_vector[1] + dir_vector[2]*dir_vector[2])
	dir_vector = (dir_vector[0]/length),(dir_vector[1]/length),(dir_vector[2]/length)
	right_top = [user_position[0]+dir_vector[0]*distance,user_position[1]+dir_vector[1]*distance,user_position[2]+dir_vector[2]*distance]
	
	line = viz.screentoworld(1.0,0.0)
	dir_vector = line.dir
	length = math.sqrt(dir_vector[0]*dir_vector[0] + dir_vector[1]*dir_vector[1] + dir_vector[2]*dir_vector[2])
	dir_vector = (dir_vector[0]/length),(dir_vector[1]/length),(dir_vector[2]/length)
	right_bot = [user_position[0]+dir_vector[0]*distance,user_position[1]+dir_vector[1]*distance,user_position[2]+dir_vector[2]*distance]
	
	sidebarBG.setVertex(0, left_top)
	sidebarBG.setVertex(1, left_bot)
	sidebarBG.setVertex(2, right_bot)
	sidebarBG.setVertex(3, right_top)	
	
	# set color and alpha of the background
	sidebarBG.color(0.0,0.0,0.0)
	sidebarBG.alpha(0.6)
	
	# update rotation variable
	animRot += .5
	if animRot == 360:
		animRot = 0
	
	# get the window height
	windowHeight = viz.MainWindow.getSize(viz.WINDOW_NORMALIZED)[1]
	# calculate the distance between each item in that list with a margin
	itemOffset = windowHeight / len(sidebar)
	
	# for each item in the sidebar, update rotation animation and place them where they belong in the sidebar
	itemIndex = 0
	for i, item in enumerate(sidebar):
		# make sure we draw this after everything else in the scene indenpendently of the depth buffer
		item.depthFunc(viz.GL_ALWAYS)
		item.drawOrder(101)
		# reset the transformation matrix and apply rotation
		item.setMatrix(identity,viz.ABS_GLOBAL)
		item.setAxisAngle(-.5,1,0,animRot+30*itemIndex)
		# calculate the position of the item on the sidebar
		center = item.getBoundingBox(viz.ABS_GLOBAL).center
		line = viz.screentoworld(0.925,0.925-itemIndex*itemOffset)
		dirVector = line.dir
		length = math.sqrt(dirVector[0]*dirVector[0] + dirVector[1]*dirVector[1] + dirVector[2]*dirVector[2])
		dirVector[0] = (dirVector[0]/length)
		dirVector[1] = (dirVector[1]/length)
		dirVector[2] = (dirVector[2]/length)
		distance = 50
		point = [user_position[0]+dirVector[0]*distance,user_position[1]+dirVector[1]*distance,user_position[2]+dirVector[2]*distance]
		item.setPosition(point[0]-center[0],point[1]-center[1],point[2]-center[2],viz.ABS_GLOBAL)
		# change color - not working
		#if blockState[itemIndex] == True:
		#	for box in item.getChildren():
		#		box.color(Colors.highlight)
		#else:
		#	for box in item.getChildren():
		#		box.color(Colors.LIGHT_BLUE)
		c = Colors.LIGHT_BLUE
		if i == selectedIndex: 
			c = Colors.highlight
		elif pieceAttr[i].placed:
			c = Colors.LIGHT_GREY
		for box in item.getChildren():
				box.color(c)
		itemIndex += 1
	

#-------------------------------------------------------------------------------
# update()
# This function is called every iteration of the main loop.
# Include here any function you need to run in the main loop.
#-------------------------------------------------------------------------------
def update():
	global won
	
	updateView()
	updateCursor()
	updateSelectedObj()
	updateSideBar()
	if won:
		pass #should do something fun here

#-------------------------------------------------------------------------------
# main()
#-------------------------------------------------------------------------------
def main():
	# global variables
	global debug
	global pieces
	global shape
	global sidebar
	global sidebarBG
	global blockState
	global cursor
	global cursorPos
	global highlightedObj
	global highlightedObjType
	global selectedObj
	global selectedObjType
	global animRot
	global identity
	global selectedIndex
	global won
	
	#---------------------------------------------------------------------------
	# init vizard
	
	# initialize pdb if debugging is needed
	#pdb.set_trace()

	# set the maximum frame rate to something lower than the minimum the application runs
	# so that the FPS is constant throughout the run
	viz.setOption('viz.max_frame_rate','60')
	
	# set the full screen monitor to 1
	viz.setOption('viz.fullscreen.monitor',2)  

	# start in full screen
	#viz.go(viz.FULLSCREEN)
	viz.go()

	# set cursor visibility
	#viz.mouse.setVisible(viz.OFF)

	# enable backface culling
	viz.enable(viz.CULL_FACE)
	
	# set clear color for raster
	viz.clearcolor(Colors.WHITE)

	#---------------------------------------------------------------------------
	# init variables
	
	# flag to toggle debug breakpoints - Use 'x' to toggle
	debug = False
	
	# list of pieces available
	pieces = []
	
	# won the game
	won = False
	
	# group with all cubes in their final position - read from file
	shape = viz.add(viz.GROUP,viz.WORLD)
	
	# input file with description of pieces and
	#input_file = open('puzzle.txt','r')
	#parseInputFile(input_file)	
	# since we still don't have an input format, we build the puzzle manually
	buildPuzzle(3,3,3)
	
	# create sidebar to indicate existing pieces/possibilities
	sidebar = []
	sidebarBG = createQuad([0,0,0],[0,0,0],[0,0,0],[0,0,0])
	sidebarBG.depthFunc(viz.GL_ALWAYS)
	sidebarBG.drawOrder(100)
	buildSideBar()
	
	animRot = 0

	identity = vizmat.Transform()
	identity.makeIdent()
	
	cursor = vizshape.addSphere(radius=0.2)
	cursor.color(Colors.LIGHT_BLUE)
	cursorPos = [0.0,0.0,3.0]
	
	selectedObj = None
	selectedObjType = None
	selectedIndex = -1
	highlightedObj = None
	highlightedObjType = None
	
	# assign keyDown and keyUp as callback functions for events
	viz.callback(viz.KEYDOWN_EVENT, keyDown)
	viz.callback(viz.KEYUP_EVENT, keyUp)

	# register the update function to be called every iteration of the main loop
	vizact.ontimer(0,update)
		
if __name__ == "__main__":
	main()
#viz.mouse(viz.ON)
