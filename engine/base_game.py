from abc import ABC, abstractmethod
import pygame


class BaseGame(ABC):
    """Abstract base class defining the Template Method game engine.

    The ``run()`` method acts as the Template Method: it fixes the skeleton of
    the game loop (lifecycle hooks, timing/FPS clock, event polling, HUD score
    rendering, and the game-over overlay) while deferring game-specific input,
    state updates, and rendering to subclasses.
    """

    def __init__(
        self,
        title: str = "Pygame Template Game",
        width: int = 640,
        height: int = 480,
        fps: int = 60,
        screen: pygame.Surface | None = None,
    ) -> None:
        if not pygame.get_init():
            pygame.init()

        self.title = title
        self.width = width
        self.height = height
        self.fps = fps

        self.screen = screen or pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.large_font = pygame.font.SysFont("arial", 44, bold=True)

        self.score: int = 0
        self.running: bool = False
        self.game_over: bool = False

    def run(self) -> str:
        """Template Method executing the invariant game loop skeleton.

        Returns:
            ``"quit"`` if the user closed the application window, or
            ``"menu"`` if the user chose to return to the launcher menu.
        """
        pygame.display.set_caption(self.title)
        self._reset_session()

        exit_action = "menu"

        while self.running:
            dt = min(self.clock.tick(self.fps) / 1000.0, 0.05)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    exit_action = "quit"
                    break
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                            self._reset_session()
                        elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                            self.running = False
                            exit_action = "menu"
                            break
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        exit_action = "menu"
                        break

            if not self.running:
                break

            if not self.game_over:
                was_game_over = self.game_over
                self.handle_input(events)
                self.update(dt)
                if not was_game_over and self.game_over:
                    self.on_game_over()

            self.render(self.screen)
            self._draw_hud()

            if self.game_over:
                self._draw_game_over()

            pygame.display.flip()

        return exit_action

    def _reset_session(self) -> None:
        self.score = 0
        self.running = True
        self.game_over = False
        self.on_start()

    def _draw_hud(self) -> None:
        score_surface = self.font.render(f"Score: {self.score}", True, (240, 244, 248))
        self.screen.blit(score_surface, (16, 14))

        hint_surface = self.small_font.render("[ESC] Menu", True, (160, 174, 192))
        self.screen.blit(hint_surface, (self.width - hint_surface.get_width() - 16, 16))

    def _draw_game_over(self) -> None:
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((10, 14, 23, 185))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.large_font.render("GAME OVER", True, (248, 113, 113))
        score_surface = self.font.render(f"Final Score: {self.score}", True, (248, 250, 252))
        prompt_surface = self.small_font.render(
            "Press [R] or [SPACE] to Retry  |  [M] or [ESC] for Menu",
            True,
            (203, 213, 225),
        )

        center_x = self.width // 2
        center_y = self.height // 2

        self.screen.blit(
            title_surface,
            (center_x - title_surface.get_width() // 2, center_y - 70),
        )
        self.screen.blit(
            score_surface,
            (center_x - score_surface.get_width() // 2, center_y - 10),
        )
        self.screen.blit(
            prompt_surface,
            (center_x - prompt_surface.get_width() // 2, center_y + 42),
        )

    @abstractmethod
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        """Process player input for the current frame."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance game state by ``dt`` seconds."""

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Draw the game world onto ``surface``."""

    def on_start(self) -> None:
        """Optional hook called when a game session starts or restarts."""

    def on_game_over(self) -> None:
        """Optional hook called once when the game transitions to game over."""
