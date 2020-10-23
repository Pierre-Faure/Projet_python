from timeit import default_timer as timer

import pandas as pd
import pygame
import random
import sys

fps = 30
pygame.init()
width = 800
height = 600

black = (0, 0, 0)
white = (255, 255, 255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126, 178, 255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)

largeText = pygame.font.SysFont("freesansbold.ttf", 115)
mediumText = pygame.font.SysFont("freesansbold.ttf", 70)
text40 = pygame.font.Font('freesansbold.ttf', 40)
text20 = pygame.font.Font('freesansbold.ttf', 20)

textBoxSpace = 5
textBoxNumber = 0


def button(word, x, y, w, h, ic, ac, action=None):
    """
    function that creates buttons
    :param word: label of the button
    :param x: position on x
    :param y: position on y
    :param w: width of the button
    :param h: height of the button
    :param ic: color
    :param ac: color when mouse on the button
    :param action: function of the button
    :return:
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    buttonText = pygame.font.Font("freesansbold.ttf", 20)
    buttonTextSurf, buttonTextRect = textObjects(word, buttonText, white)
    buttonTextRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(buttonTextSurf, buttonTextRect)


def endGame():
    """
    End screen of the game
    :return:
    """
    global textBoxSpace, textBoxNumber, end, start
    end = timer()
    print("Temps: ", end - start)
    timeTaken = (end - start)
    textBoxSpace = 5
    textBoxNumber = 0
    message = "Temps de jeu: " + str(round(timeTaken)) + "s"
    screen.fill(white)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        button("Oui", (width / 2) - 50, 420, 100, 50, darklightred, lightred, quitGame)
        button("Non", (width / 2) - 50, 500, 100, 50, darklightred, lightred, hangman)

        TextSurf, TextRect = textObjects("Arreter de jouer?", mediumText, darklightred)
        TextRect.center = (width / 2, height / 1.6)
        screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = textObjects(("Le mot etait " + pick + "!"), mediumText, darklightblue)
        TextRect.center = (width / 2, height / 2)
        screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = textObjects(message, largeText, darklightred)
        TextRect.center = (width / 2, 200)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(fps)


def quitGame():
    """
    Quitting game function
    :return:
    """
    pygame.quit()
    sys.exit()


def unpause():
    """
    End of pause function
    :return:
    """
    global pause
    screen.fill(white)
    pause = False


def pause():
    """
    Pause in game function
    :return:
    """
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        TextSurf, TextRect = textObjects("Pause", largeText, black)
        TextRect.center = (width / 2, height / 2)
        screen.blit(TextSurf, TextRect)

        button("Continuer", 150, 450, 100, 50, darklightred, lightred, unpause)
        button("Quitter", 550, 450, 100, 50, darklightblue, lightblue, quitGame)

        pygame.display.update()
        clock.tick(fps)
    screen.fill(white)


def textObjects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def main():
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pendu")

    while True:
        hangman()


def placeLetter(letter):
    global pick, pickSplit
    space = 10
    wordSpace = 0
    while wordSpace < len(pick):
        if letter in pickSplit[wordSpace]:
            TextSurf, TextRect = textObjects(letter, text40, black)
            TextRect.center = ((150 + space), 200)
            screen.blit(TextSurf, TextRect)
        wordSpace += 1
        space += 60

    pygame.display.update()
    clock.tick(fps)


def textBoxLetter(letter):
    global textBoxSpace, textBoxNumber
    if textBoxNumber <= 5:
        TextSurf, TextRect = textObjects(letter, text40, black)
        TextRect.center = ((105 + textBoxSpace), 350)
        screen.blit(TextSurf, TextRect)

    elif textBoxNumber <= 10:
        TextSurf, TextRect = textObjects(letter, text40, black)
        TextRect.center = ((105 + textBoxSpace), 400)
        screen.blit(TextSurf, TextRect)

    elif textBoxNumber <= 15:
        TextSurf, TextRect = textObjects(letter, text40, black)
        TextRect.center = ((105 + textBoxSpace), 450)
        screen.blit(TextSurf, TextRect)

    elif textBoxNumber <= 20:
        TextSurf, TextRect = textObjects(letter, text40, black)
        TextRect.center = ((105 + textBoxSpace), 500)
        screen.blit(TextSurf, TextRect)

    pygame.display.update()
    clock.tick(fps)


def hangman():
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        space = 10
        textBoxSpace = 5

        TextSurf, TextRect = textObjects("Choisir la catégorie", text20, black)
        TextRect.center = ((width / 2), (height / 2))
        screen.blit(TextSurf, TextRect)

        button("Animaux", 150, 450, 150, 100, black, lightgrey, Animals)
        button("Transports", 550, 450, 150, 100, black, lightgrey, Vehicles)
        button("Nourritures", 150, 50, 150, 100, black, lightgrey, Foods)
        button("Sports", 550, 50, 150, 100, black, lightgrey, Sports)

        pygame.display.update()
        clock.tick(fps)


def hangmanGame(category, title):
    global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start
    start = timer()
    chances = 20
    pick = random.choice(category)
    pickSplit = [pick[i:i + 1] for i in range(0, len(pick), 1)]

    screen.fill(white)

    wordSpace = 0
    space = 10

    guesses = ''
    gamePlay = True
    while gamePlay == True:
        guessLett = ''

        if textBoxNumber == 5:
            textBoxSpace = 5
        if textBoxNumber == 10:
            textBoxSpace = 5
        if textBoxNumber == 15:
            textBoxSpace = 5

        while wordSpace < len(pick):
            letterBox_surf, letterBox_rect = textObjects("_", text40, black)
            letterBox_rect.center = ((150 + space), 200)
            screen.blit(letterBox_surf, letterBox_rect)
            space = space + 60
            wordSpace += 1

        pygame.draw.rect(screen, white, [550, 20, 200, 20])
        TextSurf, TextRect = textObjects(("Chances: %s" % chances), text20, black)
        TextRect.topright = (700, 20)
        screen.blit(TextSurf, TextRect)

        TextTitleSurf, TextTitleRect = textObjects(title, text40, black)
        TextTitleRect.center = ((width / 2), 50)
        screen.blit(TextTitleSurf, TextTitleRect)

        pygame.draw.rect(screen, black, [100, 300, 250, 250], 2)

        if chances == 19:
            pygame.draw.rect(screen, black, [450, 550, 100, 10])
        elif chances == 18:
            pygame.draw.rect(screen, black, [550, 550, 100, 10])
        elif chances == 17:
            pygame.draw.rect(screen, black, [650, 550, 100, 10])
        elif chances == 16:
            pygame.draw.rect(screen, black, [500, 450, 10, 100])
        elif chances == 15:
            pygame.draw.rect(screen, black, [500, 350, 10, 100])
        elif chances == 14:
            pygame.draw.rect(screen, black, [500, 250, 10, 100])
        elif chances == 13:
            pygame.draw.rect(screen, black, [500, 250, 150, 10])
        elif chances == 12:
            pygame.draw.rect(screen, black, [600, 250, 100, 10])
        elif chances == 11:
            pygame.draw.rect(screen, black, [600, 250, 10, 50])
        elif chances == 10:
            pygame.draw.line(screen, black, [505, 505], [550, 550], 10)
        elif chances == 9:
            pygame.draw.line(screen, black, [550, 250], [505, 295], 10)
        elif chances == 8:
            pygame.draw.line(screen, black, [505, 505], [460, 550], 10)
        elif chances == 7:
            pygame.draw.circle(screen, darklightred, [605, 325], 30)
        elif chances == 6:
            pygame.draw.rect(screen, darklightred, [600, 350, 10, 60])
        elif chances == 5:
            pygame.draw.rect(screen, darklightred, [600, 410, 10, 60])
        elif chances == 4:
            pygame.draw.line(screen, darklightred, [605, 375], [550, 395], 10)
        elif chances == 3:
            pygame.draw.line(screen, darklightred, [605, 375], [650, 395], 10)
        elif chances == 2:
            pygame.draw.line(screen, darklightred, [605, 465], [550, 485], 10)
        elif chances == 1:
            pygame.draw.line(screen, darklightred, [605, 465], [650, 485], 10)

        button("Retour", 50, 50, 100, 50, black, lightgrey, hangman),

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                failed = 0

                if event.key == pygame.K_SPACE:
                    pause()

                if event.key == pygame.K_ESCAPE:
                    gamePlay = False

                if event.key == pygame.K_a:
                    # lettre q
                    guessLett = guessLett + 'q'
                    guesses += guessLett
                    for char in pick:
                        if char not in guesses:
                            failed += 1

                    if guessLett in pick:
                        placeLetter('q')

                    if failed == 0:
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        textBoxLetter('q')

                    if chances == 0:
                        endGame()

                if event.key == pygame.K_b:
                    # lettre b
                    guessLett = guessLett + 'b'
                    guesses += guessLett
                    for char in pick:
                        if char not in guesses:
                            failed += 1

                    if guessLett in pick:
                        placeLetter('b')

                    if failed == 0:
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        textBoxLetter('b')

                    if chances == 0:
                        endGame()

                if event.key == pygame.K_c:
                    # lettre c
                    guessLett = guessLett + 'c'
                    guesses += guessLett
                    for char in pick:
                        if char not in guesses:
                            failed += 1

                    if guessLett in pick:
                        placeLetter('c')

                    if failed == 0:
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        textBoxLetter('c')

                    if chances == 0:
                        endGame()

                if event.key == pygame.K_d:
                    # lettre d
                    guessLett = guessLett + 'd'
                    guesses += guessLett
                    for char in pick:
                        if char not in guesses:
                            failed += 1

                    if guessLett in pick:
                        placeLetter('d')

                    if failed == 0:
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        textBoxLetter('d')

                    if chances == 0:
                        endGame()

                if event.key == pygame.K_e:
                    # lettre e
                    guessLett = guessLett + 'e'
                    guesses += guessLett
                    for char in pick:
                        if char not in guesses:
                            failed += 1

                    if guessLett in pick:
                        placeLetter('e')

                    if failed == 0:
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        textBoxLetter('e')

                    if chances == 0:
                        endGame()

                if event.key == pygame.K_f:
                    # lettre f
                    guessLett = guessLett + 'f'
                    guesses += guessLett
                    print("letter f guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('f')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('f')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_g:
                    # letter g
                    guessLett = guessLett + 'g'
                    guesses += guessLett
                    print("letter g guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('g')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('g')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_h:
                    # letter h
                    guessLett = guessLett + 'h'
                    guesses += guessLett
                    print("letter h guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('h')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('h')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_i:
                    # letter i
                    guessLett = guessLett + 'i'
                    guesses += guessLett
                    print("letter i guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('i')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('i')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_j:
                    # letter j
                    guessLett = guessLett + 'j'
                    guesses += guessLett
                    print("letter j guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('j')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # gamePlay = False
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('j')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # gamePlay = False
                        endGame()

                if event.key == pygame.K_k:
                    # letter k
                    guessLett = guessLett + 'k'
                    guesses += guessLett
                    print("letter k guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('k')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('k')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_l:
                    # letter l
                    guessLett = guessLett + 'l'
                    guesses += guessLett
                    print("letter l guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('l')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('l')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_SEMICOLON:
                    # letter m
                    guessLett = guessLett + 'm'
                    guesses += guessLett
                    print("letter m guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('m')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('m')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_n:
                    # letter n
                    guessLett = guessLett + 'n'
                    guesses += guessLett
                    print("letter n guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('n')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # gamePlay = False
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('n')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # gamePlay = False
                        endGame()

                if event.key == pygame.K_o:
                    # letter o
                    guessLett = guessLett + 'o'
                    guesses += guessLett
                    print("letter o guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('o')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('o')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_p:
                    # letter p
                    guessLett = guessLett + 'p'
                    guesses += guessLett
                    print("letter p guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('p')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('p')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_q:
                    # letter q
                    guessLett = guessLett + 'a'
                    guesses += guessLett
                    print("letter a guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('a')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('a')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_r:
                    # letter r
                    guessLett = guessLett + 'r'
                    guesses += guessLett
                    print("letter r guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('r')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('r')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_s:
                    # letter s
                    guessLett = guessLett + 's'
                    guesses += guessLett
                    print("letter s guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('s')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('s')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_t:
                    # letter t
                    guessLett = guessLett + 't'
                    guesses += guessLett
                    print("letter t guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('t')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('t')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_u:
                    # letter u
                    guessLett = guessLett + 'u'
                    guesses += guessLett
                    print("letter u guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('u')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('u')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_v:
                    # letter v
                    guessLett = guessLett + 'v'
                    guesses += guessLett
                    print("letter v guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('v')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('v')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_w:
                    # letter w
                    guessLett = guessLett + 'z'
                    guesses += guessLett
                    print("letter z guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('z')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('z')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_x:
                    # letter x
                    guessLett = guessLett + 'x'
                    guesses += guessLett
                    print("letter x guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('x')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('x')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_y:
                    # letter y
                    guessLett = guessLett + 'y'
                    guesses += guessLett
                    print("letter y guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('y')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('y')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_z:
                    # letter z
                    guessLett = guessLett + 'w'
                    guesses += guessLett
                    print("letter w guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('w')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('w')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        endGame()

                if event.key == pygame.K_z:
                    letter = 'a'
                if event.key == pygame.K_z:
                    letter = 'b'
                if event.key == pygame.K_z:
                    letter = 'c'
                if event.key == pygame.K_z:
                    letter = 'd'
                if event.key == pygame.K_z:
                    letter = 'e'
                if event.key == pygame.K_z:
                    letter = 'f'
                if event.key == pygame.K_z:
                    letter = 'g'
                if event.key == pygame.K_z:
                    letter = 'h'
                if event.key == pygame.K_z:
                    letter = 'i'
                if event.key == pygame.K_z:
                    letter = 'j'
                if event.key == pygame.K_z:
                    letter = 'k'
                if event.key == pygame.K_z:
                    letter = 'l'
                if event.key == pygame.K_z:
                    letter = 'm'
                if event.key == pygame.K_z:
                    letter = 'n'
                if event.key == pygame.K_z:
                    letter = 'o'
                if event.key == pygame.K_z:
                    letter = 'p'
                if event.key == pygame.K_z:
                    letter = 'q'
                if event.key == pygame.K_z:
                    letter = 'r'
                if event.key == pygame.K_z:
                    letter = 's'
                if event.key == pygame.K_z:
                    letter = 't'
                if event.key == pygame.K_z:
                    letter = 'u'
                if event.key == pygame.K_z:
                    letter = 'v'
                if event.key == pygame.K_z:
                    letter = 'w'
                if event.key == pygame.K_z:
                    letter = 'x'
                if event.key == pygame.K_z:
                    letter = 'y'
                if event.key == pygame.K_z:
                    letter = 'z'

        pygame.display.update()
        clock.tick(fps)

    pygame.display.update()
    clock.tick(fps)


def Animals():
    df = pd.read_csv('data/motscsv.csv', sep=';')
    animal = list(df['Animaux'])
    animal = [item.lower() for item in animal]

    print("animal")
    title = "Animaux"
    hangmanGame(animal, title)


def Vehicles():
    df = pd.read_csv('data/motscsv.csv', sep=';')
    vehicle = list(df['Transport'])
    vehicle = [item.lower() for item in vehicle]

    print("vehicle")
    title = "Transports"
    hangmanGame(vehicle, title)


def Foods():
    df = pd.read_csv('data/motscsv.csv', sep=';')
    food = list(df['Nourriture'])
    food = [item.lower() for item in food]

    print("food")
    title = "Nourritures"
    hangmanGame(food, title)


def Sports():
    df = pd.read_csv('data/motscsv.csv', sep=';')
    sport = list(df['Sport'])
    sport = [item.lower() for item in sport]

    print("sport")
    title = "Sports"
    hangmanGame(sport, title)


if __name__ == '__main__':
    main()
