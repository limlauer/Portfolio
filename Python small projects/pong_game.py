import pygame,sys
from pygame.locals import*

pygame.init()
FPS=200
fpsClock=pygame.time.Clock()

# Configuración de la ventana
WINDOW=pygame.display.set_mode((400,300),0,32)
pygame.display.set_caption('Ping Pong')

# Configuración de los colores
WHITE=(255,255,255)
BLACK=(0,0,0)

# Configuración de las paletas y la pelota
ball=pygame.Rect(200,150,10,10)
player=pygame.Rect(380,200,10,40)
opponent=pygame.Rect(10,200,10,40)

# Configuración de las velocidades de las paletas y la pelota
ball_speed_x=1
ball_speed_y=1
player_speed=0
opponent_speed=5

# Loop principal del juego
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_DOWN:
                player_speed=5
            if event.key==K_UP:
                player_speed=-5
        if event.type==KEYUP:
            if event.key==K_DOWN:
                player_speed=0
            if event.key==K_UP:
                player_speed=0

    ball.x+=ball_speed_x
    ball.y+=ball_speed_y
    player.y+=player_speed

    # Lógica de rebote de la pelota
    if ball.top<=0 or ball.bottom>=300:
        ball_speed_y*=-1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x*=-1

    # Lógica de movimiento del oponente
    if opponent.top<ball.y:
        opponent.y+=opponent_speed
    if opponent.bottom>ball.y:
        opponent.y-=opponent_speed

    # Limitar el movimiento de las paletas dentro de la ventana
    if player.top<=0:
        player.top=0
    if player.bottom>=300:
        player.bottom=300
    if opponent.top<=0:
        opponent.top=0
    if opponent.bottom>=300:
        opponent.bottom=300

    # Si la pelota sale de la pantalla, reiniciarla en el centro
    if ball.left<=0 or ball.right>=400:
        ball.center=(200,150)
    
    # Pintar la pantalla y los objetos
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW,WHITE,player)
    pygame.draw.rect(WINDOW,WHITE,opponent)
    pygame.draw.ellipse(WINDOW,WHITE,ball)
    pygame.draw.aaline(WINDOW,WHITE,(200,0),(200,300))

    pygame.display.update()
    fpsClock.tick(FPS)
