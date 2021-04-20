import pygame, sys
from pygame.locals import *
import random
import Perceptron
import tqdm
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
count = 0

screen = pygame.display.set_mode((640, 640))
screen.fill(WHITE)
pygame.display.set_caption("Game")

ptron = Perceptron.Perceptron(3)

training = []
for i in tqdm.trange(400):
    x = random.randint(Perceptron.xmin, Perceptron.xmax)
    y = random.randint(Perceptron.ymin, Perceptron.ymax)
    answer = 1
    if (y < Perceptron.f(x)):
        answer = -1
    training.append(Perceptron.Trainer(x, y, answer))

def fixpos(p0, p1):
    return (p0+640/2, p1+640/2)

while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    # pygame.draw.circle(screen, BLACK, fixpos(int(open("x").read()), int(open("y").read())), 30)
    
    x1 = int(Perceptron.xmin)
    y1 = int(Perceptron.f(x1))
    x2 = int(Perceptron.xmax)
    y2 = int(Perceptron.f(x2))
    pygame.draw.line(screen, GREEN, fixpos(x1,y1),fixpos(x2,y2))


    weights = ptron.weights
    x1 = Perceptron.xmin
    y1 = (-weights[2] - weights[0]*x1)/weights[1]
    x2 = Perceptron.xmax
    y2 = (-weights[2] - weights[0]*x2)/weights[1]
    pygame.draw.line(screen, BLACK, fixpos(x1,y1),fixpos(x2,y2))
    
    ptron.train(training[count].inputs, training[count].answer)
    count = (count + 1) % len(training)

    for train in training:
        guess = ptron.feedforward(train.inputs)
        pygame.draw.circle(screen, BLACK, fixpos(train.inputs[0], train.inputs[1]), 4)

    pygame.display.update()
    FramePerSec.tick(FPS)

