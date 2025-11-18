import pygame

class Shark:
    def __init__(self, screen_width, screen_height):
        """
        Shark that moves side to side at the bottom of the screem
        """
        self.image = pygame.image.load('images/shark.png').convert_alpha()
        # if i need to change the size later
        self.image = pygame.transform.scale(self.image, (180, 300))

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Putting the shark at the bottom
        self.x = self.screen_width // 2
        self.y = self.screen_height - 150

        # movement
        self.speed = 4
        self.direction = 1

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """
        moving it left and right
        """
        self.x += self.speed * self.direction
        left_limit = 90
        right_limit = self.screen_width - 90

        if self.x < left_limit:
            self.x = left_limit  # stop at wall

        if self.x > right_limit:
            self.x = right_limit  #

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """Draw the shark onto the screen."""
        screen.blit(self.image, self.rect)





