import pygame, sys
import constants as CC
from classes import *


def game_loop():
    # Initialisierung aller dynamischen Variablen
    restart_button = None
    running = True
    gameOver = False
    jumpSound = True

    gameSpeed, score = CC.START_GAME_SPEED, 0

    obstacleIntervalTime = CC.OBSTACLE_INTERVAL_TIME

    # Mal 1000 zur Umrechnung in Millisekunden
    startTime, lastTime = (obstacleIntervalTime * 1000), 0

    # Initialisieren aller Elemente mittels der definierten Konstanten
    screen = Screen(CC.WINDOW_NAME, CC.SCREEN_SIZE_X, CC.SCREEN_SIZE_Y, CC.BG_COLOR)
    clock = Clock(CC.FPS)
    stage = GameObject(0, int((3*CC.SCREEN_SIZE_Y)//4), CC.SCREEN_SIZE_X, int(CC.SCREEN_SIZE_Y//4), CC.GROUND_COLOR)
    stage_bg = GameObject(0, int((3*CC.SCREEN_SIZE_Y)//4)-int(CC.PLAYER_SIZE//2), CC.SCREEN_SIZE_X, int(CC.PLAYER_SIZE//2), CC.STAGE_COLOR)
    player = Player(CC.PLAYER_OFFSET_X, int((3*CC.SCREEN_SIZE_Y)//4) - int(CC.PLAYER_SIZE * 1.25), CC.PLAYER_SIZE, CC.PLAYER_SIZE, CC.PLAYER_COLOR, CC.PLAYER_SPEED, 0, CC.JUMP_FORCE, CC.GRAVITY)
    spawner = Spawner(CC.SCREEN_SIZE_X, int((3*CC.SCREEN_SIZE_Y)//4) - int((CC.PLAYER_SIZE//CC.OBSTACLE_SIZE_TO_PLAYER_RATIO) * 1.5),
                    (CC.PLAYER_SIZE//CC.OBSTACLE_SIZE_TO_PLAYER_RATIO), CC.OBSTACLE_COLOR, CC.COIN_COLOR, CC.OBSTACLE_SPEED, 0)
    score = Score(CC.SCREEN_SIZE_X, CC.SCREEN_SIZE_Y, CC.SCORE_FONT, CC.SCORE_FONT_SIZE, CC.FONT_COLOR)
    soundmixer = SoundMixer(CC.JUMP_PATH, CC.COIN_PATH)

    # Laden des Highscores durch die Score-Datei
    highScore = Score(CC.SCREEN_SIZE_X, CC.SCREEN_SIZE_Y, CC.SCORE_FONT, CC.SCORE_FONT_SIZE, CC.FONT_COLOR)
    with open(CC.SCORE_PATH, "r") as f:
        highScore.add(int(f.readline()))
    

    while running:

        # Generieren des Hintergrundes (Einfärbung)
        screen.fill()

        # Zeichnen des Bodens
        stage.draw(screen.screen)
        stage_bg.draw(screen.screen)

        # System zum Bekommen und Auswerten der Eingabe durch die Tastatur als Dictionary
        keys_pressed = pygame.key.get_pressed()

        # Während der Spieler lebt
        if not gameOver:

            # Unterscheidung 
            # Limitieren der Spieler Bewegung innerhalb des Screens und skalieren des Bewegungstempos
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                if (player.rect.x + player.size_x) < CC.SCREEN_SIZE_X:
                    player.move(1 + gameSpeed/10, 0)

            elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                if (player.rect.x) > 0:
                    player.move(-(1 + (gameSpeed/10)), 0)

            # Überprüfung des Sprungknopfes, Boolean zum Limitieren auf einen Sprung zur gleichen Zeit
            if keys_pressed[pygame.K_SPACE] == True:
                player.jump = True
                if jumpSound:
                    soundmixer.play(jump=1)
                    jumpSound = False

            # Ausführen des Sprunges nach Drücken der Leertaste
            if player.jump:
                jumpSound = player.jumpMotion()

            # Überprüfung der Kollision zwischen Spieler und Objekten
            for obs in spawner.obstacles:
                if player.collide(obs):
                    # Logik bei Berührung der Münzen
                    if obs.coin:
                        soundmixer.play(coin=1)
                        score.add(CC.SCORE_COIN * 10)
                        spawner.deleteObstacle(obs)
                    
                    # Bei Berührung der Hindernisse
                    else:
                        gameOver = True


            # Zeichnen aller Basiselemente auf den Screen
            player.draw(screen.screen)
            
            # Messen der Zeit zwischen den Frames
            lastTime = pygame.time.get_ticks()

            timeDifference = lastTime - startTime

            if (timeDifference) > 0:
                # Zeitliches Erscheinen neuer Objekte
                spawner.spawn(CC.OBSTACLE_MAX)

                # Verschnellern des Spieles = erhöhte Schwierigkeit
                if gameSpeed < CC.MAX_GAME_SPEED:
                    gameSpeed += 0.06

                # zeitliches Erhöhen des Scores
                score.add(int((obstacleIntervalTime + gameSpeed) * 10 * CC.SCORE_TIME_MUL))

                # Errechnen des neuen Intervalls basierend auf dem gameSpeed (in Millisekunden)
                startTime += obstacleIntervalTime * 1000 - gameSpeed * 1000

            # Alle Objekte updaten
            spawner.update(screen.screen)

        # bei GameOver
        else:
            # Erscheinen lassen des HighScores
            highScore.update(screen.screen, 1, score.score, gameOver)

            # Abklingzeit zur Schließung des Programms
            if keys_pressed[pygame.K_ESCAPE]:
                running = False
                # Speichern bei automatischem Abklingen des Programms
                score.save(CC.SCORE_PATH)

        # Abfangen des Schließens des Fensters, muss nicht schnell sein, deshalb im Event-System
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Speichern beim Schließen des Programms
                score.save(CC.SCORE_PATH)

        # Uhr zur Abmessung der Zeit zwischen den Frames
        clock.tick()

        # Aktualisieren des Scores
        if score.score > highScore.score:
            score.update(screen.screen, 1)

        else:
            score.update(screen.screen)

        # Updaten des Displays zur Aktualisierung von allem
        pygame.display.update()

def main():
    # Initialiseren aller Systeme zur Verwendung von Pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Schleife des Spiels
    game_loop()

    # ordentliches Beenden von Pygame als auch des Programmes an sich
    pygame.quit()
    sys.exit()

# Ausführen des Spieles durch Starten dieser Datei
if __name__ == "__main__":
    main()