import pytmx  # Module nécessaire pour gérer Tiled
import pygame
import sys

pygame.init()
fps = 20
fpsClock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fond = pygame.Surface((WIDTH, HEIGHT))


# Importer les images du joueur
player_img_front = pygame.image.load("down.png")
player_img_back = pygame.image.load("up.png")
player_img_right = pygame.image.load("right.png")
player_img_left = pygame.image.load("left.png")

# Ouverture du fichier tiled et identification des layers
tm = pytmx.load_pygame('tiled_test2.tmx', pixelalpha=True)  # Ouvrir la map
layer_obstacles = tm.get_layer_by_name("obstacle")  # Obtenir le layer "obstacle" défini dans Tiled
layer_herbe = tm.get_layer_by_name("herbe")  # Obtenir le layer "obstacle" défini dans Tiled

# Faire apparaître les images
for x, y, image in layer_herbe.tiles():
    fond.blit(image, (x*16, y*16))

for x, y, image in layer_obstacles.tiles():
    fond.blit(image, (x*16, y*16))

# Groupe des sprites de la couche
player_list = pygame.sprite.GroupSingle()
obstacles = pygame.sprite.Group()
herbe = pygame.sprite.Group()


# Création d'une subclass tuile
class Tuile(pygame.sprite.Sprite):  # Étant donné que Tuile est une subclass de Sprite, Tuile est considéré comme un Sprite
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x*16, y*16, 16, 16)  # Définition d'un Rectangle, zone de l'obstacle
        self.image = image


# Création d'une subclass Joueur
class Player(pygame.sprite.Sprite):
    moveSpeed = 6
    change_in_x = 0
    change_in_y = 0
    direction = "None"

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_img_front
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Création d'un instance Joueur
player = Player(150, 130)
# Ajout de cette instance à une liste
player.add(player_list)

# Ajout des sprites individuels au groupe
for x, y, image in layer_herbe.tiles():  # On regarde toutes les tiles qui ont le layer "herbe"
    herbe.add(Tuile(x, y, image))  # On appelle la classe Tuile et on rajoute l'instance crée à une liste de sprites

for x, y, image in layer_obstacles.tiles():
    obstacles.add(Tuile(x, y, image))

# Prendre en compte le fait qu'une touche reste appuyée
pygame.key.set_repeat(10, 10)

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Update la direction choisie dans l'instance de Player()
        if event.type == pygame.KEYDOWN:  # Si le joueur appuie sur une touche
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:  # Si cette touche est la flèche gauche
                player.direction = "Left"  # Changer la direction de Player
            if event.key == pygame.K_RIGHT:
                player.direction = "Right"
            if event.key == pygame.K_UP:
                player.direction = "Up"
            if event.key == pygame.K_DOWN:
                player.direction = "Down"

        if event.type == pygame.KEYUP:  # Si le joueur relache une touche
            if event.key == pygame.K_LEFT:
                player.direction = "None"  # Mettre la direction sur none
            if event.key == pygame.K_RIGHT:
                player.direction = "None"
            if event.key == pygame.K_UP:
                player.direction = "None"
            if event.key == pygame.K_DOWN:
                player.direction = "None"

        # Mouvement du joueur

        if player.direction == "Right":
            # Le changement en x et y est égal à l'attribut moveSpeed
            player.change_in_x = player.moveSpeed
            # Le joueur bouge en rajoutant les valeurs de déplacement en x et y à la position x ou y du rectangle.
            player.rect.x += player.change_in_x
            # L'image du joueur est ensuite correctement choisie
            player.image = player_img_right
        if player.direction == "Left":
            player.change_in_x = player.moveSpeed
            player.rect.x += -player.change_in_x
            player.image = player_img_left
        if player.direction == "Up":
            player.change_in_y = -player.moveSpeed
            player.rect.y += player.change_in_y
            player.image = player_img_back
        if player.direction == "Down":
            player.change_in_y = player.moveSpeed
            player.rect.y += player.change_in_y
            player.image = player_img_front

        # Détection de collisions
        for tile in obstacles:  # On regarde tous les sprites dans obstacles
            if player.rect.colliderect(tile.rect):  # Si le rectangle du joueur touche le rectangle d'un obstacle
                if player.direction == "Right":  # Si la direction du joueur va à droite
                    player.rect.x -= player.change_in_x  # Le rectangle ne bouge pas en x
                if player.direction == "Left":
                    player.rect.x -= -player.change_in_x
                if player.direction == "Up":
                    player.rect.y -= player.change_in_y # Le rectangle ne bouge pas en y
                if player.direction == "Down":
                    player.rect.y -= player.change_in_y

    # Dessiner tout dans l'ordre
    herbe.draw(screen)  # Couche la plus basse = herbe
    obstacles.draw(screen)  # Couche la moins basse = obstacles
    player_list.draw(screen)  # Joueurs au plus haut

    pygame.display.update()
    pygame.display.flip()
    fpsClock.tick(fps)
