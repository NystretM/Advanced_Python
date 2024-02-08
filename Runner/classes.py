import pygame, random

# Hilfsklasse für das Managen aller Sounds
class SoundMixer(object):
    def __init__(self, jumpPath, coinPath):
        self.jump = pygame.mixer.Sound(jumpPath)
        self.coin = pygame.mixer.Sound(coinPath)

    # Spiele Sound je nach Typ
    def play(self, coin=0, jump=0):
        if coin:
            pygame.mixer.Sound.play(self.coin)
        
        if jump:
            pygame.mixer.Sound.play(self.jump)

class Score(object):
    def __init__(self, size_x, size_y, font, font_size, color):
        self.score = 0
        self.size_x, self.size_y = size_x, size_y
        self.font = pygame.font.Font(font, font_size)
        self.text = self.font.render(str(self.score), True, color)
        self.color = color

    # Erhöhung des Punktestandes
    def add(self, x):
        self.score += x

    # Aktualisieren des Scores auf dem Bildschirm
    def update(self, screen, highScore = 0, score = 0, gameOver = 0):
        p = ""

        if score >= self.score:
            self.score = score
            p = "New "

        # Spezialregeln beim Highscore, zur Anzeige
        if gameOver:
            self.text = self.font.render(p + "Highscore: " + str(self.score), True, self.color)
            screen.blit(self.text, ((self.size_x // 2) - (self.size_x // 10), 0 + (1 * self.size_y) // 2))
            return 0
        
        if highScore:
            self.text = self.font.render(str(self.score) + " (Highscore)", True, self.color)
            screen.blit(self.text, ((self.size_x // 2) - (self.size_x // 50), 0 + (1 * self.size_y) // 20))
            return 0

        self.text = self.font.render(str(self.score), True, self.color)
        screen.blit(self.text, ((self.size_x // 2) - (self.size_x // 50), 0 + (1 * self.size_y) // 20))

    # Speichern des Scores, wenn dieser echt größer ist als der schon gespeicherte -> neuer Highscore
    def save(self, file):
        # Lesen sowieso Schreiben als Berechtigung
        with open(file, "r+") as f:
            l = f.readline()

            if int(l) >= self.score:
                return 0
            
            # An den Anfang der Datei springen, um die erste Zeile nach dem Lesen der ersten Zeile überschreiben zu können
            f.seek(0)

            f.write(str(self.score))


class GameObject(object):
    def __init__(self, pos_x, pos_y, size_x, size_y, color):
        self.color = color
        self.pos_x, self.pos_y = pos_x, pos_y
        self.size_x, self.size_y = size_x, size_y
        self.rect = pygame.Rect(pos_x, pos_y, size_x, size_y)
    
    # Hilfsfunktion zum Zeichnen des Objekts
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# Unterklasse von GameObject, Addition der Bewegung und Kollision
class MovableEntity(GameObject):
    def __init__(self, pos_x, pos_y, size_x, size_y, color, speed, coin):
        # Notation zur Initialisierung des Parents
        super().__init__(pos_x, pos_y, size_x, size_y, color)
        self.coin = coin
        self.speed = speed

    # einfache Funktion zur Positionsänderung = Bewegung
    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

    # einfache Hilfsfunktion zur Überprüfung von Kollisionen aller bewegbaren Objekte
    def collide(self, other):
        return self.rect.colliderect(other)
        


class Spawner(MovableEntity):
    def __init__(self, pos_x, pos_y, size, obstacleColor, coinColor, speed, coin):
        super().__init__(pos_x, pos_y, size, size, obstacleColor, speed, coin)
        self.coinColor = coinColor
        self.obstacles = list()
        self.spawnedObstacles = 0

    # Kreieren einer Instanz von Hindernis
    def spawnObstacle(self, broad = 1, high = 1, coin = 0):
        color = self.color

        obs_pos_y = self.pos_y - self.size_y if high == 2 else self.pos_y

        if coin:
            color = self.coinColor
            random_pos = random.randint(0, 10)
            obs_pos_y = self.pos_y - (self.size_y // 2) * random_pos
            
        obs = MovableEntity(self.pos_x, obs_pos_y, self.size_x * broad, self.size_y * high, color, self.speed, coin)
        self.obstacles.append(obs)
        self.spawnedObstacles += 1

    # Hilfsfunktion zur Löschung der Instanz eines Objektes
    def deleteObstacle(self, obs):
        self.obstacles.remove(obs)
        self.spawnedObstacles -= 1

    # Instanzieren von Hindernissen, wenn nicht schon genug da sind
    def spawn(self, obsMax):
        if self.spawnedObstacles <= obsMax:

                # Arbeiten mit Wahrscheinlichkeiten zur Optimierung des Spielgeschehens und Aufteilung der Hindernisse
                if random.randint(0, 4) == 0:
                    # Münze
                    self.spawnObstacle(coin=1)

                else:
                    shape = random.randint(0, 2)

                    if shape == 0:
                        self.spawnObstacle()
                    
                    elif shape == 1:
                        # breit
                        self.spawnObstacle(2, 1)

                    else:
                        # hoch
                        self.spawnObstacle(1, 2)

    # Bewegen aller aktiven Hindernisse und Zeichnen dieser, Löschen sobald aus dem Screen raus
    def update(self, screen):
        for obs in self.obstacles:
            obs.move(-1, 0)
            obs.draw(screen)

            if (obs.rect.x + obs.size_x) < 0:
                self.deleteObstacle(obs)
                continue
            

            
# Unterklasse von den bewegten Objekten, hilft bei der Zuordnung der Zustände
class Player(MovableEntity):
    def __init__(self, pos_x, pos_y, size_x, size_y, color, speed, coin, jump_force, gravity):
        super().__init__(pos_x, pos_y, size_x, size_y, color, speed, coin)
        self.jump_force = jump_force
        self.gravity = gravity

        self.jump = False
        self.vel_y = self.jump_force

    # Sprungfunktion
    def jumpMotion(self):
        self.rect.y -= self.vel_y
        self.vel_y -= self.gravity

        # Überprüfen der Höhe des Spielers, Stopp des Falles bei ursprünglicher Höhe
        if self.vel_y < -self.jump_force:
            self.jump = False
            self.vel_y = self.jump_force

            return True


# Das Uhr-Objekt zur Zeitmessung aus Pygame
class Clock(object):
    def __init__(self, tickSpeed):
        self.clock = pygame.time.Clock()
        self.tickSpeed = tickSpeed

    def tick(self):
        self.clock.tick(self.tickSpeed)

# Vereinfachung des Screens aus Pygame, daher Hilfsklasse
class Screen(object):
    def __init__(self, name, size_x, size_y, color):
        self.name = name
        self.surface = pygame.Surface((size_x, size_y))
        pygame.display.set_caption(self.name)
        self.screen = pygame.display.set_mode((size_x, size_y))
        self.color = color
        
    def fill(self):
        self.screen.fill(self.color)

    def update(self, rect):
        self.screen.blit(rect)

def reset_game():
    # Setze alle Spielvariablen zurück, um das Spiel neu zu starten
    global gameOver
    gameOver = False
    global jumpSound
    jumpSound = True
    global gameSpeed, score
    gameSpeed, score = CC.START_GAME_SPEED, 0
    global player
    player.rect.x = CC.PLAYER_OFFSET_X
    player.rect.y = int((3*CC.SCREEN_SIZE_Y)//4) - int(CC.PLAYER_SIZE * 1.25)
    global spawner
    spawner.reset()
    global highScore
    highScore.update(screen.screen, 1, score, gameOver)

def show_restart_button(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Restart", True, (255, 255, 255))
    button_rect = text.get_rect()
    button_rect.center = (CC.SCREEN_SIZE_X // 2, CC.SCREEN_SIZE_Y // 2)

    pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Hintergrund des Buttons
    screen.blit(text, button_rect.topleft)
    return button_rect
