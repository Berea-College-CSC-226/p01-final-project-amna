import pygame
from pygame import transform

from shark import Shark
from falling_items import FallingItem

class Game:
    def __init__(self):
        """
        making the game window and setting up the game screen,
        background, shark and falling items.
        """
        pygame.init()

        # WINDOW SIZE
        self.width = 1000
        self.height = 700

        # WINDOW CREATION
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Feeding Frenzy')

        self.clock = pygame.time.Clock()

        # LOGO
        self.logo = pygame.image.load("images/title.png").convert_alpha()
        self.logo = transform.scale(self.logo, (700, 700))

        # BACKGROUND
        self.background = pygame.image.load("images/water_still.png").convert_alpha()

        # FONT
        self.font = pygame.font.Font("fonts/pixel.ttf", 40)

        # STATE OF GAME
        self.running = True
        self.game_started = False

        # SHARK
        self.shark = Shark(self.width, self.height)

        # FALLING ITEMS
        self.items = [
            FallingItem(self.width,self.height, "images/good_1.png", speed = 4),
            FallingItem(self.width,self.height, "images/good_2.png", speed = 4),
            FallingItem(self.width,self.height, "images/good_4.png", speed = 4),
            FallingItem(self.width,self.height, "images/good_5.png", speed = 4),
            FallingItem(self.width,self.height, "images/good_6.png", speed = 4),
            FallingItem(self.width,self.height, "images/bad_item.png", speed = 4),
        ]

    def start_page(self):
        """
        Shows the logo and waits for the user to actually click on
        the screen before actually starting the game
        """

        text = self.font.render("Click anywhere to begin!", True, (255,255,255))

        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_started = True

            # DRAWING THE BACKGROUND FROM PICTURE
            self.screen.blit(self.background, (0, 0))

            # draw logo
            logo_rect = self.logo.get_rect(center=(self.width // 2, 220))
            self.screen.blit(self.logo, logo_rect)

            # draw text
            text_rect = text.get_rect(center=(self.width // 2, 430))
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start_page()


