# Joueur A

import radio
import random
from microbit import *

radio.config(group=10) # Canal radio
a_pad, b_pad = 2, 2 # Position des pads
pad_map = [4,3,2,1]
ball_x = 3 # Position de départ de la balle
ball_y = 2
directions = [1, -1] # Direction aléatoire pour la balle
x_direction = random.choice(directions)
y_direction = random.choice(directions)
delay = 500 # 1sec de delay
counter = 0

a_points = 0 # Score du joueur A
b_points = 0 # Score du joueur B
winning_score = 5 # Score à atteindre pour gagner

def move_ball():
    global ball_x, ball_y, x_direction, y_direction, counter, a_pad, b_pad, a_points, b_points, delay
    display.set_pixel(ball_x, ball_y, 0)
    ball_x = ball_x + x_direction
    ball_y = ball_y + y_direction
    if ball_x < 0:	# Rebondir si mur gauche touché
        ball_x = 0
        x_direction = 1
    if ball_x > 4:	# Rebondir si mur droit touché
        ball_x = 4
        x_direction = -1
    if ball_y == 0:
        if ball_x == b_pad:	# Rebondir si joueur B touche la balle
            ball_y = 0
            y_direction = 1
            delay -= 50	 # Vitesse augmenté quand joueur touché
        else:
            # Joueur A obtient 1 point si Joueur B a raté la balle
            a_points += 1
            ball_y = 0
            y_direction = 1
            radio.send('a'+str(a_points))# Transmet les points à joueur B

    if ball_y == 4:	# Rebondir si joueur A touche la balle
        if ball_x == a_pad:
            ball_y = 4
            y_direction = -1
            delay -= 50
        else:
            # Joueur B obtient 1 point si Joueur A rate la balle
            b_points += 1
            ball_y = 4
            y_direction = -1
            radio.send('b'+str(b_points))
    counter = 0
    radio.send('x'+str(ball_x))	# Transmet la position de la balle
    radio.send('y'+str(ball_y))

radio.on()
game_over = False
while not game_over:
    counter += 1
    display.set_pixel(a_pad, 4, 6)  # Créér le pad
    display.set_pixel(b_pad, 0, 6)
    display.set_pixel(ball_x, ball_y, 9)  # Créér la balle
    if button_a.was_pressed():
        display.set_pixel(a_pad, 4, 0)
        a_pad = a_pad - 1
        if a_pad < 0:
            a_pad = 0
        radio.send('p'+str(a_pad))
    if button_b.was_pressed():
        display.set_pixel(a_pad, 4, 0)
        a_pad = a_pad + 1
        if a_pad > 4:
            a_pad = 4
        radio.send('p'+str(a_pad))
    incoming = radio.receive()
    if incoming:
        display.set_pixel(b_pad, 0, 0)
        b_pad = pad_map[int(incoming)]
    if counter == delay:
        move_ball()
    if a_points == winning_score or b_points == winning_score:
        game_over = True

if a_points > b_points:
    display.show(Image.HAPPY)
else:
    display.show(Image.SAD)
sleep(250)
display.scroll(f'{a_points} / {b_points}')