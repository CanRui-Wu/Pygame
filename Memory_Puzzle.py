# -*- coding: utf-8 -*-
import random,pygame,sys
from pygame.locals import *

#以下定义了一些颜色与形状的全局变量
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



class Game(object):
	def getRandomizedBoard(self,board_width,board_hegiht):  #得到游戏需要的随机版块，返回的类型为Box组成的列表
		icons = []
		for color in ALLCOLORS:
			for shape in ALLSHAPES:
				icons.append((shape,color))
		random.shuffle(icons)  #原地打乱列表的顺序，使游戏板元素具有随机性
		numIconUsed = board_hegiht*board_width / 2
		icons = icons[:numIconUsed]*2  #取出需要的数量，每一种元素生成两份
		random.shuffle(icons)
		board = []    #用来生成一个由width*height个Box对象组成的列表
		XMARGIN = (self.window_width-(self.board_width*(self.box_size+self.gap_size)))/2   #屏幕水平方向边缘的空白像素数
		YMARGIN = (self.window_height-(self.board_height*(self.box_size+self.gap_size)))/2    #屏幕竖直方向边缘的空白像素数
		for x in range(board_width):
			for y in range(board_hegiht):
				box = Box(x,y,icons[0][0],icons[0][1],self.box_size,self.gap_size,XMARGIN,YMARGIN)
				del icons[0]
				board.append(box)  
		return board
	
	def __init__(self):
		self.fps = 30          
		self.window_width = 640
		self.window_height = 480
		self.board_width = 5
		self.board_height = 6
		self.box_size = 40
		self.gap_size = 10
		self.reveal_speed = 4
		self.mainBoard = self.getRandomizedBoard(self.board_width,self.board_height)
	

class Box(object):
	def __init__(self,x,y,shape,color,size,gap_size,XMARGIN,YMARGIN):
		self.x = x
		self.y = y
		self.size = size
		self.gap_size = gap_size
		self.shape = shape
		self.color = color
		self.revealed = False
		self.XMARGIN = XMARGIN
		self.YMARGIN = YMARGIN
		self.left,self.top = self.get_lefttop_coord()
		
	def get_lefttop_coord(self):
		left = self.x*(self.size+self.gap_size)+self.XMARGIN
		top = self.y*(self.size+self.gap_size)+self.YMARGIN
		return (left,top)

class Handler(object):
	def __init__(self,game):
		self.board_width = game.board_width
		self.board_height = game.board_height
		self.mainBoard = game.mainBoard
		self.box_size = game.box_size
		self.gap_size = game.gap_size
		self.reveal_speed = game.reveal_speed
		self.DISPLAYSURF = pygame.display.set_mode((game.window_width,game.window_height))
		self.FPSCLOCK = pygame.time.Clock()
		self.fps = game.fps
	def drawIcon(self,box):
		quarter = int(self.box_size*0.25)
		half = int(self.box_size*0.5)
		left = box.left
		top = box.top
		color = box.color
		shape = box.shape
		BOXSIZE = box.size
		DISPLAYSURF = self.DISPLAYSURF
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
			
	def drawBoard(self):
		for box in self.mainBoard:
			if not box.revealed:
				pygame.draw.rect(self.DISPLAYSURF,BOX_COLOR,(box.left,box.top,box.size,box.size))
			else:
				self.drawIcon(box)
			
	def drawBoxCovers(self,boxes,coverage):
		for box in boxes:
			pygame.draw.rect(self.DISPLAYSURF,BG_COLOR,(box.left,box.top,box.size,box.size))
			self.drawIcon(box)
			if coverage > 0:
				pygame.draw.rect(self.DISPLAYSURF,BOX_COLOR,(box.left,box.top,coverage,box.size))
		pygame.display.update()
		self.FPSCLOCK.tick(self.fps)


	def drawHighlightBox(self,box):
		pygame.draw.rect(self.DISPLAYSURF,HIGHLIGHT_COLOR,(box.left-5,box.top-5,box.size+10,box.size+10),4)
		
	def getBoxAtPixel(self,x,y):        #给定一个坐标，返回对应的方块
		for box in self.mainBoard:
			boxRect = pygame.Rect(box.left,box.top,box.size,box.size)
			if boxRect.collidepoint(x,y):
				return box
		return None
	
	def hasWon(self):  #判断玩家是否取胜，取胜条件为所有方块都被翻开
		for box in self.mainBoard:
			if not box.revealed:
				return False
		return True
	
	def revealBoxesAnimation(self,boxesToReveal):  #boxesToReveal放的是要翻开的方块对象列表
		for box in boxesToReveal:
			box.revealed = True
		for coverage in range(self.box_size,-1,-self.reveal_speed):
			self.drawBoxCovers(boxesToReveal,coverage)

	def coverBoxesAnimation(self,boxesToCover):
		for box in boxesToCover:
			box.revealed = False
		for coverage in range(0,self.box_size+self.reveal_speed,self.reveal_speed):
			self.drawBoxCovers(boxesToCover,coverage)
			
	def startGameAnimation(self):
		def splitIntoGroupOf(groupSize,theList):   #将列表按给定长度分割成列表的列表
			result = []
			for i in range(0,len(theList),groupSize):
				result.append(theList[i:i+groupSize])
			return result
		boxes = []
		for box in self.mainBoard:
			boxes.append(box)
		random.shuffle(boxes)
		boxGroups = splitIntoGroupOf(8,boxes)
		self.drawBoard()
		for boxGroup in boxGroups:
			self.revealBoxesAnimation(boxGroup)
			self.coverBoxesAnimation(boxGroup)

	def gameWonAnimation(self):
		color1 = LIGHTBG_COLOR
		color2 = BG_COLOR
		for i in range(13):
			color1,color2 = color2,color1
			self.DISPLAYSURF.fill(color1)
			self.drawBoard()
			pygame.display.update()
			pygame.time.wait(300)
			



def main():
	pygame.init()
	pygame.display.set_caption('Memory Game')
	game = Game()
	handler = Handler(game)
	assert (game.board_width*game.board_height) % 2 == 0 ,'断言,格子总数必须是偶数'
	
	
	mousex = 0
	mousey = 0
	firstSelection = None
	handler.startGameAnimation()
	
	while True:
		mouseClicked = False
		handler.DISPLAYSURF.fill(BG_COLOR)
		handler.drawBoard()
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
				mouseClicked = True
			box = handler.getBoxAtPixel(mousex,mousey)
			if box != None:
				if not box.revealed:
					handler.drawHighlightBox(box)
					if mouseClicked:
						handler.revealBoxesAnimation([box])
						if firstSelection == None:
							firstSelection = box
						else:
							if box.color != firstSelection.color or box.shape != firstSelection.shape:
								pygame.time.wait(1000)
								handler.coverBoxesAnimation([firstSelection,box])
							elif handler.hasWon():
								handler.gameWonAnimation()
								pygame.time.wait(2000)
								game = Game()
								handler = Handler(game)
								handler.drawBoard()
								pygame.display.update()
								pygame.time.wait(1000)
								handler.startGameAnimation()
							firstSelection = None
		pygame.display.update()
		handler.FPSCLOCK.tick(game.fps)

if __name__ == '__main__':
	main()