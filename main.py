import pygame
import sys
import random

# Khởi tạo pygame
pygame.init()

# Màn hình
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Khoảng cách giữa các cột
PIPE_SPACING = 200  # Tăng khoảng cách giữa các cột
# Tốc độ cuộn ban đầu
SCROLL_SPEED = 3
# Trọng lực
GRAVITY = 0.5
# Sức nhảy
JUMP_POWER = -8
# Tỉ lệ sinh cột mới sẽ được ngẫu nhiên
MIN_PIPE_FREQUENCY = 1250  # Thời gian min giữa các cột (ms)
MAX_PIPE_FREQUENCY = 2500  # Thời gian max giữa các cột (ms)

# Font chữ
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Đồng hồ
clock = pygame.time.Clock()
FPS = 60

# Biến lưu trữ số lần chết toàn cục
total_deaths = 0

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15  # Đổi kích thước cho chim hình tròn
        self.velocity = 0
        self.alive = True
    
    def draw(self):
        # Vẽ chim hình tròn màu đỏ
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        if self.y < self.radius:  # Điều chỉnh giới hạn trên cho hình tròn
            self.y = self.radius
            self.velocity = 0
        
        if self.y + self.radius > HEIGHT:  # Điều chỉnh giới hạn dưới cho hình tròn
            self.y = HEIGHT - self.radius
            self.alive = False
    
    def jump(self):
        self.velocity = JUMP_POWER
    
    def get_rect(self):
        # Trả về hình chữ nhật bao quanh hình tròn để kiểm tra va chạm
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 50
        # Tạo khoảng trống ngẫu nhiên kích thước từ 130 đến 180
        self.gap_size = random.randint(130, 180)
        # Vị trí khoảng trống
        self.gap_y = random.randint(100, HEIGHT - 100 - self.gap_size)
        self.passed = False
    
    def draw(self):
        # Vẽ cột dưới
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + self.gap_size, self.width, HEIGHT - (self.gap_y + self.gap_size)))
        # Vẽ cột trên
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
    
    def update(self, speed):
        self.x -= speed
    
    def is_offscreen(self):
        return self.x + self.width < 0
    
    def get_rects(self):
        # Trả về hình chữ nhật của cột trên và cột dưới
        return (
            pygame.Rect(self.x, 0, self.width, self.gap_y),
            pygame.Rect(self.x, self.gap_y + self.gap_size, self.width, HEIGHT - (self.gap_y + self.gap_size))
        )

class Game:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.bird = Bird(100, HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.game_active = True
        self.last_pipe = 0
        self.game_time = 0  # Lưu thời gian chơi
        # Tạo thời gian ngẫu nhiên cho cột đầu tiên
        self.next_pipe_time = random.randint(MIN_PIPE_FREQUENCY, MAX_PIPE_FREQUENCY)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.game_active:
                    self.bird.jump()
                else:
                    self.reset_game()
    
    def update(self):
        if self.game_active:
            # Cập nhật thời gian chỉ khi game đang hoạt động
            self.game_time = (pygame.time.get_ticks() - self.start_time) // 1000
            
            self.bird.update()
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > self.next_pipe_time:
                self.pipes.append(Pipe(WIDTH))
                self.last_pipe = current_time
                # Tạo thời gian ngẫu nhiên cho cột tiếp theo
                self.next_pipe_time = random.randint(MIN_PIPE_FREQUENCY, MAX_PIPE_FREQUENCY)
            
            # Tốc độ tăng theo điểm (tăng nhanh hơn)
            speed = SCROLL_SPEED + self.score * 0.5  
            
            for pipe in self.pipes:
                pipe.update(speed)
                
                if pipe.x + pipe.width < self.bird.x and not pipe.passed:
                    pipe.passed = True
                    self.score += 1
                
                # Kiểm tra va chạm
                if self.bird.get_rect().colliderect(pipe.get_rects()[0]) or self.bird.get_rect().colliderect(pipe.get_rects()[1]):
                    self.bird.alive = False
            
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]
            
            if not self.bird.alive:
                global total_deaths
                total_deaths += 1  # Tăng số lần chết toàn cục
                self.game_active = False
    
    def draw(self):
        # Màn hình trắng thay vì xanh dương
        screen.fill(WHITE)
        
        for pipe in self.pipes:
            pipe.draw()
        self.bird.draw()
        
        # Hiển thị thông tin với màu đen
        score_text = small_font.render(f"Score: {self.score}", True, BLACK)
        deaths_text = small_font.render(f"Deaths: {total_deaths}", True, BLACK)
        time_text = small_font.render(f"Time: {self.game_time}s", True, BLACK)
        fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(deaths_text, (WIDTH - 120, 10))
        screen.blit(time_text, (WIDTH // 2 - 40, 10))
        screen.blit(fps_text, (WIDTH - 100, HEIGHT - 30))
        
        if not self.game_active:
            game_over_text = font.render("Game Over", True, BLACK)
            restart_text = small_font.render("Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

# Khởi tạo trò chơi
game = Game()
while True:
    game.handle_events()
    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(FPS)

# 23/03/2025
