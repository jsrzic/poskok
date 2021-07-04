import pygame, sys, random

pygame.init()
pygame.font.init()

#global variables
clock = pygame.time.Clock()
size = 800
rows = 20
blockSize = size // rows
window = pygame.display.set_mode((size, size))
largeText = pygame.font.Font('OdibeeSans-Regular.ttf', 115)
smallText = pygame.font.Font('OdibeeSans-Regular.ttf', 70)
smallerText = pygame.font.Font('OdibeeSans-Regular.ttf', 50)
with open('highscores.txt') as f:   
    highscores = [tuple(map(lambda x : x.strip(), i.split(','))) for i in f]

bgColor = (0, 0, 0)
gridColor = (255, 255, 255)
snakeColor = (0, 255, 0)
foodColor = (255,165,0)


def storeHighscores():
    f = open('highscores.txt', 'w')
    for user, score in highscores:
        f.write(user + ',' + score + '\n')
    f.close()


def displayGameOverScreen(score):
    pygame.display.set_caption('Poskok')
    icon = pygame.image.load('snake.png')
    pygame.display.set_icon(icon)
    colorInactive = (255, 0, 0)
    colorActive = (0, 255, 0)
    color = colorInactive
    username = ''
    active = False
    displayHS = False
    inputDone = False
    inputBox = pygame.Rect(470, 360, 300, 70) #? values
    

    waiting = True
    while waiting:
        window.fill((bgColor))
        drawText('GAME OVER', largeText, (255, 0, 0), window, size // 2, 80)
        drawText('(press space to play a new game)', smallerText, (255, 0, 0), window, size // 2, 150)
        drawText(f'Your Score: {score}', smallText, (255, 255, 255), window, size // 2, 300)
        drawText('Enter Name: ', smallText, (255, 255, 255), window, 300, 400)
        if displayHS:
            displayHighscores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storeHighscores()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    storeHighscores()
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputBox.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = colorActive if active else colorInactive
            if event.type == pygame.KEYDOWN:
                if active and not inputDone:
                    if event.key == pygame.K_RETURN:
                        inputDone = True
                        highscores.append((username, str(score)))
                        username = ''
                        displayHS = True

                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
        
        inputSurface = smallText.render(username, 1, color)
        window.blit(inputSurface, inputBox)
        pygame.draw.rect(window, color, inputBox, 2)

        pygame.display.update()
        clock.tick(10)


def displayHighscores():
    sortedHighscores = sorted(highscores, key=lambda tup: int(tup[1]), reverse=True)
    i = 1
    for user, highscore in sortedHighscores:
        if i > 5:
            break
        drawText(f'{i}.   {user}    {highscore}', smallerText, (255, 255, 255), window, size // 2, 500 + i*50)
        i += 1

def drawText(text, font, color, window, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.center = (x, y)
    window.blit(textObj, textRect)

def mainMenu():
    pygame.display.set_caption('Poskok')
    icon = pygame.image.load('snake.png')
    pygame.display.set_icon(icon)
    intro = True
    click = False
    displayHS = False
    

    while intro:
        window.fill((bgColor))
        drawText('POSKOK', largeText, (0, 255, 0), window, size // 2, 80)

        mx, my = pygame.mouse.get_pos()

        textObj1 = smallText.render("Start Game", 1, (255, 0, 0)) 
        textObj2 = smallText.render("Toggle High Scores", 1, (255, 0, 0)) 
        button_1 = textObj1.get_rect()
        button_2 = textObj2.get_rect()
        button_1.center = (size //2, 200)
        button_2.center = (size //2, 300)

        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                displayHS = not displayHS

        
        window.blit(textObj1, button_1)
        window.blit(textObj2, button_2)

        if(displayHS):
            displayHighscores()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                

        pygame.display.update()
        clock.tick(10)



def generateFood(snake):
    success = False
    while(not success):
        success = True
        foodX = random.randrange(0, size, blockSize)
        foodY = random.randrange(0, size, blockSize)
        for snakePart in snake:
            if snakePart[0] == foodX and snakePart[1] == foodY:
                success = False
                break
        return (foodX, foodY)


def drawGrid():
    window.fill(bgColor)
    for x in range(0, size, blockSize):
        for y in range(0, size, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(window, gridColor, rect, 1)




def main():
    pygame.display.set_caption('Poskok')
    icon = pygame.image.load('snake.png')
    pygame.display.set_icon(icon)

    drawGrid()
    headX = 400
    headY = 400
    snake = [(400, 400)]
    delta = (0, 0)
    food = generateFood(snake)
    direction = ""
    score = 1
    play = True
    gameOver = False

    while play:
        if gameOver:
            displayGameOverScreen(score)
            gameOver = False
            pygame.display.set_caption('Poskok')
            icon = pygame.image.load('snake.png')
            pygame.display.set_icon(icon)

            drawGrid()
            headX = 400
            headY = 400
            snake = [(400, 400)]
            delta = (0, 0)
            food = generateFood(snake)
            direction = ""
            score = 1
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    delta = (-blockSize, 0)
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    delta = (blockSize, 0)
                    direction = "right"
                elif event.key == pygame.K_DOWN and direction != "up":
                    delta = (0, blockSize)
                    direction = "down"
                elif event.key == pygame.K_UP and direction != "down":
                    delta = (0, -blockSize)
                    direction = "up"
                elif event.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()

        drawGrid()
        foodRect = pygame.Rect(food[0], food[1], blockSize, blockSize)
        pygame.draw.rect(window, foodColor, foodRect, 0)
        

        headX += delta[0]
        headY += delta[1]           
        
        if headX > size - blockSize or headX < 0 or headY > size - blockSize or headY < 0:
            gameOver = True
        

        if delta != (0, 0) and not gameOver:
            if (headX, headY) in snake:
                gameOver = True
            snake.insert(0, (headX, headY))
            if (headX, headY) == food:
                food = generateFood(snake)
                score += 1      
            else:
                snake.pop()
            for i in snake:
                snakeRect = pygame.Rect(i[0], i[1], blockSize, blockSize)
                pygame.draw.rect(window, snakeColor, snakeRect, 0)

            
        
        pygame.display.update()
        clock.tick(10)

    
mainMenu()