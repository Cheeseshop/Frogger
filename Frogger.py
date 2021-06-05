import pygame, random

class Game ():
    def __init__ (self,screenW = 800,screenH = 600):
        self.screenW = screenW
        self.screenH = screenH
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenW,self.screenH))
        self.gameOver = False
        self.clock = pygame.time.Clock()
        self.deltaT = 0
    
    def setup(self):
        self.frogger = Frogger(pygame.image.load(r'Frogger Images/frogSit.png'),pygame.image.load(r'Frogger Images/frogJump.png'),jmpAmt=20,jmpTime=200)
        #self.car = Vehicle(self.screenW//2 - 100,self.screenH//2,pygame.image.load(r'Frogger Images/frogSit.png'))
        #self.car1 = Vehicle(self.screenW//2 + 100,self.screenH//2,pygame.image.load(r'Frogger Images/frogSit.png'))
        self.cars = []
        for i in range(100):
            self.cars.append(Vehicle(random.uniform(0,self.screenW),
                random.uniform(0,self.screenH),pygame.image.load(r'Frogger Images/frogSit.png')))
    
    def play(self):
        self.setup()
        
        while not self.gameOver:
            self.doInput() # KEYPRESSES AND MOUSE
            self.doInteraction()# INTERACTION CODE
            self.doDraw()# DRAWING CODE

            self.deltaT = self.clock.tick(30)
    
    def doInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.frogger.onSpacePressed()
    
    def doDraw(self):
        self.screen.fill((0,0,10))
        self.frogger.draw(self.screen)
        #self.car.draw(self.screen)
        #self.car1.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        pygame.display.update()

    def doInteraction(self):
        self.frogger.update(self.deltaT)
        #self.car.update()
        #self.car1.update()
        for car in self.cars:
            car.update(self.screenW)

class Frogger():
    def __init__(self, froggerSitIm, froggerJumpIm, scale = 32, jmpAmt = 5, jmpTime = 1000):
        self.frogImSit = froggerSitIm
        self.frogImJump = froggerJumpIm
        self.frogImSit = pygame.transform.scale(self.frogImSit,(scale,scale))
        self.frogImJump = pygame.transform.scale(self.frogImJump,(scale,scale))
        self.frogIm = self.frogImSit
        self.frogPos = [400,300]
        self.frogJumpTime = jmpTime
        self.jumpCountdown = 0
        self.jumpAmount = jmpAmt

    def onSpacePressed(self):
        # jump
        self.frogPos[1] -= self.jumpAmount
        self.frogIm = self.frogImJump
        self.jumpCountdown = self.frogJumpTime

    def onMoveLeft(self):
        pass # Miles homework

    def onMoveRight(self):
        pass # Miles homework
        # reminder: Transform.rotate

    def update(self, deltaT):
        if self.jumpCountdown > 0:
            self.jumpCountdown -= deltaT
            if self.jumpCountdown <= 0:
                self.frogIm = self.frogImSit

    def draw(self,surf):
        frogRect = self.frogIm.get_rect()
        surf.blit(self.frogIm, (self.frogPos[0],self.frogPos[1],frogRect[2],frogRect[3]))    

class Vehicle():
    def __init__(self,startX,startY, image, scale = 32, startDir = 0, minSpeed = 3,maxSpeed = 10, spawnChance = 1):
        self.startPos = [startX,startY]
        self.speed = random.uniform(minSpeed,maxSpeed)
        self.pos = self.startPos
        self.dir = startDir
        self.spawnChance = spawnChance
        self.scale = scale
        self.image = pygame.transform.scale(image,(scale,scale))

    def draw(self,surf):
        vehicleRect = self.image.get_rect()
        surf.blit(self.image, (self.pos[0],self.pos[1],vehicleRect[2],vehicleRect[3]))

    def update(self,screenW):
        self.pos[0] += self.speed
        if self.pos[0] > screenW:
            self.pos[0] = 0  
        if self.pos[0] < 0:
            self.pos[0] = screenW  

    
        


g = Game()
g.play()