import pygame

class Shark:
    def __init__(self, screen_width, screen_height):
        """
        Shark that moves side to side at the bottom of the screem
        """
        self.image = pygame.image.load('images/shark.png').convert_alpha()
        # if i need to change the size later
        self.image = pygame.transform.scale(self.image, (512, 539))

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Putting the shark at the bottom
        self.x = self.screen_width // 2
        self.y = self.screen_height - 150

        # movement
        self.speed = 4

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """
        moving the shark with arrow keys
        """
        keys = pygame.key.get_pressed()

        # move left
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        # move right
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # keep inside boundaries
        if self.x < 90:
            self.x = 90
        if self.x > self.screen_width - 90:
            self.x = self.screen_width - 90

        # update rectangle
        self.rect.center = (self.x, self.y)


    def draw(self, screen):
        """Draw the shark onto the screen."""
        screen.blit(self.image, self.rect)





