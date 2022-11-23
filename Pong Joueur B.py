# Joueur B

import radio
from microbit import *

radio.config(group=10)

a_pad = 2 # Position du pad A
b_pad = 2 # Position du pad B
pad_map = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0} # écran inversé
ball_x = 2 # Position de la balle
ball_y = 2
a_points = 0
b_points = 0
winning_score = 5

def parse_message(incoming): # analyser message
    global a_pad, bat_map, ball_x, ball_y, a_points, b_points
    msg_type = incoming[:1] # Type de message reçu
    msg = incoming[1:] # Contenu du message
    if msg_type == 'p':
        display.set_pixel(a_pad, 0, 0)
        their_pad = int(msg) # Recopie la position du pad adverse
        a_pad = pad_map[their_pad]
    if msg_type == 'x':
        display.set_pixel(ball_x, ball_y, 0)
        ball_x = pad_map[int(msg)]
    if msg_type == 'y':
        display.set_pixel(ball_x, ball_y, 0)
        ball_y = pad_map[int(msg)]
    if msg_type == 'a':
        a_points = int(msg)
    if msg_type == 'b':
        b_points = int(msg)

radio.on()
game_over = False
while not game_over:
    display.set_pixel(b_pad, 4, 6)
    display.set_pixel(a_pad, 0, 6)
    display.set_pixel(ball_x, ball_y, 9) # Créér la balle
    if button_a.was_pressed():
        display.set_pixel(b_pad, 4, 0)
        b_pad = b_pad - 1
        if b_pad < 0:
            b_pad = 0
        radio.send(str(b_pad))
    if button_b.was_pressed():
        display.set_pixel(b_pad, 4, 0)
        b_pad = b_pad + 1
        if b_pad > 4:
            b_pad = 4
        radio.send(str(b_pad))
    incoming = radio.receive()
    if incoming:
        parse_message(incoming)
    if a_points == winning_score or b_points == winning_score:
        game_over = True

if b_points > a_points:
    display.show(Image.HAPPY)
else:
    display.show(Image.SAD)
sleep(250)
display.scroll(f'{a_points} / {b_points}')