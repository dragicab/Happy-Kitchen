import pygame
import sys
from ingredients import INGREDIENTS, RECIPES
from reactions import get_reaction

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Весела кујна")

font = pygame.font.SysFont("Comic Sans MS", 30)
clock = pygame.time.Clock()

selected = []




def draw_text(text, x, y, color=(0, 0, 0)):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))


def main():
    running = True
    result = ""

    while running:
        screen.fill((255, 229, 204))


        for i, ing in enumerate(INGREDIENTS):
            draw_text(ing, 50, 50 + i * 40)

        draw_text(f"Избрано: {', '.join(selected)}", 400, 50)
        draw_text(f"Резултат: {result}", 400, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, ing in enumerate(INGREDIENTS):
                    if 50 <= x <= 250 and 50 + i * 40 <= y <= 80 + i * 40:
                        if len(selected) < 2:
                            selected.append(ing)
                        if len(selected) == 2:
                            result = get_reaction(selected[0], selected[1])
                            selected.clear()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
