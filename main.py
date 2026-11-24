import sys
import pygame

from engine.catch_game import CatchGame
from engine.dodge_game import DodgeGame

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
MENU_FPS = 60


def draw_menu(
    surface: pygame.Surface,
    title_font: pygame.font.Font,
    option_font: pygame.font.Font,
    small_font: pygame.font.Font,
) -> tuple[pygame.Rect, pygame.Rect]:
    """Render the launcher menu and return clickable card rects."""
    surface.fill((15, 23, 42))

    title = title_font.render("Pygame Mini-Game Engine", True, (248, 250, 252))
    subtitle = small_font.render(
        "Template Method Design Pattern Demo  |  Shared BaseGame Loop",
        True,
        (148, 163, 184),
    )

    surface.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 56))
    surface.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 108))

    card_1 = pygame.Rect(90, 165, 460, 88)
    card_2 = pygame.Rect(90, 275, 460, 88)

    # Option 1: DodgeGame
    pygame.draw.rect(surface, (30, 41, 59), card_1, border_radius=12)
    pygame.draw.rect(surface, (56, 189, 248), card_1, width=2, border_radius=12)
    text_1 = option_font.render("[1]  Play DodgeGame", True, (56, 189, 248))
    desc_1 = small_font.render(
        "Dodge falling red blocks using Left/Right or A/D.",
        True,
        (203, 213, 225),
    )
    surface.blit(text_1, (card_1.x + 24, card_1.y + 16))
    surface.blit(desc_1, (card_1.x + 24, card_1.y + 50))

    # Option 2: CatchGame
    pygame.draw.rect(surface, (30, 41, 59), card_2, border_radius=12)
    pygame.draw.rect(surface, (52, 211, 153), card_2, width=2, border_radius=12)
    text_2 = option_font.render("[2]  Play CatchGame", True, (52, 211, 153))
    desc_2 = small_font.render(
        "Catch gold coins & purple gems before losing 3 lives.",
        True,
        (203, 213, 225),
    )
    surface.blit(text_2, (card_2.x + 24, card_2.y + 16))
    surface.blit(desc_2, (card_2.x + 24, card_2.y + 50))

    footer = small_font.render(
        "Press [1] or [2] to launch  |  Press [ESC] or [Q] to quit",
        True,
        (148, 163, 184),
    )
    surface.blit(footer, (WINDOW_WIDTH // 2 - footer.get_width() // 2, 415))

    return card_1, card_2


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Mini-Game Launcher")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 36, bold=True)
    option_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 18)

    running = True
    while running:
        card_1, card_2 = draw_menu(screen, title_font, option_font, small_font)
        pygame.display.flip()
        clock.tick(MENU_FPS)

        selected_game = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    selected_game = DodgeGame(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, screen=screen)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    selected_game = CatchGame(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, screen=screen)
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if card_1.collidepoint(event.pos):
                    selected_game = DodgeGame(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, screen=screen)
                elif card_2.collidepoint(event.pos):
                    selected_game = CatchGame(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, screen=screen)

        if selected_game is not None:
            result = selected_game.run()
            pygame.display.set_caption("Pygame Mini-Game Launcher")
            if result == "quit":
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
