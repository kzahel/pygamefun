# Example file showing a circle moving on screen
import pygame
import time
import random
from typing import List
import math

pygame.init()


FULLSCREEN = True

if FULLSCREEN:
    screen_sz = (1728, 1117)
else:
    screen_sz = (1280, 720)

screenw = screen_sz[0]
screenh = screen_sz[1]

screen = pygame.display.set_mode(screen_sz)
if FULLSCREEN:
    pygame.display.toggle_fullscreen()


clock = pygame.time.Clock()
running = True
dt = 0
background_color = (0, 10, 30, 255)


def randpos():
    pad = 30
    return pygame.Vector2(
        random.randrange(pad, screen.get_width() - pad),
        random.randrange(pad, screen.get_height() - pad),
    )


def checkbg(pos: pygame.Vector2):
    intpos = [int(pos.x), int(pos.y)]
    if intpos[0] < 0 or intpos[0] >= screenw:
        return True
    if intpos[1] < 0 or intpos[1] >= screenh:
        return True

    try:
        color = screen.get_at(intpos)
    except:
        return True

    if color == background_color:
        return True


class Player:
    def __init__(self, name: str, game: "Game", color=None, pos=None, binds=None):
        self.name = name
        self.game = game
        self.binds: dict = binds or {}
        self.pos = pygame.Vector2((pos[0], pos[1])) if pos else randpos()
        self.vec = pygame.Vector2((1, 0))
        self.color = color or randcolor()
        self.size = 3
        self.speed = 1
        self.dead = False
        self.deadtime = time.time()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def update(self):
        if self.dead and time.time() - self.deadtime > 2:
            self.dead = False
            self.pos = randpos()
        if self.dead:
            return
        checkpos = self.pos + self.vec * self.speed * 5

        if not checkbg(checkpos):
            self.die()

        self.pos = self.pos + self.vec * self.speed

    def die(self):
        print(f"player {self.name} dies!")
        self.deadtime = time.time()
        self.dead = True

    def turn_left(self):
        self.vec = self.vec.rotate(-90)

    def turn_right(self):
        self.vec = self.vec.rotate(90)

    def speedup(self):
        self.speed = 2

    def speednormal(self):
        self.speed = 1

    def shoot(self):
        self.game.bullets.append(Bullet(self))

    def handle_event(self, event: pygame.event.Event):
        if event.key in self.binds:
            command = self.binds[event.key]
            if hasattr(self, command):
                getattr(self, command)()


class Bullet:
    def __init__(self, player: Player):
        self.player = player
        self.speed = 2
        self.vec = player.vec.normalize() * self.speed
        self.pos = player.pos + self.vec
        self.color = (255, 255, 255)
        self.size = 4

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def clear(self):
        pygame.draw.circle(screen, background_color, self.pos, self.size + 1)

    def update(self):
        self.pos += self.vec * self.speed


def clamp_players(players: List[Player]):
    for player in players:
        if player.pos.x < 0:
            player.pos.x = screen.get_width()
        if player.pos.x > screen.get_width():
            player.pos.x = 0
        if player.pos.y < 0:
            player.pos.y = screen.get_height()
        if player.pos.y > screen.get_height():
            player.pos.y = 0


def randcolor():
    return (
        random.randrange(0, 256),
        random.randrange(0, 256),
        random.randrange(0, 256),
    )


p1_binds = {
    pygame.K_o: "turn_left",
    pygame.K_u: "turn_right",
    pygame.K_PERIOD: "shoot",
}
p2_binds = {
    pygame.K_LEFT: "turn_left",
    pygame.K_RIGHT: "turn_right",
    pygame.K_UP: "shoot",
}


class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.bullets: List[Bullet] = []
        self.fps = 120

    def reset(self):
        pad = 100
        screen.fill(background_color)

        self.players = [
            Player("player1", self, "red", (pad, screenh - pad * 2), p1_binds),
            Player("player2", self, "blue", (pad, pad), p2_binds),
        ]
        self.bullets = []

        self.running = False

    def start(self):
        self.running = True
        while self.running:
            self.loop()

    def loop(self):
        self.handle_events()

        for bullet in self.bullets:
            bullet.clear()
            bullet.update()
            bullet.clear()
            bullet.update()
            bullet.draw()

        for player in self.players:
            player.update()
            player.draw()

        clamp_players(self.players)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(self.fps) / 1000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_RETURN:
                    self.reset()

                for player in self.players:
                    if event.key in player.binds:
                        player.handle_event(event)


game = Game()
game.reset()
game.start()

if __name__ == "__main__":
    game.start()


pygame.quit()
