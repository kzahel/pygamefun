# Example file showing a circle moving on screen
import pygame
import random
from typing import List
import math

# pygame setup
pygame.init()
screen_sz = (1728, 1117)
screen = pygame.display.set_mode(screen_sz)
clock = pygame.time.Clock()
running = True
dt = 0
background_color = (0, 10, 30)


def randpos():
    pad = 30
    return pygame.Vector2(
        random.randrange(pad, screen.get_width() - pad),
        random.randrange(pad, screen.get_height() - pad),
    )


players = []
monsters = []
trees = []


def randcolor():
    return (
        random.randrange(0, 256),
        random.randrange(0, 256),
        random.randrange(0, 256),
    )


def randmonster(pos=None):
    return {
        "pos": pos or randpos(),
        "size": random.random() * 20 + 5,
        "color": randcolor(),
        "speed": random.random() * 0.5,
    }


def maketrees():
    trees = []
    for _ in range(10):
        trees.append(
            {
                "pos": randpos(),
                "size": random.randrange(20, 100),
            }
        )
    return trees


def reset():
    global players
    global monsters
    global trees

    trees = maketrees()
    players = [
        {"pos": randpos(), "speed": 300, "color": "red", "size": 20},
        {"pos": randpos(), "speed": 200, "color": "yellow", "size": 30},
    ]
    monsters = []
    for _ in range(10):
        monsters.append(randmonster())


reset()


def monstermove(
    mvec: pygame.Vector2, pvecs: List[pygame.Vector2], speed: int, scared=False
):
    distances = [mvec.distance_to(p) for p in pvecs]
    if not pvecs:
        return mvec
    mval = min(distances)
    idx = distances.index(mval)

    player = pvecs[idx]

    # angle = mvec.angle_to(player)

    if scared:
        return mvec.move_towards(player, speed * -1)
    else:
        return mvec.move_towards(player, speed)


def update_player_size(player, monster):
    player_area = (player["size"] / 2) ** 2
    monster_area = (monster["size"] / 2) ** 2

    new_area = player_area + monster_area

    new_diam = math.sqrt(new_area) * 2

    player["size"] = new_diam


def reset_positions():
    global players

    for player in players:
        player["pos"] = randpos()


def get_hidden_by(player, trees):
    player_pos: pygame.Vector2 = player["pos"]
    for tree in trees:
        if tree["size"] < player["size"]:
            continue
        else:
            rad_diff = tree["size"] - player["size"]
            dist = player_pos.distance_to(tree["pos"])

            if dist < rad_diff:
                return tree


def clamp_players(players):
    for player in players:
        if player["pos"].x < 0:
            player["pos"].x = 0
        if player["pos"].x > screen.get_width():
            player["pos"].x = screen.get_width()
        if player["pos"].y < 0:
            player["pos"].y = 0
        if player["pos"].y > screen.get_height():
            player["pos"].y = screen.get_height()


pygame.display.toggle_fullscreen()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # trees.append({"size": random.randrange(20, 100), "pos": pos})
            pos = pygame.Vector2(pos)
            monsters.append(randmonster(pos))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_color)

    for player in players:
        pygame.draw.circle(screen, player["color"], player["pos"], player["size"])

    for monster in monsters:
        monster["pos"] = monstermove(
            monster["pos"],
            [p["pos"] for p in players if not get_hidden_by(p, trees)],
            monster["speed"],
            scared=True,
        )

        pygame.draw.circle(screen, monster["color"], monster["pos"], monster["size"])

    for tree in trees:
        pygame.draw.circle(screen, (0, 100, 0), tree["pos"], tree["size"])

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_RETURN]:
        # reset_positions()
        reset()

    if keys[pygame.K_SPACE]:
        sp2 = 500
    else:
        sp2 = 200

    if keys[pygame.K_RSHIFT]:
        sp1 = 600
    else:
        sp1 = 300

    if keys[pygame.K_9]:
        for _ in range(100):
            monsters.append(randmonster())

    if keys[pygame.K_UP]:
        players[0]["pos"].y -= sp1 * dt
    if keys[pygame.K_DOWN]:
        players[0]["pos"].y += sp1 * dt
    if keys[pygame.K_LEFT]:
        players[0]["pos"].x -= sp1 * dt
    if keys[pygame.K_RIGHT]:
        players[0]["pos"].x += sp1 * dt

    if len(players) > 1:
        if keys[pygame.K_PERIOD]:
            players[1]["pos"].y -= sp2 * dt
        if keys[pygame.K_e]:
            players[1]["pos"].y += sp2 * dt
        if keys[pygame.K_o]:
            players[1]["pos"].x -= sp2 * dt
        if keys[pygame.K_u]:
            players[1]["pos"].x += sp2 * dt

    # clamp_players(players)
    clamp_players(monsters)

    deadmonsters = []

    for player in players:
        for monster in monsters:
            player = get_hidden_by(monster, players)
            if player:
                update_player_size(player, monster)

                deadmonsters.append(monster)

    for m in deadmonsters:
        if m in monsters:
            monsters.remove(m)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()
