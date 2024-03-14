import pygame
import sys
import random
import os

pygame.init()

FPS = 60
GRAVITY = 1
BIRD_JUMP = -15
PIPE_WIDTH = 100
PIPE_HEIGHT = 200
PIPE_GAP = 400
BIRD_SIZE = 100
BONUS_SCORE_THRESHOLD = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("Flappy Absolut")

image_path = os.path.join(os.path.dirname(__file__), 'Imagens')

bird_img = pygame.image.load(os.path.join(image_path, 'image122.png'))
pipe_img = pygame.image.load(os.path.join(image_path, 'image2.jpg'))
background_img = pygame.image.load(os.path.join(image_path, 'image3.jpg'))

bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

def draw_bird(x, y):
    bird_rect = bird_img.get_rect(center=(x, y))
    screen.blit(bird_img, bird_rect)
    return bird_rect

def draw_pipe(pipe_x, pipe_height):
    screen.blit(pipe_img, (pipe_x, 0))
    screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe_x, pipe_height + PIPE_GAP))

def draw_play_button():
    play_button_size = 50
    play_button_color = (0, 255, 0)
    pygame.draw.polygon(screen, play_button_color, [(WIDTH // 2, HEIGHT // 2 - play_button_size),
                                                    (WIDTH // 2 + play_button_size, HEIGHT // 2),
                                                    (WIDTH // 2, HEIGHT // 2 + play_button_size)])

def show_bonus_message():
    font = pygame.font.Font(None, 36)
    text = font.render("Bonus: Franchetti nao pagou", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def is_click_on_play_button(pos):
    play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
    return play_button_rect.collidepoint(pos)

def reset_game():
    return WIDTH // 2, HEIGHT // 2, 0, WIDTH, random.randint(100, HEIGHT - PIPE_GAP - 100), 0

def main():
    clock = pygame.time.Clock()

    bird_x, bird_y, bird_velocity, pipe_x, pipe_height, score = reset_game()

    game_active = False
    last_pipe_move_time = pygame.time.get_ticks()
    bonus_display_time = 0
    current_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    bird_x, bird_y, bird_velocity, pipe_x, pipe_height, score = reset_game()
                    game_active = True
                elif event.key == pygame.K_SPACE and game_active:
                    bird_velocity = BIRD_JUMP
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                if is_click_on_play_button(pygame.mouse.get_pos()):
                    bird_x, bird_y, bird_velocity, pipe_x, pipe_height, score = reset_game()
                    game_active = True

        if game_active:
            bird_y += bird_velocity
            bird_velocity += GRAVITY

            current_time = pygame.time.get_ticks()
            time_passed = current_time - last_pipe_move_time

            if time_passed >= 10:
                pipe_x -= 5
                last_pipe_move_time = current_time

            bird_rect = draw_bird(bird_x, bird_y)
            pipe_rect_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
            pipe_rect_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)

            if bird_x > pipe_x + PIPE_WIDTH:
                score += 1
                if score % BONUS_SCORE_THRESHOLD == 0 and current_time - bonus_display_time > 2000:
                    bonus_display_time = current_time

            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                game_active = False

            if bird_y > HEIGHT or bird_y < 0:
                game_active = False

            if pipe_x < -PIPE_WIDTH:
                pipe_x = WIDTH
                pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)

        screen.blit(background_img, (0, 0))

        if not game_active:
            draw_play_button()

        draw_pipe(pipe_x, pipe_height)
        draw_bird(bird_x, bird_y)

        if current_time - bonus_display_time <= 2000:
            show_bonus_message()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
