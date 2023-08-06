#! /usr/bin/python3

from config import *
import numpy as np
import arcade as ar
import brains
import snakes
import random
import math


class MyApplication(ar.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title="AI Snakes", resizable=False)
        self.snakes = {}
        self.apples = []
        self.last_id = 0
        self.buttons = {ar.key.UP: False, ar.key.RIGHT: False, ar.key.DOWN: False, ar.key.LEFT: False}
        self.longest = 0
        self.oldest = 0

    def setup(self):
        self.snakes = {}
        for _ in range(SNAKES):
            self.spawn_snake()
        self.apples = [snakes.Apple(self) for _ in range(APPLES)]
        ar.schedule(self.move, 0.05)

    def update(self, dt):
        for snake_id in self.snakes:
            self.snakes[snake_id].update()

    def move(self, dt=None):
        for snake_id in list(self.snakes):
            self.snakes[snake_id].move()

    def on_draw(self):
        ar.start_render()

        ar.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, BACKGROUND_COLOR)

        for y in range(0, SCREEN_HEIGHT + 1, RECT_HEIGHT):
            ar.draw_line(0, y, SCREEN_WIDTH, y, GRID_COLOR, 1)

        for x in range(0, SCREEN_WIDTH + 1, RECT_WIDTH):
            ar.draw_line(x, 0, x, SCREEN_HEIGHT, GRID_COLOR, 1)

        for snake_id in self.snakes:
            self.snakes[snake_id].draw()

        for apple in self.apples:
            apple.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.buttons.keys():
            self.buttons[symbol] = True

    def on_key_release(self, symbol, modifier):
        if symbol in self.buttons.keys():
            self.buttons[symbol] = False

    def snake_died(self, id):
        if self.snakes[id].longest > self.longest:
            self.longest = self.snakes[id].longest
            print("New high score. Snake number %d died with %d segments." % (id, self.longest))

        if self.snakes[id].ticks > self.oldest:
            self.oldest = self.snakes[id].ticks
            print("New high score. Snake number %d survived %d ticks." % (id, self.oldest))

        del self.snakes[id]
        self.spawn_snake(*self.get_surviving_DNA())

    def get_free_place(self):
        pos = None
        while not pos or any([self.snakes[snake_id].lays_on(pos) for snake_id in self.snakes] + [apple.lays_on(pos) for apple in self.apples]):
            pos = [math.floor(random.random() * (SCREEN_WIDTH // RECT_WIDTH)),
                   math.floor(random.random() * (SCREEN_HEIGHT // RECT_HEIGHT))]
        return pos

    def spawn_snake(self, W1=None, W2=None):
        self.last_id += 1
        self.snakes[self.last_id] = snakes.Snake(self.get_free_place(), self, brains.NN(self, W1, W2), self.last_id)

    def get_surviving_DNA(self):
        best_one = [np.array([]), 0]
        best_two = [np.array([]), 0]
        for snake_id in self.snakes:
            score = len(self.snakes[snake_id].body)*self.snakes[snake_id].ticks
            if score >= best_one[1]:
                best_two = best_one
                best_one = [self.snakes[snake_id].brain.W, score]
            elif score > best_two[1] or best_two[1] == 0:
                best_two = [self.snakes[snake_id].brain.W, score]
        return best_one[0], best_two[0]


window = MyApplication()
window.setup()

ar.run()
