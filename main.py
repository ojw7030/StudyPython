import pygame
import sys
import random, time
from time import sleep


BLACK = (0, 0, 0)
padWidth = 480      # 가로크기
padHeight = 640     # 세로크기
enemyImage = ["C:/Python3/VScodeP3.9/projectRiden/air.png", "C:/Python3/VScodeP3.9/projectRiden/air2.png", 
 "C:/Python3/VScodeP3.9/projectRiden/air3.png",  "C:/Python3/VScodeP3.9/projectRiden/air4.png",]

# 객체 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter, missile, boom
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("Riden")     # 이름
    background = pygame.image.load("C:/Python3/VScodeP3.9/projectRiden/background.png") # 배경 - 경로설정 필수
    fighter = pygame.image.load("C:/Python3/VScodeP3.9/projectRiden/flight.png")        # 비행기
    missile = pygame.image.load("C:/Python3/VScodeP3.9/projectRiden/mis.png")
    boom = pygame.image.load("C:/Python3/VScodeP3.9/projectRiden/boom.png")
    clock = pygame.time.Clock()

def runGame():
    global gamepad, clock, background, fighter, missile, boom

    missileXY = [] # 무기좌표

    # 적 랜덤 생성
    time.sleep(random.randrange(1, 5))
    enemy = pygame.image.load(random.choice(enemyImage))
    enemySize = enemy.get_rect().size   # 적 크기
    enemyWidth = enemySize[0]
    enemyHeight = enemySize[1]

    # 적 초기 위치 설정
    enemyX = random.randrange(0, padWidth - enemyWidth)
    enemyY = 0
    enemySpeed = 4


    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # 미사일 적중 여부
    isShot = False
    shotCount = 0
    ePass = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:     # 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:      # 왼쪽이동
                    fighterX -= 5
                
                elif event.key == pygame.K_RIGHT:   # 오른쪽 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE:   # 미사일 발사
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
            
            if event.type in [pygame.KEYUP]:        # 키 안누름
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                    

        drawObject(background, 0, 0) # 배경화면 그리기

        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        #gamePad.fill(BLACK)     # 화면 (검은색 채움)

        drawObject(fighter, x, y)    # 화면속 비행기 배치

        if len(missileXY) != 0:    # 미사일 발사
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                # 미사일에 적 적중판정
                if bxy[1] < enemyY:
                    if bxy[0] > enemyX-15 and bxy[0] < enemyX + enemyWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:  # 화면에서 벗어남 - > 제거
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        enemyY += enemySpeed    # 적 낙하
        # 지나쳐갔을경우
        if enemyY > padHeight:
            # 새로운 적군
            enemy = pygame.image.load(random.choice(enemyImage))
            enemySize = enemy.get_rect().size   # 적 크기
            enemyWidth = enemySize[0]
            enemyHeight = enemySize[1]
            enemyX = random.randrange(0, padWidth - enemyWidth)
            enemyY = 0
        
        # 맞췃으면
        if isShot:
            drawObject(boom, enemyX, enemyY)    # 폭발그리기
            
            enemy = pygame.image.load(random.choice(enemyImage)) # 새로운 적 출현
            enemySize = enemy.get_rect().size   
            enemyWidth = enemySize[0]
            enemyHeight = enemySize[1]
            enemyX = random.randrange(0, padWidth - enemyWidth)
            enemyY = 0
            isShot = False
        


        drawObject(enemy, enemyX, enemyY) # 적 그림

        pygame.display.update() # 화면을 다시 그린다.

        clock.tick(60)          # 초당 60프레임

    pygame.quit()               # pygame 종료

initGame()
runGame()
