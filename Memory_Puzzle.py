# -*- coding: utf-8 -*-
import random,pygame,sys
from pygame.locals import *

FPS = 30          
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

BOARD_WIDTH = 4
BOARD_HEGIHT = 5
BOXSIZE = 40
GAPSIZE = 10

REVEALSPEED = 4




assert (BOARD_HEGIHT*BOARD_WIDTH) % 2 == 0 ,'断言,格子总数必须是偶数'

XMARGIN = (WINDOW_WIDTH - (BOARD_HEGIHT*(BOXSIZE+GAPSIZE)))/2   #屏幕水平方向边缘的空白像素数
YMARGIN = (WINDOW_HEIGHT-(BOARD_HEGIHT*(BOXSIZE+GAPSIZE)))/2    #屏幕竖直方向边缘的空白像素数

assert XMARGIN > 0 and YMARGIN > 0 ,'断言,屏幕必须足够大' 

GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PUPPLE = (255,0,255)
CYAN = (0,255,255)

BG_COLOR = NAVYBLUE
LIGHTBG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED,GREEN,BLUE,YELLOW,ORANGE,PUPPLE,CYAN)
ALLSHAPES = (DONUT,SQUARE,DIAMOND,LINES,OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARD_WIDTH * BOARD_HEGIHT,'断言,要有足够的颜色与形状来表示'



		


def leftTopCoordsOfBox(box_x,box_y):       #给定一个对应的方块坐标，返回它左上角的坐标 
	left = box_x*(BOXSIZE+GAPSIZE)+XMARGIN
	top = box_y*(BOXSIZE+GAPSIZE)+YMARGIN
	return (left,top)

def getBoxAtPixel(x,y):        #给定一个坐标，返回对应的方块坐标
	for box_x in range(BOARD_WIDTH):
		for box_y in range(BOARD_HEGIHT):
			left,top = leftTopCoordsOfBox(box_x,box_y)
			boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(x,y):
				return (box_x,box_y)
	return (None,None)

def drawIcon(shape,color,box_x,box_y):
	quarter = int(BOXSIZE*0.25)
	half = int(BOXSIZE*0.5)
	left,top = leftTopCoordsOfBox(box_x,box_y)
	if shape == DONUT:
		pygame.draw.circle(DISPLAYSURF,color,(left+half,top+half),half-5)
		pygame.draw.circle(DISPLAYSURF,BG_COLOR,(left+half,top+half),quarter-5)
	elif shape == SQUARE:
		pygame.draw.rect(DISPLAYSURF,color,(left+quarter,top+quarter,BOXSIZE-half,BOXSIZE-half))
	elif shape == DIAMOND:
		pygame.draw.polygon(DISPLAYSURF,color,((left+half,top),(left+BOXSIZE-1,top+half),(left+half,top+BOXSIZE-1),(left,top+half)))
	elif shape == LINES:
		for i in range(0,BOXSIZE,4):
			pygame.draw.line(DISPLAYSURF,color,(left,top+i),(left+i,top))
			pygame.draw.line(DISPLAYSURF,color,(left+i,top+BOXSIZE-1),(left+BOXSIZE-1,top+i))
	elif shape == OVAL:
		pygame.draw.ellipse(DISPLAYSURF,color,(left,top+quarter,BOXSIZE,half))

def getShapeAndColor(board,box_x,box_y):
	return board[box_x][box_y][0],board[box_x][box_y][1]

def drawBoxCovers(board,boxes,coverage):
	for box in boxes:
		left,top = leftTopCoordsOfBox(box[0],box[1])
		pygame.draw.rect(DISPLAYSURF,BG_COLOR,(left,top,BOXSIZE,BOXSIZE))
		shape,color = getShapeAndColor(board,box[0],box[1])
		drawIcon(shape,color,box[0],box[1])
		if coverage > 0:
			pygame.draw.rect(DISPLAYSURF,BOX_COLOR,(left,top,coverage,BOXSIZE))
	pygame.display.update()
	FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
	for coverage in range(BOXSIZE,-1,-REVEALSPEED):
		drawBoxCovers(board,boxesToReveal,coverage)

def coverBoxesAnimation(board,boxesToCover):
	for coverage in range(0,BOXSIZE+REVEALSPEED,REVEALSPEED):
		drawBoxCovers(board,boxesToCover,coverage)

def drawBoard(board,revealed):
	for box_x in range(BOARD_WIDTH):
		for box_y in range(BOARD_HEGIHT):
			left,top = leftTopCoordsOfBox(box_x,box_y)
			if not revealed[box_x][box_y]:
				pygame.draw.rect(DISPLAYSURF,BOX_COLOR,(left,top,BOXSIZE,BOXSIZE))
			else:
				shape,color = getShapeAndColor(board,box_x,box_y)
				drawIcon(shape,color,box_x,box_y)

def drawHighlightBox(box_x,box_y):
	left,top = leftTopCoordsOfBox(box_x,box_y)
	pygame.draw.rect(DISPLAYSURF,HIGHLIGHT_COLOR,(left-5,top-5,BOXSIZE+10,BOXSIZE+10),4)
	
def startGameAnimation(board,coveredBoxes):
	def splitIntoGroupOf(groupSize,theList):   #将列表按给定长度分割成列表的列表
		result = []
		for i in range(0,len(theList),groupSize):
			result.append(theList[i:i+groupSize])
		return result
	coveredBoxes = generateRevealedBoxesData()
	boxes = []
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_HEGIHT):
			boxes.append((x,y))
	random.shuffle(boxes)
	boxGroups = splitIntoGroupOf(8,boxes)
	drawBoard(board,coveredBoxes)
	for boxGroup in boxGroups:
		revealBoxesAnimation(board,boxGroup)
		coverBoxesAnimation(board,boxGroup)

def gameWonAnimation(board,coveredBoxes):
	color1 = LIGHTBG_COLOR
	color2 = BG_COLOR
	for i in range(13):
		color1,color2 = color2,color1
		DISPLAYSURF.fill(color1)
		drawBoard(board,coveredBoxes)
		pygame.display.update()
		pygame.time.wait(300)

def hasWon(revealedBoxes):
	for i in revealedBoxes:
		if False in i:
			return False
	return True


def generateRevealedBoxesData():  #生成一个全为False的二维列表，用来表示方块是否翻开
	revealedBoxes = []
	for i in range(BOARD_WIDTH):
		revealedBoxes.append([False]*BOARD_HEGIHT)
	return revealedBoxes

def getRandomizedBoard():  #得到游戏需要的随机版块，返回的类型为[[(shape,color)]],里层board_hegiht个，外层board_width个
	icons = []
	for color in ALLCOLORS:
		for shape in ALLSHAPES:
			icons.append((shape,color))
	random.shuffle(icons)  #原地打乱列表的顺序，使游戏板元素具有随机性
	numIconUsed = BOARD_HEGIHT*BOARD_WIDTH / 2
	icons = icons[:numIconUsed]*2  #取出需要的数量，每一种元素生成两份
	random.shuffle(icons)
	board = []    #创建一个二维列表，第一维表示行，第二维表示列，来表示整个游戏板上的元素
	for x in range(BOARD_WIDTH):
		column = []
		for y in range(BOARD_HEGIHT):
			column.append(icons[0])
			del icons[0]
		board.append(column)  
	return board
	
	



def main():
	global FPSCLOCK,DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
	pygame.display.set_caption('记忆游戏')
	mainBoard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData()
	mousex = 0
	mousey = 0
	firstSelection = None
	startGameAnimation(mainBoard,revealedBoxes)
	
	while True:
		mouseClicked = False
		
		DISPLAYSURF.fill(BG_COLOR)
		drawBoard(mainBoard,revealedBoxes)
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
				mouseClicked = True
			
			box_x,box_y = getBoxAtPixel(mousex,mousey)
			if box_x != None and box_y != None:
				if not revealedBoxes[box_x][box_y]:
					drawHighlightBox(box_x,box_y)
					if mouseClicked:
						revealBoxesAnimation(mainBoard,[(box_x,box_y)])
						revealedBoxes[box_x][box_y] = True
						if firstSelection == None:
							firstSelection = (box_x,box_y)
						else:
							icon1shape,icon1color = getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
							icon2shape,icon2color = getShapeAndColor(mainBoard,box_x,box_y)
							if icon1color != icon2color or icon1shape != icon2shape:
								pygame.time.wait(1000)
								coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(box_x,box_y)])
								revealedBoxes[firstSelection[0]][firstSelection[1]] = False
								revealedBoxes[box_x][box_y] = False
							elif hasWon(revealedBoxes):
								gameWonAnimation(mainBoard,revealedBoxes)
								pygame.time.wait(2000)
								
								mainBoard = getRandomizedBoard()
								revealedBoxes = generateRevealedBoxesData(False)
								
								drawBoard(mainBoard,revealedBoxes)
								pygame.display.update()
								pygame.time.wait(1000)
								startGameAnimation(mainBoard)
							firstSelection = None
		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	main()