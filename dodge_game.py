import random
import pygame
from engine.base_game import BaseGame


class DodgeGame(BaseGame):
    """Concrete game where the player dodges falling hazard blocks."""

    BG_COLOR = (18, 24, 38)
    GRID_COLOR = (28, 37, 56)
    PLAYER_COLOR = (56, 189, 248)
    PLAYER_ACCENT = (186, 230, 253)
    BLOCK_COLOR = (239, 68, 68)
    BLOCK_INNER = (252, 165, 165)

    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        fps: int = 60,
        screen: pygame.Surface | None = None,
    ) -> None:
        super().__init__(
            title="Dodge Blocks - Template Method Demo",
            width=width,
            height=height,
            fps=fps,
            screen=screen,
        )
        self.player_width = 52
        self.player_height = 24
        self.player_speed = 380.0
        self.player_x = 0.0
        self.move_direction = 0
        self.player_rect = pygame.Rect(0, 0, self.player_width, self.player_height)
        self.blocks: list[dict[str, float | pygame.Rect]] = []
        self.spawn_timer = 0.0
        self.spawn_interval = 0.65
        self.elapsed_time = 0.0
        self.best_score = 0

    def on_start(self) -> None:
        self.player_x = float((self.width - self.player_width) // 2)
        self.player_rect = pygame.Rect(
            int(self.player_x),
            self.height - self.player_height - 24,
            self.player_width,
            self.player_height,
        )
        self.move_direction = 0
        self.blocks.clear()
        self.spawn_timer = 0.0
        self.spawn_interval = 0.65
        self.elapsed_time = 0.0

    def on_game_over(self) -> None:
        if self.score > self.best_score:
            self.best_score = self.score

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1
        self.move_direction = direction

    def update(self, dt: float) -> None:
        self.elapsed_time += dt

        # Move player horizontally within screen bounds
        self.player_x += self.move_direction * self.player_speed * dt
        self.player_x = max(8.0, min(float(self.width - self.player_width - 8), self.player_x))
        self.player_rect.x = int(self.player_x)

        # Gradually increase difficulty over time
        difficulty = 1.0 + min(self.elapsed_time * 0.04, 2.0)
        self.spawn_interval = max(0.22, 0.65 - self.elapsed_time * 0.01)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self._spawn_block(difficulty)

        # Update falling blocks and check collisions
        remaining_blocks: list[dict[str, float | pygame.Rect]] = []
        for block in self.blocks:
            rect = block["rect"]
            speed = float(block["speed"])
            y = float(block["y"]) + speed * dt
            assert isinstance(rect, pygame.Rect)

            block["y"] = y
            rect.y = int(y)
            if rect.colliderect(self.player_rect):
                self.game_over = True
                remaining_blocks.append(block)
            elif rect.top > self.height:
                self.score += 1
            else:
                remaining_blocks.append(block)

        self.blocks = remaining_blocks

    def _spawn_block(self, difficulty: float) -> None:
        size = random.randint(28, 52)
        x = random.randint(8, self.width - size - 8)
        speed = random.uniform(190.0, 290.0) * difficulty
        self.blocks.append(
            {
                "rect": pygame.Rect(x, -size, size, size),
                "y": float(-size),
                "speed": speed,
            }
        )

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(self.BG_COLOR)

        # Subtle background grid
        for gx in range(0, self.width, 40):
            pygame.draw.line(surface, self.GRID_COLOR, (gx, 0), (gx, self.height), 1)
        for gy in range(0, self.height, 40):
            pygame.draw.line(surface, self.GRID_COLOR, (0, gy), (self.width, gy), 1)

        # Draw falling hazard blocks
        for block in self.blocks:
            rect = block["rect"]
            assert isinstance(rect, pygame.Rect)
            pygame.draw.rect(surface, self.BLOCK_COLOR, rect, border_radius=6)
            inner = rect.inflate(-10, -10)
            if inner.width > 4 and inner.height > 4:
                pygame.draw.rect(surface, self.BLOCK_INNER, inner, width=2, border_radius=4)

        # Draw player ship/block
        pygame.draw.rect(surface, self.PLAYER_COLOR, self.player_rect, border_radius=6)
        cockpit = pygame.Rect(
            self.player_rect.centerx - 10,
            self.player_rect.top + 5,
            20,
            8,
        )
        pygame.draw.rect(surface, self.PLAYER_ACCENT, cockpit, border_radius=3)

        # Best score & controls hint
        best_text = self.small_font.render(f"Best: {self.best_score}", True, (148, 163, 184))
        surface.blit(best_text, (16, 44))

        controls = self.small_font.render("Move: Left/Right or A/D", True, (100, 116, 139))
        surface.blit(controls, (self.width // 2 - controls.get_width() // 2, self.height - 24))
