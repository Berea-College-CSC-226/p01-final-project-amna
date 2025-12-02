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
        self.life_pic = transform.scale(self.life_pic, (90, 90))

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

        #  START SPEED
        self.start_speed = 4

        # LANES FOR FALLING
        self.lanes = [
            self.width * 0.15,
            self.width * 0.35,
            self.width * 0.55,
            self.width * 0.75
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
            logo_rect = self.logo.get_rect(center=(self.width // 2, 270))
            self.screen.blit(self.logo, logo_rect)

            # draw text
            text_rect = text.get_rect(center=(self.width // 2, 470))
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)


    def game_over(self):
        """
        just the game over screen and the final score
        """
        game_over_text = self.font.render("Game Over!", True, (255,255,255))
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        click_text = self.font.render("Click to play again", True, (255, 255, 255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return # to restart

                # DRAW background
                self.screen.blit(self.background, (0, 0))

            # DRAW text
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.width // 2, 250)))
            self.screen.blit(score_text, score_text.get_rect(center=(self.width // 2, 350)))
            self.screen.blit(click_text, click_text.get_rect(center=(self.width // 2, 450)))

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

            # INCREASING SPEED EVERY 200 POINTS
            self.start_speed = 4 + (self.score//200) - 0.5

            # SPAWNING
            self.spawn_timer += 1

            if self.spawn_timer >= self.spawn_difference:
                self.spawn_timer = 0

                lane_x = random.choice(self.lanes)

                # TRYING TO AVOID STACKING
                lane_blocked = False
                for item in self.items:
                    # if this item is in the same lane (x position matches)
                    if abs(item.rect.centerx - lane_x) < 10:
                        # and it is too close to top → block lane
                        if item.y < 450:
                            lane_blocked = True
                            break

                if lane_blocked:
                    continue

                if random.random() < 0.90:
                    img = random.choice(self.fish_images)
                    speed = self.start_speed
                    new_item = FallingItem(self.width, self.height, img, speed)
                    new_item.kind = "fish"
                else:
                    speed = self.start_speed
                    new_item = FallingItem(self.width, self.height, "images/bad_item.png", speed)
                    new_item.image = self.bucket_image
                    new_item.rect = new_item.image.get_rect(center=(new_item.x, new_item.y))
                    new_item.kind = "bucket"

                # APPLY lane X position
                new_item.x = lane_x
                new_item.rect.centerx = lane_x

                if len(self.items) < len(self.lanes):  # max = 4 items always
                    self.items.append(new_item)

            # UPDATE OBJECTS
            self.shark.update()

            for item in self.items[:]:
                item.update()

                # REMOVE ITEM IF IT FALLS BELOW SCREEN
                if item.rect.top > self.height:
                    self.items.remove(item)
                    continue

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
                    if item.kind == "fish":
                        self.score += 20
                    elif item.kind == "bucket":
                        self.lives -= 1

                    self.items.remove(item)

                    if self.lives == 0:
                        self.game_over()
                        return

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
   while True:
       game = Game()
       game.start_page()
       game.game_loop()
