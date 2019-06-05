#Flappy bird python edition By Zaydme aka 911
import pygame
import random
import pygame.font
import os
pygame.font.init()
pygame.mixer.init()
print(os.path.dirname(__file__))
score_myfont = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 80)
score_myfont_Outline = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 100)
myfont = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 50)
myfont_Outline = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 53)
Small = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 30)
Small_Outline = pygame.font.Font(os.path.dirname(__file__)+'/FlappyFont.TTF', 31)
score_sound = pygame.mixer.Sound(os.path.dirname(__file__)+'/score.wav')
fly_sound = pygame.mixer.Sound(os.path.dirname(__file__)+'/fly.wav')
ground_color = (135, 206, 235)
width = 300
height = 500
Bird_color = (255,100,20)
Pipe_color = (10,10,250)
ground_image = os.path.dirname(__file__)+"/ground.png"
bird_image = os.path.dirname(__file__)+"/bird.png"
Pipe_Speed = -4
Pipes_Marge = 200
Pipe_width = 80
gravity = 5
bounce = True
class Pipe(object):
    def __init__(self,x,y,color=Pipe_color):
        self.pos = (x,y)
        self.y = y
        self.color = Pipe_color
        self.image = pygame.image.load(os.path.dirname(__file__)+"/pipe.png")
        self.rect = self.image.get_rect()



    def move(self,UP):   
        global Pipe_Speed
        self.pos = (self.pos[0] + Pipe_Speed, self.pos[1])
        self.rect.x = self.pos[0] 
        if UP: self.rect.y = self.pos[1]-Pipe_width-800
        else : self.rect.y = self.pos[1]+Pipe_width
        


    def draw(self,win,up):    
        x = self.pos[0]
        y = self.pos[1]
        if up: win.blit(pygame.transform.flip(self.image,False,True),(x,y-Pipe_width-800))
        else : win.blit(self.image,(x,y+Pipe_width))


class Bird(object):
    def __init__(self,start,color=Bird_color):
        self.color = color
        self.pos = start
        self.image = pygame.image.load(bird_image)
        self.rect = self.image.get_rect()


    def move(self):
        global gravity,bounce
        if bounce :
            if self.pos[1] > 190 : self.gravity = -1.5
            if self.pos[1] < 60 : self.gravity = 1.5
        if not bounce:
            self.gravity = gravity
            if gravity < 8 : gravity += 0.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            pygame.key.set_repeat()
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fly_sound.play()
                    bounce = False
                    if gravity > 0 : gravity -= gravity+8
                    elif gravity < 0 : gravity -= 4
        self.pos = (self.pos[0], self.pos[1] + self.gravity)
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        if self.pos[1] < 5 : gravity = 0.2

    def draw(self,win): 
        x = self.pos[0]
        y = self.pos[1]
        win.blit(pygame.transform.rotate(self.image,-self.gravity*2),(self.pos[0],self.pos[1]))
    def colidded(self,obg):
        return self.rect.colliderect(obg.rect)


class Background(object):
    def __init__(self,start,image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.pos = start
    def move(self):
        self.pos = (self.pos[0]+Pipe_Speed*2,self.pos[1])
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
    def draw(self,win):
        win.blit(self.image,(self.pos[0],self.pos[1]))
    



def redrawWindow(win,last_score):
    global b, width
    win.fill(ground_color)      
    b.draw(win)
    p1.draw(win,False)
    p1_up.draw(win,True)
    p2.draw(win,False)
    p2_up.draw(win,True)
    ground_0.draw(win)
    ground_1.draw(win)
    if not bounce :
        textsurface = score_myfont.render(str(score), True, (233, 255, 35))
        textOut = score_myfont_Outline.render(str(score), True, (0, 0, 0))
        win.blit(textOut,(width/2-textOut.get_width()/2,5-7))
        win.blit(textsurface,(width/2-textsurface.get_width()/2,5))
    else :
        title = myfont.render("Flappy Bird", True, (233, 255, 35))
        title_Outline = myfont_Outline.render("Flappy Bird", True, (0, 0, 0))

        textsurface = myfont.render("LAST : "+str(last_score), True, (233, 255, 35))
        textOut = myfont_Outline.render("LAST : "+str(last_score), True, (0, 0, 0))

        credit = Small.render("By Zayd", True, (123, 135, 21))
        creditOut = Small_Outline.render("By Zayd", True, (0, 0, 0))

        win.blit(creditOut,(width/2-creditOut.get_width()/2,height-35-4))
        win.blit(credit,(width/2-credit.get_width()/2,height-35))

        win.blit(title_Outline,(width/2-title_Outline.get_width()/2,height/2-10-4))
        win.blit(title,(width/2-title.get_width()/2,height/2-10))

        win.blit(textOut,(width/2-textOut.get_width()/2,height/2+60-4))
        win.blit(textsurface,(width/2-textsurface.get_width()/2,height/2+60))
        
    pygame.display.set_caption("flappy | By Zayd " )
    pygame.display.update()

def randomPipeCoord():
    return random.randrange(150,300)

def main(last_score=0):
    global score,b,p1,p2,p1_up,p2_up,ground_0,ground_1,bounce
    score = 0
    win = pygame.display.set_mode((width, height))
    ground_0 = Background((0,height-60),ground_image)
    ground_1 = Background((width,height-60),ground_image)
    b = Bird((100,200))
    p1 = Pipe(2*width,randomPipeCoord())
    p1_up = Pipe(2*width,p1.y)
    p2 = Pipe(p1.pos[0]+Pipes_Marge,randomPipeCoord())
    p2_up = Pipe(p1.pos[0]+Pipes_Marge,p2.y)
    flag = True
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(10)           
        clock.tick(60)
        ground_0.move()
        ground_1.move()
        b.move()
        if not bounce:
            p1.move(False)
            p1_up.move(True)
            p2.move(False)
            p2_up.move(True)
            if b.colidded(ground_0) or b.colidded(ground_1)  or b.colidded(p1)  or b.colidded(p2) or b.colidded(p1_up)  or b.colidded(p2_up):
                pygame.mixer.music.load(os.path.dirname(__file__)+'/die.mp3')
                pygame.mixer.music.play(0)
                bounce = True
                main(score)
        if p1.pos[0]-b.pos[0] ==0  or p2.pos[0]-b.pos[0] ==0 :
            score +=1
            score_sound.play()
        if p1.pos[0] == -Pipe_width:
            del(p1)
            coord = randomPipeCoord()
            p1 = Pipe(p2.pos[0]+Pipes_Marge,coord)
            p1_up = Pipe(p2.pos[0]+Pipes_Marge,coord)

            
        if p2.pos[0] == -Pipe_width:
            del(p2)
            coord = randomPipeCoord()
            p2 = Pipe(p1.pos[0]+Pipes_Marge,coord)
            p2_up = Pipe(p1.pos[0]+Pipes_Marge,coord)
        
        if ground_0.pos[0] <= -width:
            del(ground_0)
            ground_0 = Background((width-4,height-60),ground_image)
            
        if ground_1.pos[0] == -width:
            del(ground_1)
            ground_1 = Background((width,height-60),ground_image)
            
        redrawWindow(win,last_score)
 
       
    pass

main()
