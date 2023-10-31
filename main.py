import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 7
PADDLE_SPEED = 10

# Adjustable FPS
desired_fps = 60

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.velocity = 0

    def move(self):
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))

class MainMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 36)
        self.title = self.title_font.render("Pong Game", True, WHITE)
        self.play_option = self.option_font.render("Press SPACE to Play", True, WHITE)
        self.quit_option = self.option_font.render("Press Q to Quit", True, WHITE)

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.title, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(self.play_option, (WIDTH // 2 - 160, HEIGHT // 2 + 20))
        screen.blit(self.quit_option, (WIDTH // 2 - 120, HEIGHT // 2 + 60))

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.menu = MainMenu()
        self.game_started = False

        self.player_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.opponent_paddle = Paddle(WIDTH - 50 - 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        self.player_score = 0
        self.opponent_score = 0
        self.font = pygame.font.Font(None, 36)

        self.colors_inverted = False

        # Load and play background music
        pygame.mixer.music.load("background_music.mp3")  # Replace "background_music.mp3" with your music file
        pygame.mixer.music.set_volume(0.3)  # Adjust the volume as needed
        pygame.mixer.music.play(-1)  # Play the music in a loop

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if not self.game_started:
            if keys[pygame.K_SPACE]:
                self.game_started = True
            elif keys[pygame.K_q]:
                pygame.quit()
                exit()

        if self.game_started:
            # Player paddle control
            if keys[pygame.K_w]:
                self.player_paddle.velocity = -self.player_paddle.speed
            elif keys[pygame.K_s]:
                self.player_paddle.velocity = self.player_paddle.speed
            else:
                self.player_paddle.velocity = 0

            # Opponent paddle control
            if keys[pygame.K_UP]:
                self.opponent_paddle.velocity = -self.opponent_paddle.speed
            elif keys[pygame.K_DOWN]:
                self.opponent_paddle.velocity = self.opponent_paddle.speed
            else:
                self.opponent_paddle.velocity = 0

    def check_ball_collision(self):
        if self.ball.rect.colliderect(self.player_paddle.rect) and self.ball.speed_x < 0:
            self.ball.speed_x = -self.ball.speed_x
            self.colors_inverted = not self.colors_inverted

        if self.ball.rect.colliderect(self.opponent_paddle.rect) and self.ball.speed_x > 0:
            self.ball.speed_x = -self.ball.speed_x
            self.colors_inverted = not self.colors_inverted

    def update(self):
        self.ball.rect.x += self.ball.speed_x
        self.ball.rect.y += self.ball.speed_y

        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y = -self.ball.speed_y

        self.check_ball_collision()

        if self.ball.rect.left <= 0:
            self.opponent_score += 1
            self.reset_ball()

        if self.ball.rect.right >= WIDTH:
            self.player_score += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball = Ball()
        self.colors_inverted = False

    def draw(self):
        if self.colors_inverted:
            self.screen.fill(BLACK)
            text_color = WHITE
        else:
            self.screen.fill(WHITE)
            text_color = BLACK

        pygame.draw.rect(self.screen, WHITE if self.colors_inverted else BLACK, self.player_paddle.rect)
        pygame.draw.rect(self.screen, WHITE if self.colors_inverted else BLACK, self.opponent_paddle.rect)
        pygame.draw.ellipse(self.screen, WHITE if self.colors_inverted else BLACK, self.ball.rect)
        pygame.draw.aaline(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        player_text = self.font.render(f"Player: {self.player_score}", True, text_color)
        opponent_text = self.font.render(f"Opponent: {self.opponent_score}", True, text_color)
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(opponent_text, (WIDTH - 250, 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(BLACK)

            if not self.game_started:
                self.menu.draw(self.screen)
            else:
                self.player_paddle.move()
                self.opponent_paddle.move()
                self.update()
                self.draw()

            pygame.display.flip()
            self.clock.tick(desired_fps)

if __name__ == "__main__":
    pong_game = PongGame()
    pong_game.run()
