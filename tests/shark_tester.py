class SharkTester:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = screen_width // 2
        self.y = screen_height - 150
        self.speed = 5
        self.direction = 0  # -1 left, 1 right

    def update(self):
        self.x += self.direction * self.speed

        # boundaries
        if self.x < 90:
            self.x = 90
        if self.x > self.screen_width - 90:
            self.x = self.screen_width - 90
