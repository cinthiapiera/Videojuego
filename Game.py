import pygame
import pygame_menu

# Inicialización de Pygame
pygame.init()
# Inicialización de fuentes de Pygame
pygame.font.init()
# Creación de la ventana del juego
pantalla = pygame.display.set_mode((600,400))

class Game:
    def __init__(self, width, height, difficulty):
        # Inicialización de las variables del juego
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("fondo.png")
        self.difficulty = difficulty

        #self.start_time = pygame.time.get_ticks()  # Inicializar el tiempo al inicio del juego
        self.score = 0  # Reiniciar el puntaje al iniciar un nuevo juego
        self.aliens = []  # Reiniciar la lista de aliens
        self.rockets = []  # Reiniciar la lista de proyectiles
        self.lost = False
        self.win = False
        done = False

        # Creación del héroe y generador de aliens
        hero = Hero(self, width/2, height-20)
        generator = Generator(self, difficulty)

        #pygame.mixer.music.load("song_galaxy.wav")
        #pygame.mixer.music.play(-1)

        while not done:
            if len(self.aliens) == 0:
                self.win = True
                self.displaytext("¡Ganaste el juego!") # Mostrar mensaje de victoria
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < width-20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost: #and len(self.rockets)<4
                    self.rockets.append(Rocket(self,hero.x,hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.blit(self.fondo,(0,0))
            self.draw_score()   # Llama al método para dibujar la puntuación

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height):
                    self.lost = True
                    self.displaytext("¡Perdiste el juego!") # Mostrar mensaje de derrota

            for rocket in self.rockets: # iteracion de lista de proyectiles
                if not self.win:
                    rocket.draw()
                if rocket.y <= 0:
                    self.rockets.remove(rocket)

            if not self.lost:
                hero.draw()

    def draw_score(self):
        # Dibuja el puntaje en la pantalla
        font = pygame.font.SysFont("Arial", 24)
        score_surface = font.render("Puntuación: " + str(self.score), False, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))  # Posición de la puntuación en la parte superior izquierda
    def displaytext(self,text):
        # Muestra un mensaje en la pantalla
        font = pygame.font.SysFont("Arial",50)
        textSurface = font.render(text,False, (255,255,255))
        self.screen.blit(textSurface,(125,150))
class Alien:
    def __init__(self, game, x,y, velocity):
        # Inicialización de las características de un alien
        self.x = x
        self.game = game
        self.y = y
        self.size = 30
        self.image = pygame.image.load("alien.png")
        self.velocity = velocity

    def draw(self):
        # Dibuja el alien en la pantalla
        self.game.screen.blit(self.image,(self.x,self.y))
        self.y += self.velocity
    def checkCollision(self, game):
        # Verifica si un alien ha sido golpeado por un proyectil
        for rocket in game.rockets:
            if(rocket.x < self.x + self.size and rocket.x > self.x - self.size and rocket.y < self.y + self.size and rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)
                game.score += 10  # Incrementar la puntuación cuando se destruye un alien
class Hero:
    def __init__(self, game, x, y):
        # Inicialización del héroe
        self.x = x
        self.y = y
        self.game = game
        self.image = pygame.image.load("nave.png")
    def draw(self):
        self.game.screen.blit(self.image,(self.x,self.y))

class Generator:
    def __init__(self, game, velocity):
        # Genera aliens en el juego
        margin = 30
        width = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y, velocity))

class Rocket:
    def __init__(self, game, x,y ):
        # Inicialización de proyectiles
        self.game = game
        self.x = x
        self.y = y
    def draw(self):
        # Dibuja proyectiles
        pygame.draw.rect(self.game.screen, (254, 52, 110), pygame.Rect(self.x,self.y, 2,4))
        self.y -= 2

def start_easy(): # Inicia un nuevo juego en dificultad fácil
    Game(600,400,0.07)

def start_medium(): # Inicia un nuevo juego en dificultad media
    Game(600,400,0.2)

def start_hard(): # Inicia un nuevo juego en dificil
    Game(600, 400,0.5)

#Menú principal del juego
menu = pygame_menu.Menu(height = 400,
                        theme = pygame_menu.themes.THEME_BLUE,
                        title = "Galactic Defender",
                        width = 600)

menu.add.button("Easy", start_easy)
menu.add.button("Medium",start_medium)
menu.add.button("Hard",start_hard)
menu.add.button("Quit",pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(pantalla)