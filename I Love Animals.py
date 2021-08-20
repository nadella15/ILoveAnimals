#set anemy random

from typing import Text
import pygame
import random
import math
from pygame import mixer

pygame.init()

# membuat layar
screen = pygame.display.set_mode((800, 600))

# Caption dan Icon
pygame.display.set_caption("I Love Animals")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

#background
bg_layar = pygame.image.load('assets/background.png')

#background sound
mixer.music.load('assets/skyzoo.wav')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('assets/player.png')
playerX = 340 #posisi
playerY = 440
playerX_change = 0

#enemy_gajah
enemyImg = [] #untuk multiple enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
jumlah_enemy = 10

for i in range(jumlah_enemy):
    enemyImg.append(pygame.image.load('assets/enemy_gajah.png')) #penggunaan fungsi .append
    enemyX.append(random.randint(100, 735)) #posisi #random
    enemyY.append(random.randint(50, 150)) 
    enemyX_change.append(4) #semula 1, diubah karena delay pergerakan enemynya
    enemyY_change.append(40) #posisi enemy kebawah menuju player

#bullet_love
bulletImg = pygame.image.load('assets/bullet_love.png')
bulletX = 0 #posisi bullet peluru love
bulletY = 480
bulletX_change = 0 #posisi love bullet
bulletY_change = 10 #posisi love bullet
bullet_state = "siap"

#score font
jumlah_score = 0
font = pygame.font.Font('freesansbold.ttf', 38)

textX = 325 #letak posisi text score
textY = 10

#dead font <=====
over_font = pygame.font.Font('freesansbold.ttf', 64)


#======================================================
def munculkan_score(x,y):
    score = font.render("Score :" + str(jumlah_score), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text(): # <===
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def love_bullet(x, y):
    global bullet_state
    bullet_state = "love"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 100: #100 adalah ukuran kepekaan terhadap terkenanya peluru dengan enemy_gajah
        return True
    else:
        return False


#======================================================

# Game Loop
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(bg_layar, (0,0)) #background layar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  #tekan tombol ke kiri atau kanan per 1 detik
            if event.key == pygame.K_LEFT:
                playerX_change = -5 #semula (-1), diubah karena delay pergerakan playernya
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
            if event.key == pygame.K_LEFT or event.key == pygame.K_SPACE:
                if bullet_state is "siap": #bullet keluar ketika keadaan tekan spasi dan menunggu bullet sampai/ hanya sekali per shoot
                    bullet_sound = mixer.Sound('assets/S2KVCQ4-laser-hit.wav') # sound bullet tembakan love <===== 
                    bullet_sound.play()

                    bulletX = playerX
                    love_bullet(playerX, bulletY) #posisi arah love menembak

#=================================================================================================  
    #Set agar tidak keluar dari boarder
    #posisi player pindah
    #5 = (5 + -0.1) -> 5 = (5 - 0.1) #5 adalah tiap titik x yang diubah ke kiri atau kanan
    playerX += playerX_change
    
    if playerX <= 0: #set player batas border layar 
        playerX = 0
    elif playerX >= 672: #titik lebar koordinat x pada layar adalah 800
        playerX = 672

    #posisi enemy move
    for i in range(jumlah_enemy): #jumlah enemy yang keluar [i]
        #Dead <=====
        # Game Over
        if enemyY[i] > 380:
            for j in range(jumlah_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0: #set player batas border layar 
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i] #posisi random enemy dikoordinat y
        elif enemyX[i] >= 672: #titik lebar koordinat x pada layar adalah 800
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i] #posisi random enemy dikoordinat y
        
        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            aksi_sound = mixer.Sound('assets/8BLMWFP-female-child-i-love-you.wav') # sound bullet setelah tembakan love <===== 
            aksi_sound.play()

            bulletY = 480
            bullet_state = "siap"
            jumlah_score += 1 #set score
            enemyX[i] = random.randint(0, 672) #posisi #random
            enemyY[i] = random.randint(50, 150) 
        
        enemy(enemyX[i], enemyY[i], i)


    #posisi bullet love move
    if bulletY <= 0: #multiple bullet love
        bulletY = 480
        bullet_state = "siap"
    if bullet_state is "love":
        love_bullet (bulletX, bulletY)
        bulletY -= bulletY_change


#================================================================================================= 

    player(playerX, playerY)
    munculkan_score(textX, textY)
    pygame.display.update()
