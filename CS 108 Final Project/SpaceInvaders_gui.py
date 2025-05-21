"""CS 108 Lab 12

This module implements a GUI controller for a particle simulation

@author: Serita Nelesen (smn4)
@date: Fall, 2014
@author: Keith VanderLinden (kvlinden)
@date: Fall, 2018 - updated to use callback animation
@date: Spring, 2021 - ported to GuiZero
@author: Jaden Brookens (jlb224)
@date: semester, year
"""

from guizero import App, Drawing, PushButton, Box, Text, TextBox, Window
from random import randint
from particle import Particle
from helpers import get_random_color, distance
from Bullets import Bullets
from time import sleep
from random import *
class ParticleSimulation:
    """ParticleSimulation runs a simulation of multiple particles interacting
    on a single canvas.
    """

    def __init__(self, app):
        """Instantiate the simulation GUI app."""

        app.title = 'Space Invasion'
        UNIT = 1000
        CONTROL_UNIT = 50
        app.font = 'Helvetica'
        app.width = UNIT
        app.height = UNIT + CONTROL_UNIT + 100
        self.p_list = []
        self.b_list = []
        self.score = 0
        app.when_key_pressed = self.key_pressed
        
        app.repeat(10, self.draw_frame)
        
        
        self.spaceship = (Particle(460, 990, 0, 0, 0, 'blue', -1))
        self.p_list.append(self.spaceship)
        
        box = Box(app, layout='grid', width=UNIT, height=UNIT + CONTROL_UNIT)
        self.drawing = Drawing(box, width=UNIT, height=UNIT, grid=[0,0,2,1])
        self.drawing.bg = "black"
        
        #window = Window(app, layout='grid', title = "Score Board")
        #Text(app, text="Score:", grid=[1,1], align='right')
        self.score_text = Text(app, text=self.score, grid=[1,1])
        
        #PushButton(box, grid=[1,1], text='Start', command=self.run_game)
        
        self.run_game()
        
    def add_particle(self, y):
        radius = 0
        x = randint(50, self.drawing.width-100)
        vel_x = 0
        vel_y = randint(2,4)
        color = get_random_color()
        self.p_list.append(Particle(x, y, vel_x, vel_y, radius, color))

#This allows the user to move using the arrow keys and shoot using the up arrow.
    def key_pressed(self,event):
        if event.tk_event.keysym == "Left":
            self.spaceship.x -= 30
        elif event.tk_event.keysym == "Right":
            self.spaceship.x += 30
        elif event.tk_event.keysym == "Up":
            self.b_list.append(Bullets(x=self.spaceship.x, y=self.spaceship.y, color="white"))

            
    def run_game(self):
        i = 0
        while i < 50:
            self.add_particle(-randint(100, 10000))
            i += 1
           
        
    def draw_frame(self):
        
        for bullets in self.b_list:
            if bullets.x > 1000:
                self.score += 1
                #self.score_text.text=self.score
                self.score_text.destroy()
                self.score_text = Text(app, text=self.score, grid=[0,1])
                self.b_list.remove(bullets)
            elif bullets.y < -10:
                self.b_list.remove(bullets)
                
        
        self.drawing.clear()
        for particle in self.p_list:
            particle.move(self.drawing)
        for bullet in self.b_list:
            bullet.move(self.drawing)
        #asteroids gets hit
        for i in range(len(self.p_list)):
            for j in range(len(self.b_list)):
                self.p_list[i].collision(self.b_list[j], self.score)
        for particle in self.p_list:
            particle.draw(self.drawing)
        for bullet in self.b_list:
            bullet.draw(self.drawing)
                
        


app = App()
PS = ParticleSimulation(app)
app.display()

