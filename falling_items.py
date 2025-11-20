import pygame
import random

class FallingItem:
    def __init__(self, screen_width, screen_height, image_path, speed):
        """
        general class for anything that falls, can be bad or good item
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        # CHANGE WIDTH AND HEIGHT LATER
        self.image = pygame.transform.scale(self.image, (128, 72))

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed

        self.x = 0
        self.y = 0

        # collisions
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # where it starts falling from
        self.reset_position()

    def reset_position(self):
        """
        respawning items randomly from the top of the screen
        """
        self.x = random.randint(10, self.screen_width - 10)
        self.y = random.randint(-300,-50)

        self.rect.center = (self.x, self.y)

    def update(self):
        # actually move the item downward
        self.y += self.speed

        # reset if item goes past the bottom
        if self.y > self.screen_height + 50:
            self.reset_position()

        # update the rectangle
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


