import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
PLATFORM_HEIGHT = 20
JUMP_VELOCITY = -15
GRAVITY = 0.8

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.color = color
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.controls = controls
        self.score = 0
        self.checkpoint = (x, y)
        self.deaths = 0

    def move(self, dx):
        self.velocity_x = dx * 5

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False

    def update(self, platforms, hazards):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Screen boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                if self.velocity_y > 0:  # Falling
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.y = platform.y + platform.height
                    self.velocity_y = 0

        # Hazard collision
        for hazard in hazards:
            if self.check_collision(hazard):
                self.die()
                break

        # Check if fallen off screen
        if self.y > SCREEN_HEIGHT:
            self.die()

    def check_collision(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

    def die(self):
        self.deaths += 1
        self.x, self.y = self.checkpoint
        self.velocity_x = 0
        self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Platform:
    def __init__(self, x, y, width, height, color=WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2-Player Obstacle Course")
        self.clock = pygame.time.Clock()
        
        # Create players
        self.player1 = Player(50, SCREEN_HEIGHT - 100, BLUE, {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w
        })
        
        self.player2 = Player(50, SCREEN_HEIGHT - 100, RED, {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_UP
        })
        
        # Create level
        self.platforms = []
        self.hazards = []
        self.create_level()

    def create_level(self):
        # Starting platform
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 200, PLATFORM_HEIGHT))
        
        # Create platforms
        x = 200
        y = SCREEN_HEIGHT - 40
        while x < SCREEN_WIDTH - 100:
            # Random platform
            width = random.randint(60, 150)
            gap = random.randint(60, 120)
            y_change = random.randint(-50, 50)
            y = max(100, min(SCREEN_HEIGHT - 100, y + y_change))
            
            self.platforms.append(Platform(x + gap, y, width, PLATFORM_HEIGHT))
            
            # Add hazard
            if random.random() < 0.3:
                hazard_width = 30
                self.hazards.append(Platform(x + gap + width//2 - hazard_width//2, 
                                          y - 20, hazard_width, 20, RED))
            
            x = x + gap + width

        # Finish platform
        self.platforms.append(Platform(SCREEN_WIDTH - 100, 100, 100, PLATFORM_HEIGHT, GREEN))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Player 1 controls
        if keys[self.player1.controls['left']]:
            self.player1.move(-1)
        elif keys[self.player1.controls['right']]:
            self.player1.move(1)
        else:
            self.player1.velocity_x = 0
        if keys[self.player1.controls['jump']]:
            self.player1.jump()
            
        # Player 2 controls
        if keys[self.player2.controls['left']]:
            self.player2.move(-1)
        elif keys[self.player2.controls['right']]:
            self.player2.move(1)
        else:
            self.player2.velocity_x = 0
        if keys[self.player2.controls['jump']]:
            self.player2.jump()

    def update(self):
        self.player1.update(self.platforms, self.hazards)
        self.player2.update(self.platforms, self.hazards)

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw hazards
        for hazard in self.hazards:
            hazard.draw(self.screen)
        
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        # Draw scores
        font = pygame.font.Font(None, 36)
        p1_text = font.render(f"P1 Deaths: {self.player1.deaths}", True, BLUE)
        p2_text = font.render(f"P2 Deaths: {self.player2.deaths}", True, RED)
        self.screen.blit(p1_text, (10, 10))
        self.screen.blit(p2_text, (10, 50))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game
                        self.__init__()

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
