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
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenW,self.screenH))
        self.gameOver = False
        self.clock = pygame.time.Clock()
        self.score = 0
        self.deltaT = 0
        self.rowHeight = self.screenH//16
        self.lanePositions = [(0,self.rowHeight*3),(self.screenW,self.rowHeight*4),(0,self.rowHeight*5),(self.screenW,self.rowHeight*6)] 
        # audio
        pygame.mixer.init()
        self.riverNoise = pygame.mixer.Sound("Sounds/Water.wav")
        # fonts
        self.arcadeFont = pygame.font.Font("ARCADECLASSIC.TTF",100)
        self.arcadeFontSmall = pygame.font.Font("ARCADECLASSIC.TTF",30)
        
    
    def setup(self):
        self.carsIm = ['Frogger Images/Car 1.png','Frogger Images/Car 2.png','Frogger Images/Car 3.png','Frogger Images/Tractor.png','Frogger Images/Lorry.png']
        self.frogger = Frogger(pygame.image.load(r'Frogger Images/frogSit.png'),pygame.image.load(r'Frogger Images/frogJump.png'),jmpAmt=self.rowHeight,jmpTime=200,pos=[self.screenW//2,self.screenH-self.rowHeight],scale = 22)
        self.carLanes = [[self.screenH-self.rowHeight*2,0],
                      [self.screenH-self.rowHeight*3,0],
                      [self.screenH-self.rowHeight*4,1],
                      [self.screenH-self.rowHeight*5,1],
                      [self.screenH-self.rowHeight*6,0]]
        self.cars = []
        self.victory = False
        self.victoryTime = 0
        self.highestRow = 0
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
                    self.logs.append(Moving(sectionXPos,lane[0],pygame.image.load(imChoice), minSpeed = laneSpeed, maxSpeed = laneSpeed, width = w, height = 22,startDir=lane[1]))
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
                    if self.frogger.pos[0] > 0:
                        self.frogger.onLeftArrowPressed()
                if event.key == pygame.K_RIGHT:
                    if self.frogger.pos[0] < self.screenW - self.frogger.width:
                        self.frogger.onRightArrowPressed()
                if event.key == pygame.K_UP:
                    if self.frogger.pos[1] > 0 + self.frogger.height:
                        self.frogger.onUpArrowPressed()
                        currentRow = self.screenH-self.frogger.pos[1]//self.rowHeight
                        if  currentRow > self.highestRow:
                            self.highestRow = currentRow
                            self.score += 10 
                if event.key == pygame.K_DOWN:
                    if self.frogger.pos[1] < self.screenH - self.frogger.height*2:
                        self.frogger.onDownArrowPressed()
                if event.key == pygame.K_ESCAPE:
                    exit()
    
    def doDraw(self):
        self.screen.fill((0,0,10))
        riverRect = pygame.Rect(0,0,self.screenW,self.rowHeight*7)
        pygame.draw.rect(self.screen,(0,0,100),riverRect)
        grasssRect = pygame.Rect(0,0,self.screenW,self.rowHeight*2)
        pygame.draw.rect(self.screen,(0,100,0),grasssRect)
        for log in self.logs:
            log.draw(self.screen)
        for turtle in self.turtles:
            turtle.draw(self.screen)
        if not self.gameOver:
            self.frogger.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        # draw score
        scoreText = self.arcadeFontSmall.render("Score   " + str(self.score),True,(255,255,255))
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.bottomleft = (10,self.screenH - 10)
        self.screen.blit(scoreText, scoreTextRect)

        if self.gameOver:
            gameOverText = self.arcadeFont.render("GAME     OVER",True,(0,255,255))
            gameOverTextRect = gameOverText.get_rect()
            gameOverTextRect.center = (self.screenW//2,self.screenW//2 - 50)
            self.screen.blit(gameOverText, gameOverTextRect)
        
        if self.victory:
            victoryText = self.arcadeFont.render("VICTORY",True,(255,255,0))
            victoryTextRect = victoryText.get_rect()
            victoryTextRect.center = (self.screenW//2,self.screenW//2 - 50)
            self.screen.blit(victoryText, victoryTextRect)
        
        pygame.display.update()

    def doInteraction(self):
        self.frogger.update(self.deltaT)
        #self.car.update(self.screenW)
        #if self.car.collision(self.frogger):
            #print("HIT!")
        #self.car1.update()
        closestCar = self.cars[0]
        smallestDist = 999999999999999
        for car in self.cars:
            dist = car.distTo(self.frogger.pos)
            car.update(self.screenW,dist) 
            if dist < smallestDist:
                smallestDist = dist
                closestCar = car
            if car.collision(self.frogger) and not self.gameOver:
                self.frogger.deathSquish()
                self.gameOver = True
                return
        
        if not self.frogger.pos[1] < self.rowHeight*7:
            self.riverNoise.stop()
            closestCar.playSound(dist)
        else:
            closestCar.stopSound()
            if not pygame.mixer.get_busy():
                self.riverNoise.play()

        
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
            if not onLog and not onTurtle and not self.gameOver:
                self.frogger.deathPlop()
                self.gameOver = True
                return
        
        # winning condition
        if self.frogger.pos[1] < self.rowHeight * 2:
            if not self.victory:
                self.victory = True
                self.score += 600
            elif self.victoryTime > 3000: #time in miliseconds
                self.setup()
            else:
                self.victoryTime += self.deltaT


class Frogger():
    def __init__(self, froggerSitIm, froggerJumpIm, scale = 32, jmpAmt = 5, jmpTime = 1000, pos = [400,300]):
        self.frogImSit = froggerSitIm
        self.frogImJump = froggerJumpIm
        self.frogImSit = pygame.transform.scale(self.frogImSit,(scale,int(scale*0.8)))
        self.frogImJump = pygame.transform.scale(self.frogImJump,(scale,scale))
        self.frogIm = self.frogImSit
        self.pos = pos
        self.width = scale
        self.height = scale
        self.frogJumpTime = jmpTime
        self.jumpCountdown = 0
        self.jumpAmount = jmpAmt
        self.angle = 0
        self.frogNoise = pygame.mixer.Sound("Sounds/Frog Noise.wav")
        self.plop = pygame.mixer.Sound("Sounds/Plop.wav")
        self.squish = pygame.mixer.Sound("Sounds/Squish.wav")

    def doJumpAnim(self,dir):
        self.frogIm = pygame.transform.rotate(self.frogImJump, self.angle)
        self.jumpCountdown = self.frogJumpTime

    def onUpArrowPressed(self):
        self.angle = 0
        self.pos[1] -= self.jumpAmount
        self.doJumpAnim(1)
        self.croak()

    def onLeftArrowPressed(self):
        self.angle = 90
        self.pos[0] -= self.jumpAmount
        self.doJumpAnim(0)
        self.croak()

    def onDownArrowPressed(self):
        self.angle = 180
        self.pos[1] += self.jumpAmount
        self.doJumpAnim(1)
        self.croak()
        
    def onRightArrowPressed(self):
        self.angle = 270
        self.pos[0] += self.jumpAmount
        self.doJumpAnim(0)
        self.croak()

    def croak(self):
        if random.uniform(0,1) < 0.2:
            self.frogNoise.play()

    def update(self, deltaT):
        if self.jumpCountdown > 0:
            self.jumpCountdown -= deltaT
            if self.jumpCountdown <= 0:
                self.frogIm = pygame.transform.rotate(self.frogImSit, self.angle)

    def draw(self,surf):
        frogRect = self.frogIm.get_rect()
        surf.blit(self.frogIm, (self.pos[0],self.pos[1],frogRect[2],frogRect[3]))

    def deathPlop(self):
        # TODO: death images
        #self.frogIm =     
        self.plop.play()

    def deathSquish(self):
        self.squish.play()
        

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

    def playSound(self,dist = 0):
        vol = dist/400*-1+1
        if vol < 0:
            vol = 0
        if vol > 1:
            vol = 1
        self.carEngineLoop.set_volume(vol)
        if not pygame.mixer.get_busy():
            if not vol == 0:
                self.carEngineLoop.play()
    
    def stopSound(self):
        self.carEngineLoop.stop()

    def update(self,screenW,dist = 0,deltaT = 0):
        if self.dir == 0:
            self.pos[0] += self.speed
        elif self.dir == 1:
            self.pos[0] -= self.speed
        if self.pos[0] > screenW:
            self.pos[0] = -self.width  
        if self.pos[0] < -self.width:
            self.pos[0] = screenW
        
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