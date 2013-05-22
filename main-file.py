from __future__ import division
from visual import *
from visual.controls import *
from visual.graph import *
from random import uniform
from random import choice
from random import randrange
import pprint

class Cells:
    def __init__(self, n = 20, ms=1.5):
        d = display(x=800, center=(n/5,n/5,n/5), title = "Tumor Growth v1.0")
        d.forward = (-0.8,-0.65,-1)
        self.num = n                    #Number of cells = n^3
        self.array = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]   #Creating a 3D array to store all the positions
        self.radius = ms/2            #Radius of a cell

        self.MINX = -1-ms/2           #left
        self.MINY = -1-ms/2           #bottom
        self.MINZ = -1-ms/2           #back
        self.MAXX = n-ms/2            #right
        self.MAXY = n-ms/2            #top
        self.MAXZ = n-ms/2            #front

        self.ProbCellMove = .05             # Probability for a cell to Move
        self.ProbCellDivide = .1            # Probability for a cell to Divide
        self.ProbCelltoCancer = 0.001       # Probability for a cell to become Cancer cell
        self.ProbCancerDivide = .30         # Probability for a Cancer cell to Divide
        self.ProbCancerCellDie = 0          # Probability for a Cancer cell to Die
        self.ProbCancerDivideChemo = 0.05   # Probability for a Cancer cell to Divide during Chemo
        self.ProbCancerCellDieChemo = 0.50  # Probability for a Cancer cell to Die during Chemo
        self.ProbCelltoCancerChemo = 0      # Probability for a Cancer cell to become Cancer cell during Chemo
        self.ProbCellDieChemo = .08         # Probability for a cell to Die under Chemo
        self.ProbCellDieNorm = .01         # Probability for a cell to Die under Normal condition

        self.NoOfCellsBeforeCancerAppears = n^2                 # Approximate number of cells before a cancer cell should appear ~ It's an approximation
        self.PercentageCellsHitByChemo = 85                     # Percentage of cancer cells hit by chemo
                
        self.t = 0                                              # Time
        self.timechemostart = 9999                              # Time the chemo doze was started
        self.chemodozecheck = 0                                 # Check to see whether the chemo doze has been given or not
        
        self.NoOfCells = n^3                                    # Number of Cells
        self.NoOfCancer = 0                                     # Number of Cancer Cells
        self.f = frame()                                        # frame for all the healthy cells
        self.c = frame()                                        # frame for all the cancer cells
        self.CanTurn = self.ProbCelltoCancer                     # don't change
        self.CanDivide =  self.ProbCancerDivide                  # don't change
        self.ProbCellDie = self.ProbCellDieNorm                  # don't change
        self.state = 0                                           # Check to see the state of chemo
        self.cells()

    def cells(self):
        self.initializePositions()
        gd = gdisplay(y=360, xtitle='Time', ytitle='No. of cells')         # Creating a Graph Display
        f1 = gcurve(color=color.cyan)
        f2 = gcurve(color=color.red)
        delta = 0.001
        
        while (1==1):
            rate(1000)
            self.Grow()
            f1.plot(pos=(self.t, self.NoOfCells))
            f2.plot(pos=(self.t, self.NoOfCancer))
            self.t = self.t+delta
            if self.chemodozecheck == 1:
                if (self.t > (self.timechemostart+1)):
                    self.state = 0
                    self.chemodozecheck = 0
                    self.CanTurn = self.ProbCelltoCancer
                    self.CanDivide =  self.ProbCancerDivide
                    self.ProbCellDie = self.ProbCellDieNorm
                    for obj in self.c.objects:
                        obj.color = color.red
            
                
            
    def initializePositions(self):
        #wire frame of space
        backBottom = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MAXX, self.MINY, self.MINZ)], color=color.white)
        backTop = curve(pos=[(self.MINX, self.MAXY, self.MINZ), (self.MAXX, self.MAXY, self.MINZ)], color=color.white)
        frontBottom = curve(pos=[(self.MINX, self.MINY, self.MAXZ), (self.MAXX, self.MINY, self.MAXZ)], color=color.white)
        frontTop = curve(pos=[(self.MINX, self.MAXY, self.MAXZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)
        leftBottom = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MINX, self.MINY, self.MAXZ)], color=color.white)
        leftTop = curve(pos=[(self.MINX, self.MAXY, self.MINZ), (self.MINX, self.MAXY, self.MAXZ)], color=color.white)
        rightBottom = curve(pos=[(self.MAXX, self.MINY, self.MINZ), (self.MAXX, self.MINY, self.MAXZ)], color=color.white)
        rightTop = curve(pos=[(self.MAXX, self.MAXY, self.MINZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)
        backLeft = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MINX, self.MAXY, self.MINZ)], color=color.white)
        backRight = curve(pos=[(self.MAXX, self.MINY, self.MINZ), (self.MAXX, self.MAXY, self.MINZ)], color=color.white)
        frontLeft = curve(pos=[(self.MINX, self.MINY, self.MAXZ), (self.MINX, self.MAXY, self.MAXZ)], color=color.white)
        frontRight = curve(pos=[(self.MAXX, self.MINY, self.MAXZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)
        
        # Creating initial 8 cells
        for x in range(int(self.num/2),int(self.num/2)+2):
            for y in range(int(self.num/2),int(self.num/2)+2):
                for z in range(int(self.num/2),int(self.num/2)+2):
                    self.array[x][y][z] = sphere(frame = self.f,pos=(x,y,z), radius=self.radius, color=color.white)
        
        c = controls(height=360)                # Creating the buttons to control the Display
        b1 = button(pos=(0,75), height=42, width=110, text='Show All', action=lambda: self.showall())
        b2 = button(pos=(0,25), height=42, width=110, text='Show Cancer Cells', action=lambda: self.showcancer())
        b5 = button(pos=(0,-25), height=42, width=100, text='Chemo 1 doze', action=lambda: self.chemodoze())

    def showcancer(self):
        self.f.visible = False
                    
    def showall(self):
        self.f.visible = True
    

    def chemodoze(self):
        self.state = 1
        self.CanTurn = self.ProbCelltoCancerChemo
        self.CanDivide =  self.ProbCancerDivideChemo
        self.ProbCellDie = self.ProbCellDieChemo
        self.chemodozecheck = 1
        self.timechemostart = self.t
        for obj in self.c.objects:
                a = uniform(0, 100)
                if a < self.PercentageCellsHitByChemo :
                    obj.color = color.cyan
                else :
                    pass

    
    def Grow(self):
        count = 0
        count1 = 0
        for x in range(self.num):
            for y in range(self.num):
                for z in range(self.num):
                    if self.array[x][y][z] == 0:
                        pass
                    elif self.array[x][y][z].frame == self.f:
                        count = count+1
                        a = uniform(0, 100)
                        if a < self.ProbCellMove :
                            self.MoveCell(x,y,z)
                        elif a < self.ProbCellMove+self.ProbCellDivide :
                            self.CellDivide(x,y,z)
                        elif a < self.ProbCellMove+self.ProbCellDivide+self.ProbCellDie :
                            self.array[x][y][z].visible = False
                            self.array[x][y][z] = 0
                        elif ((a<self.ProbCellMove+self.ProbCellDivide+self.ProbCellDie+self.CanTurn)&(self.NoOfCells>(self.NoOfCellsBeforeCancerAppears))) :
                            if self.state==1:
                                self.array[x][y][z].color = color.cyan
                            else:
                                self.array[x][y][z].color = color.red
                            self.array[x][y][z].frame = self.c
                        
                    elif self.array[x][y][z].frame == self.c:
                        count = count+1
                        count1 = count1+1
                        a = uniform(0, 100)
                        if a < self.CanDivide :
                            self.CancerDivide(x,y,z)
                        elif self.array[x][y][z].color == color.red :
                            if a < self.CanDivide+self.ProbCancerCellDie :
                                self.array[x][y][z].visible = False
                                self.array[x][y][z] = 0
                        elif self.array[x][y][z].color == color.cyan :
                            if a < self.CanDivide+self.ProbCancerCellDieChemo :
                                self.array[x][y][z].visible = False
                                self.array[x][y][z] = 0
                            
        self.NoOfCells = count
        self.NoOfCancer = count1

    def MoveCell(self, x, y, z):            # Function to move a specific cell
        t = []
        t = self.FindAdjacentFree(x,y,z)
        if t != []:
            moveto = choice(t)
            i=0
            for x1 in range(x-1, x+2):
                for y1 in range(y-1, y+2):
                    for z1 in range(z-1, z+2):
                        i = i+1
                        if i==moveto :
                            self.array[x1][y1][z1] = sphere(frame = self.f, pos=(x1,y1,z1), radius=self.radius, color=color.white)

            self.array[x][y][z].visible = False
            self.array[x][y][z] = 0

    def FindAdjacentFree(self, x, y, z):        # Function to find empty adjacent places
        t = []
        i=0
        for x1 in range(x-1, x+2):
            for y1 in range(y-1, y+2):
                for z1 in range(z-1, z+2):
                    i = i+1
                    try:
                        if self.array[x1][y1][z1]==0:
                            t.append(i)
                    except:
                        pass
        return t
        

    def CellDivide(self, x, y, z):              # Function to Divide the Cell.
        t = []
        t = self.FindAdjacentFree(x,y,z)
        if t != []:
            moveto = choice(t)
            i=0
            for x1 in range(x-1, x+2):
                for y1 in range(y-1, y+2):
                    for z1 in range(z-1, z+2):
                        i = i+1
                        if i==moveto :
                            self.array[x1][y1][z1] = sphere(frame = self.f, pos=(x1,y1,z1), radius=self.radius, color=color.white)

    def CancerDivide(self, x, y, z):             # Function to Divide the Cancer Cell.
        moveto = randrange(0,28)
        i = 0
        for x1 in range(x-1, x+2):
            for y1 in range(y-1, y+2):
                for z1 in range(z-1, z+2):
                    i = i+1
                    if i==moveto :
                        try:
                            if self.array[x1][y1][z1] == 0:
                                self.array[x1][y1][z1] = sphere(frame = self.c, pos=(x1,y1,z1), radius=self.radius)
                            else:
                                self.array[x1][y1][z1].visible = False
                                self.array[x1][y1][z1] = sphere(frame = self.c, pos=(x1,y1,z1), radius=self.radius)
                            if self.state==1:
                                self.array[x1][y1][z1].color = color.cyan
                            else:
                                self.array[x1][y1][z1].color = color.red
                        except:
                            pass
        
################################################################################################################
c = Cells(20, 1.5)  ###   USED TO RUN THE PROGRAM. GIVE THE NUMBER OF CELLS AND THE SIZE OF EACH CELL HERE   ###
################################################################################################################
