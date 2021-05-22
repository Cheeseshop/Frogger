import pygame 

class Game ():
    def __init__ (self,screenW = 800,screenH = 600):
        self.screenW = screenW
        self.screenH = screenH
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenW,self.screenH))
        self.gameOver = False
        
    
    def play(self):
        self.frogger = Frogger(pygame.image.load(r'Frogger Images/frogSit.png'),pygame.image.load(r'Frogger Images/frogJump.png'))
        while not self.gameOver:
            self.doInput() # KEYPRESSES AND MOUSE
            self.doInteraction()# INTERACTION CODE
            self.doDraw()# DRAWING CODE
    
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
        pygame.display.update()

    def doInteraction(self):
        pass

class Frogger():
    def __init__(self, froggerSitIm, froggerJumpIm, jmpAmt = 5):
        self.frogImSit = froggerSitIm
        self.frogImJump = froggerJumpIm
        self.frogIm = self.frogImSit
        self.frogPos = [0,0]
        self.jumpAmount = jmpAmt

    def onSpacePressed(self):
        # jump
        self.frogPos[1] -= self.jumpAmount
        self.frogIm = self.frogImJump

    def draw(self,surf):
        frogRect = self.frogIm.get_rect()
        surf.blit(self.frogIm, (self.frogPos[0],self.frogPos[1],frogRect[2],frogRect[3]))    

g = Game()
g.play()