import pygame
from math import radians, sin, cos
from random import choice, uniform, randint
import time

pygame.init()

WIN = pygame.display
D = WIN.set_mode((1200, 600))

class Particle:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.color = choice([(217, 103, 51), (238, 95, 30)])
        self.radius = uniform(2, 7)
        self.pull = 0
        self.start = time.time()
        self.points = []

    def adjust(self):
        self.radius -= 0.03

    def draw(self):
        if self.radius > 0:
            pygame.draw.circle(D, self.color, (int(self.pos[0])
                                           , int(self.pos[1])), int(self.radius))
            for i in range(len(self.points)):
                for j in range(1, len(self.points)):
                    pygame.draw.line(D, self.color, (int(self.points[i][0]), int(self.points[i][1]))
                                     , (int(self.points[j][0]), int(self.points[j][1])), int(self.radius))

    def move(self):
        now  = time.time()
        self.pos[0] += cos(radians(self.angle)) * 2
        self.pos[1] += (sin(radians(self.angle)) + self.pull) * 2
        if now - self.start > 0.1:
            self.points.append(self.pos)
            self.pull += 0.25
            self.start = now


class FireWorks:
    def __init__(self):
        self.particles = []
        for i in range(360):
            self.particles.append(Particle([600, 300], i))

    def explode(self):
        for i in range(len(self.particles)):
            self.particles[i].draw()
            self.particles[i].move()
            self.particles[i].adjust()
        for p in self.particles:
            if p.radius < 0:
                self.particles.remove(p)
            

f = FireWorks()
D.fill((0, 0, 0))
while True:
    pygame.event.get()
    D.fill((0, 0, 0))
    f.explode()
    WIN.flip()
    
