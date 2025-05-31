import pygame
import sys
import math
from ingredients import INGREDIENTS, RECIPES
from reactions import get_reaction

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Весела кујна")
font = pygame.font.SysFont("Comic Sans MS", 24)
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

selected = []
result = ""
score = 0
reaction_scores = []
last_selected = []


neutral_customer_img = pygame.image.load("assets/neutral_customer.png")
neutral_customer_img = pygame.transform.scale(neutral_customer_img, (150, 150))

ingredient_images = {}
ingredient_positions = {}

chef_img = pygame.image.load("assets/chef.png").convert_alpha()
chef_img = pygame.transform.scale(chef_img, (200, 200))

for name, path in INGREDIENTS.items():
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (70, 70))
    ingredient_images[name] = image


def draw_text(text, x, y, color=(0, 0, 0), center=False):
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(render, rect)


def start_screen():
    button_rect = pygame.Rect(WIDTH // 2 - 75, 400, 150, 50)
    running = True

    while running:
        screen.fill((255, 229, 204))
        screen.blit(chef_img, (WIDTH // 2 - 100, 150))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 300, 50, 600, 80), border_radius=20)
        draw_text("Дали си спремен да направиш некого среќен денес?", WIDTH // 2, 90, center=True)
        pygame.draw.rect(screen, (255, 153, 51), button_rect, border_radius=10)
        draw_text("Почни", button_rect.centerx, button_rect.centery - 10, color=(255, 255, 255), center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)


def get_customer_reaction_image(text):
    if "Освежувачка бомба" in text or "Галактички десерт" in text:
        return pygame.image.load("assets/smile.png")
    elif "Чуден хит" in text or "Неутрално лице" in text or "Што е ова" in text:
        return pygame.image.load("assets/neutral1.png")
    else:
        return pygame.image.load("assets/sad.png")


def show_popup(text):
    popup_duration = 2000
    start_time = pygame.time.get_ticks()

    background = screen.copy()
    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    dark_overlay.set_alpha(180)
    dark_overlay.fill((0, 0, 0))

    popup = pygame.Surface((500, 250))
    popup.fill((255, 255, 255))
    pygame.draw.rect(popup, (255, 153, 204), popup.get_rect(), 5)

    font_big = pygame.font.SysFont("Comic Sans MS", 26)
    text_render = font_big.render(text, True, (0, 0, 0))

    reaction_img = get_customer_reaction_image(text)
    reaction_img = pygame.transform.scale(reaction_img, (80, 80))
    popup.blit(reaction_img, (30, 30))
    popup.blit(text_render, (130, 60))

    for i, ing in enumerate(selected):
        img = pygame.transform.scale(ingredient_images[ing], (50, 50))
        popup.blit(img, (130 + i * 100, 150))
        draw_text(ing, 130 + i * 100, 205, center=True)

    while pygame.time.get_ticks() - start_time < popup_duration:
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))
        screen.blit(popup, (WIDTH // 2 - 250, HEIGHT // 2 - 125))
        pygame.display.flip()
        clock.tick(30)


def handle_click(ingredient):
    global selected, result, score, last_selected

    if ingredient not in selected:
        selected.append(ingredient)

    if len(selected) == 2:
        result = get_reaction(selected[0], selected[1]) or "🤔 Што е ова?"
        show_popup(result)

        if "Освежувачка бомба" in result or "Галактички десерт" in result:
            score += 3
            reaction_scores.append(2)
        elif "Чуден хит" in result or "Неутрално лице" in result or "Што е ова" in result:
            score += 1
            reaction_scores.append(0)
        else:
            score -= 2
            reaction_scores.append(-1)

        last_selected = selected.copy()
        selected.clear()


def end_screen():
    screen.fill((255, 229, 204))

    if reaction_scores:
        max_score = len(reaction_scores) * 2
        total = sum(reaction_scores)
        percentage = max(0, int((total / max_score) * 100))
    else:
        percentage = 0

    if percentage >= 70:
        message = "Браво!"
        color = (0, 153, 0)
    elif percentage >= 40:
        message = "Солидно"
        color = (255, 165, 0)
    else:
        message = "Денес не е твојот ден"
        color = (204, 0, 0)

    center = (WIDTH // 2, HEIGHT // 2)
    radius = 100
    thickness = 15

    current_percent = 0
    while current_percent <= percentage:
        screen.fill((255, 229, 204))

        pygame.draw.circle(screen, (200, 200, 200), center, radius, thickness)

        end_angle = (current_percent / 100) * 360
        for angle in range(int(end_angle)):
            rad = math.radians(angle - 90)
            x = int(center[0] + math.cos(rad) * radius)
            y = int(center[1] + math.sin(rad) * radius)
            pygame.draw.circle(screen, color, (x, y), thickness // 2)

        draw_text(f"{current_percent}%", center[0], center[1] - 15, center=True)
        draw_text(message, center[0], center[1] + 40, color=color, center=True)

        pygame.display.flip()
        current_percent += 1
        clock.tick(60)

    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


def main_game():
    global score
    running = True

    while running:
        screen.fill((255, 229, 204))

        right_panel_x = WIDTH - 300
        screen.blit(neutral_customer_img, (right_panel_x, 10))
        draw_text(f"Поени: {score}", right_panel_x + 160, 60)

        y_start = 30
        for i, (name, image) in enumerate(ingredient_images.items()):
            y_pos = y_start + i * 80
            screen.blit(image, (50, y_pos))
            draw_text(name, 140, y_pos + 25)
            ingredient_positions[name] = pygame.Rect(50, y_pos, 80, 80)

        draw_text("Избрани состојки:", right_panel_x, 180)
        for i in range(2):
            if i < len(last_selected):
                ing = last_selected[i]
                y_pos = 240 + i * 90
                screen.blit(ingredient_images[ing], (WIDTH - 150, y_pos))

        finish_button = pygame.Rect(WIDTH - 160, HEIGHT - 60, 130, 40)
        pygame.draw.rect(screen, (255, 102, 102), finish_button, border_radius=10)
        draw_text("ЗАВРШИ", finish_button.centerx, finish_button.centery - 10, color=(255, 255, 255), center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for name, rect in ingredient_positions.items():
                    if rect.collidepoint(x, y):
                        handle_click(name)
                if finish_button.collidepoint(x, y):
                    end_screen()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    start_screen()
    main_game()
