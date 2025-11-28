import pygame
from pygame import transform, display
import random

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
        self.height = 750
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
        # LIVES
        self.lives = 3
        self.life_pic = pygame.image.load("images/heart.png").convert_alpha()
        self.life_pic = transform.scale(self.life_pic, (80, 80))
        # BAD ITEM
        # BUCKET (putting it here because it is the only one with a different size)
        self.bucket_image = pygame.image.load("images/bad_item.png").convert_alpha()
        self.bucket_image = pygame.transform.scale(self.bucket_image, (100,100))
        # SPAWN TIMER
        self.spawn_timer = 0
        self.spawn_difference = 40
        # LIST WITH FALLING ITEMS
        self.items = []
        self.fish_images = [
            "images/good_1.png",
            "images/good_2.png",
            "images/good_4.png",
            "images/good_5.png",
            "images/good_6.png"
        ]

        self.score = 0

        # LIVES
        self.lives = 3

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
            logo_rect = self.logo.get_rect(center=(self.width // 2, 270))
            self.screen.blit(self.logo, logo_rect)

            # draw text
            text_rect = text.get_rect(center=(self.width // 2, 470))
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def game_loop(self):
        """
        Main loop in which the game will update shark and falling items
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # SPAWNING
            self.spawn_timer += 1

            if self.spawn_timer >= self.spawn_difference:
                self.spawn_timer = 0

                # more fish than buckets
                if random.random() < 0.80:
                    img = random.choice(self.fish_images)
                    speed = 3.9
                    new_item = FallingItem(self.width, self.height, img, speed)
                else:
                    speed = 4
                    new_item = FallingItem(self.width, self.height, "images/bad_item.png", speed)
                    new_item.image = self.bucket_image
                    new_item.rect = new_item.image.get_rect(center=(new_item.x, new_item.y))

                # LIMITING HOW MANY THINGS ARE ON THE SCREENS
                if len(self.items) < 4:
                    self.items.append(new_item)

            # UPDATE OBJECTS
            self.shark.update()

            for item in self.items[:]:
                item.update()

                #  shark mouth hitbox
                mouth_width = 122
                mouth_height = 190

                offset_x = 35

                mouth_rect = pygame.Rect(
                    self.shark.rect.centerx + offset_x- mouth_width // 2,
                    self.shark.rect.bottom - mouth_height,
                    mouth_width,
                    mouth_height
                )

                if item.rect.colliderect(mouth_rect):
                    if item.image != self.bucket_image:
                        self.score += 20
                    else:
                        self.lives -= 1

                    self.items.remove(item)

                    if self.lives == 0:
                        self.running = False

                    continue

            # DRAWING EVERYTHING
            self.screen.blit(self.background, (0, 0))

            self.shark.draw(self.screen)

            for item in self.items:
                item.draw(self.screen)

            score_text = self.font.render(str(self.score), True, (255, 255, 255))
            text_rect = score_text.get_rect(topright=(self.width - 20, 20))
            self.screen.blit(score_text, text_rect)

            for i in range(self.lives):
                self.screen.blit(self.life_pic, (20 + (i * 45), 20))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start_page()
    game.game_loop()
