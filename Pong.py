import simplegui
import random

WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [2, -random.random()*2]
    else:
        ball_vel = [-2, -random.random()*2]
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([LEFT,RIGHT]))
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    c.draw_line([WIDTH/2,0], [WIDTH/2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH-PAD_WIDTH, 0], [WIDTH-PAD_WIDTH, HEIGHT], 1,"White")

    #update ball
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        #reach left
        if paddle1_pos - HALF_PAD_HEIGHT < ball_pos[1] and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
        else:
            score2 = score2 + 1
            spawn_ball(RIGHT);
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        #reach right
        if paddle2_pos - HALF_PAD_HEIGHT < ball_pos[1] and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
        else:
            score1 = score1 + 1
            spawn_ball(LEFT);
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        #reach top or buttom
        ball_vel[1] = -ball_vel[1]
    
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    ball_vel[0] = ball_vel[0]*1.001
    ball_vel[1] = ball_vel[1]*1.001
    
    #draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    #update paddle's vertical position, keep paddle on the screen
    paddle1_pos = paddle1_pos + paddle1_vel
    if HALF_PAD_HEIGHT > paddle1_pos:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos >  HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    paddle2_pos = paddle2_pos + paddle2_vel
    if HALF_PAD_HEIGHT > paddle2_pos:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos >  HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        

    
    #draw paddles
    c.draw_line([0, paddle1_pos], [PAD_WIDTH, paddle1_pos], PAD_HEIGHT, "White")
    c.draw_line([WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH, paddle2_pos], PAD_HEIGHT, "White")

    #draw scores
    c.draw_text(str(score1), (200, 100), 48, "White")
    c.draw_text(str(score2), (400, 100), 48, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -2
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 2
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -2
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 2
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

new_game()
frame.start()
    