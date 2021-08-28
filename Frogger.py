import pygame, random
from math import sqrt

def pythag(a, b):
    return sqrt(a*a + b*b)

def pointRectIntersect(pt, r):
    rx,ry,rw,rh = r[0],r[1],r[2],r[3]
    ptx, pty = pt[0], pt[1]
    if ptx > rx:
        if ptx < rx + rw:
            if pty > ry:
                if pty < ry + rh:
                    return True
    return False

def rectRectIntersect(a,b):
    ax,ay,aw,ah = a[0],a[1],a[2],a[3]
    bx,by,bw,bh = b[0],b[1],b[2],b[3]

    # test all 4 corners of a inside b?
    if pointRectIntersect((ax,ay),b):
        return True
    elif pointRectIntersect((ax+aw,ay),b):
        return True
    elif pointRectIntersect((ax+aw,ay+ah),b):
        return True
    elif pointRectIntersect((ax,ay+ah),b):
        return True
    # test all 4 corners of b inside a?
    elif pointRectIntersect((bx,by),a):
        return True
    elif pointRectIntersect((bx+bw,by),a):
        return True
    elif pointRectIntersect((bx+bw,by+bh),a):
        return True
    elif pointRectIntersect((bx,by+bh),a):
        return True
    # test the center of a inside b
    elif pointRectIntersect((ax+aw/2,ay+ah/2),b):
        return True
    # test the center of b inside a
    elif pointRectIntersect((bx+bw/2,by+bh/2),a):
        return True
    return False

class Game ():
    def __init__ (self,screenW = 800,screenH = 600):
        self.screenW = screenW
        self.screenH = screenH
        pygame.font.init()
        self.arcadeFont = pygame.font.Font("ARCADECLASSIC.TTF",100)
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenW,self.screenH))
        self.gameOver = False
        self.clock = pygame.time.Clock()
        self.deltaT = 0
        self.rowHeight = self.screenH//16
        self.lanePositions = [(0,self.rowHeight*3),(self.screenW,self.rowHeight*4),(0,self.rowHeight*5),(self.screenW,self.rowHeight*6)] 
        # audio
        pygame.mixer.init()
        
    
    def setup(self):
        self.carsIm = ['Frogger Images/Car 1.png','Frogger Images/Car 2.png','Frogger Images/Car 3.png','Frogger Images/Tractor.png','Frogger Images/Lorry.png']
        self.frogger = Frogger(pygame.image.load(r'Frogger Images/frogSit.png'),pygame.image.load(r'Frogger Images/frogJump.png'),jmpAmt=self.rowHeight,jmpTime=200,pos=[self.screenW//2,self.screenH-self.rowHeight])
        self.carLanes = [[self.screenH-self.rowHeight*2,0],
                      [self.screenH-self.rowHeight*3,0],
                      [self.screenH-self.rowHeight*4,1],
                      [self.screenH-self.rowHeight*5,1],
                      [self.screenH-self.rowHeight*6,0]]
        self.cars = []
        for lane in self.carLanes:
            numCars = random.randint(1,5)
            imChoice = random.choice(self.carsIm)
            laneSpeed = random.randint(3,10)
            w = 32
            if imChoice == 'Frogger Images/Lorry.png':
                w = 64
                laneSpeed = 4
            if imChoice == 'Frogger Images/Tractor.png':
                laneSpeed = 2
            laneCarXs = []
            for i in range(numCars):
                xRand = random.randint(0,self.screenW)
                for otherCarX in laneCarXs:
                    while abs(xRand - otherCarX) < w*2:
                        xRand = random.randint(0,self.screenW)
                laneCarXs.append(xRand)
                self.cars.append(Moving(xRand,lane[0],pygame.image.load(imChoice), minSpeed = laneSpeed, maxSpeed = laneSpeed, width = w,startDir=lane[1]))

        self.logLanes = [[self.rowHeight*4,0],
                      [self.rowHeight*5,0],
                      [self.rowHeight*2,1]]
        self.logsIm = ['Frogger Images/Log L.png','Frogger Images/Log M.png','Frogger Images/Log R.png']
        self.logs = []
        for lane in self.logLanes:
            numlogs = random.randint(1,3)
            laneSpeed = random.randint(1,2)
            w = 32
            laneLogXs = []
            for i in range(numlogs):
                logWidth = random.randint(2,4)
                xRand = random.randint(0,self.screenW)
                # TODO: do this, make sure we don't generate one log on top of another!
                for otherLogX in laneLogXs:
                    while abs(xRand - otherLogX) < w*2:
                        xRand = random.randint(0,self.screenW)
                for section in range(logWidth):
                    sectionXPos = xRand+(w*section)
                    laneLogXs.append(sectionXPos)
                    if section == 0:
                        imChoice = self.logsIm[0]
                    elif section == logWidth-1:
                        imChoice = self.logsIm[2]
                    else:
                        imChoice = self.logsIm[1]
                    self.logs.append(Moving(sectionXPos,lane[0],pygame.image.load(imChoice), minSpeed = laneSpeed, maxSpeed = laneSpeed, width = w,startDir=lane[1]))
        self.turtleLanes = [[self.rowHeight*3,0],
                            [self.rowHeight*6,1]]
        self.turtlesIm = ['Frogger Images/Turtle 1.png','Frogger Images/Turtle 2.png','Frogger Images/Turtle 3.png','Frogger Images/Turtle 4.png','Frogger Images/Turtle 5.png']
        self.turtles = []
        for lane in self.turtleLanes:
            numTurtles = 3
            laneSpeed = -random.randint(2,3)
            w = 32
            laneTurtleXs = []
            for i in range(numTurtles):
                turtleWidth = 3
                xRand = random.randint(0,self.screenW)
                # TODO: do this, make sure we don't generate one log on top of another!
                for otherTurtleX in laneTurtleXs:
                    while abs(xRand - otherTurtleX) < w*2:
                        xRand = random.randint(0,self.screenW)
                for section in range(turtleWidth):
                    sectionXPos = xRand+(w*section)
                    laneTurtleXs.append(sectionXPos)
                    imChoice = self.turtlesIm[1]
                    self.turtles.append(Moving(sectionXPos,lane[0],pygame.image.load(imChoice), minSpeed = laneSpeed, maxSpeed = laneSpeed, width = w,startDir=lane[1],animates=True,animTime=200,animImages=[pygame.image.load(self.turtlesIm[1]),pygame.image.load(self.turtlesIm[2])]))

    def play(self):
        self.setup()
        
        while not self.gameOver:
            self.doInput() # KEYPRESSES AND MOUSE
            self.doInteraction()# INTERACTION CODE
            self.doDraw()# DRAWING CODE

            self.deltaT = self.clock.tick(30)
        self.endGame()

    
    def endGame(self):
        while self.gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_RETURN:
                        self.gameOver = False
                        
            if self.gameOver:
                self.doInteraction()
                self.doDraw()
            # TODO: display end game text
            self.deltaT = self.clock.tick(30)
        self.play()
    
    def doInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.frogger.onLeftArrowPressed()
                if event.key == pygame.K_RIGHT:
                    self.frogger.onRightArrowPressed()
                if event.key == pygame.K_UP:
                    self.frogger.onUpArrowPressed()
                if event.key == pygame.K_DOWN:
                    self.frogger.onDownArrowPressed()
                if event.key == pygame.K_ESCAPE:
                    exit()
    
    def doDraw(self):
        self.screen.fill((0,0,10))
        riverRect = pygame.Rect(0,0,self.screenW,self.rowHeight*7)
        pygame.draw.rect(self.screen,(0,0,100),riverRect)
        for log in self.logs:
            log.draw(self.screen)
        for turtle in self.turtles:
            turtle.draw(self.screen)
        self.frogger.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        if self.gameOver:
            gameOverText = self.arcadeFont.render("GAME     OVER",True,(0,255,255))
            gameOverTextRect = gameOverText.get_rect()
            gameOverTextRect.center = (self.screenW//2,self.screenW//2 - 50)
            self.screen.blit(gameOverText, gameOverTextRect)
        pygame.display.update()

    def doInteraction(self):
        self.frogger.update(self.deltaT)
        #self.car.update(self.screenW)
        #if self.car.collision(self.frogger):
            #print("HIT!")
        #self.car1.update()
        for car in self.cars:
            dist = car.distTo(self.frogger.pos)
            car.update(self.screenW,dist) 
            if car.collision(self.frogger):
                self.frogger.death()
                self.gameOver = True
                return
        
        for log in self.logs:
            log.update(self.screenW)
        
        for turtle in self.turtles:
            turtle.update(self.screenW,self.deltaT)

        if self.frogger.pos[1] >= self.rowHeight*2 and self.frogger.pos[1] < self.rowHeight*7:
            onLog = False
            for log in self.logs:
                if log.collision(self.frogger):
                    # TODO: Fix this, strange motion...
                    self.diff = log.pos[0] - self.frogger.pos[0]
                    self.frogger.pos[0] += self.diff
                    onLog = True
                    return
            onTurtle = False
            for turtle in self.turtles:
                if turtle.collision(self.frogger):
                    # TODO: Fix this, strange motion...
                    self.diff = turtle.pos[0] - self.frogger.pos[0]
                    self.frogger.pos[0] += self.diff
                    onTurtle = True
                    return
            if not onLog and not onTurtle:
                self.frogger.death()
                self.gameOver = True
                return

class Frogger():
    def __init__(self, froggerSitIm, froggerJumpIm, scale = 32, jmpAmt = 5, jmpTime = 1000, pos = [400,300]):
        self.frogImSit = froggerSitIm
        self.frogImJump = froggerJumpIm
        self.frogImSit = pygame.transform.scale(self.frogImSit,(scale,scale))
        self.frogImJump = pygame.transform.scale(self.frogImJump,(scale,scale))
        self.frogIm = self.frogImSit
        self.pos = pos
        self.width = scale
        self.height = scale
        self.frogJumpTime = jmpTime
        self.jumpCountdown = 0
        self.jumpAmount = jmpAmt
        self.angle = 0

    def doJumpAnim(self,dir):
        self.frogIm = pygame.transform.rotate(self.frogImJump, self.angle)
        self.jumpCountdown = self.frogJumpTime

    def onUpArrowPressed(self):
        self.angle = 0
        self.pos[1] -= self.jumpAmount
        self.doJumpAnim(1)

    def onLeftArrowPressed(self):
        self.angle = 90
        self.pos[0] -= self.jumpAmount
        self.doJumpAnim(0)

    def onDownArrowPressed(self):
        self.angle = 180
        self.pos[1] += self.jumpAmount
        self.doJumpAnim(1)
        
    def onRightArrowPressed(self):
        self.angle = 270
        self.pos[0] += self.jumpAmount
        self.doJumpAnim(0)

    def update(self, deltaT):
        if self.jumpCountdown > 0:
            self.jumpCountdown -= deltaT
            if self.jumpCountdown <= 0:
                self.frogIm = pygame.transform.rotate(self.frogImSit, self.angle)

    def draw(self,surf):
        frogRect = self.frogIm.get_rect()
        surf.blit(self.frogIm, (self.pos[0],self.pos[1],frogRect[2],frogRect[3]))

    def death(self):
        # TODO: death images
        #self.frogIm =     
        pass
        

class Moving():
    def __init__(self,startX,startY, image,  width = 32, height = 32, startDir = 0, minSpeed = 3,maxSpeed = 10, spawnChance = 1, dissapears = False, minDissapear = 3,maxDissapear = 8, animTime = 0.5, animates = False, animImages = []):
        self.startPos = [startX,startY]
        self.speed = random.uniform(minSpeed,maxSpeed)
        self.pos = self.startPos
        self.animates = animates
        self.animDeltaT = 0
        self.animTime = animTime
        self.animCounter = 0
        self.dissapears = dissapears
        self.dissapearTime = random.uniform(minDissapear,maxDissapear)
        self.dissppearCounter = 0
        self.width = width
        self.height = height
        self.dir = startDir
        self.spawnChance = spawnChance
        self.scale = width
        self.image = pygame.transform.scale(image,(width,height))
        self.animImages = []
        self.beep1 = pygame.mixer.Sound("Sounds/beep1.wav")
        self.beep2 = pygame.mixer.Sound("Sounds/beep2.wav")
        self.carEngineLoop = pygame.mixer.Sound("Sounds/CarEngineLoop.wav")
        for im in animImages:
            self.animImages.append(pygame.transform.scale(im,(width,height)))

    def draw(self,surf):
        movingRect = self.image.get_rect()
        surf.blit(self.image, (self.pos[0],self.pos[1],movingRect[2],movingRect[3]))

    def distTo(self,otherPos):
        a = self.pos[0] - otherPos[0]
        b = self.pos[1] - otherPos[1]
        return pythag(a,b)

    def update(self,screenW,dist = 0,deltaT = 0):
        if self.dir == 0:
            self.pos[0] += self.speed
        elif self.dir == 1:
            self.pos[0] -= self.speed
        if self.pos[0] > screenW:
            self.pos[0] = -self.width  
        if self.pos[0] < -self.width:
            self.pos[0] = screenW

        # Sound
        
        self.carEngineLoop.set_volume(dist)
        self.carEngineLoop.play(-1)
        
        if self.animates:
            if self.animDeltaT > self.animTime:
                self.animCounter += 1
                self.animDeltaT -= self.animTime
            self.image = self.animImages[self.animCounter%len(self.animImages)]
            self.animDeltaT += deltaT
        
        if self.dissapears:
            if self.dissppearCounter >= self.dissapearTime:
                #TODO: make the turtle dissapear
                pass
            self.dissppearCounter += deltaT


    def collision(self,other):
        a = (self.pos[0],self.pos[1],self.width,self.height)
        b = (other.pos[0],other.pos[1],other.width,other.height)
        if rectRectIntersect(a,b) :
            return True
        return False
    
    
g = Game()
g.play()