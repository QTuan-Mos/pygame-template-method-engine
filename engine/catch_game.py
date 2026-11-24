import random
import pygame
from engine.base_game import BaseGame


class CatchGame(BaseGame):
    """Concrete game where the player catches falling items with a basket."""

    BG_COLOR = (19, 28, 33)
    FLOOR_COLOR = (30, 45, 54)
    PADDLE_COLOR = (52, 211, 153)
    PADDLE_RIM = (167, 243, 208)
    ITEM_COLOR = (250, 204, 21)
    BONUS_COLOR = (168, 85, 247)
    LIFE_COLOR = (244, 63, 94)

    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        fps: int = 60,
        screen: pygame.Surface | None = None,
    ) -> None:
        super().__init__(
            title="Catch Items - Template Method Demo",
            width=width,
            height=height,
            fps=fps,
            screen=screen,
        )
        self.paddle_width = 96
        self.paddle_height = 20
        self.paddle_speed = 430.0
        self.paddle_x = 0.0
        self.move_direction = 0
        self.paddle_rect = pygame.Rect(0, 0, self.paddle_width, self.paddle_height)

        self.items: list[dict[str, float | int | str]] = []
        self.spawn_timer = 0.0
        self.spawn_interval = 0.85
        self.lives = 3
        self.combo = 0
        self.banner_timer = 0.0

    def on_start(self) -> None:
        """Override the BaseGame hook to reset lives, combo, and spawn an opening item."""
        self.paddle_x = float((self.width - self.paddle_width) // 2)
        self.paddle_rect = pygame.Rect(
            int(self.paddle_x),
            self.height - self.paddle_height - 26,
            self.paddle_width,
            self.paddle_height,
        )
        self.move_direction = 0
        self.items.clear()
        self.spawn_timer = 0.0
        self.spawn_interval = 0.85
        self.lives = 3
        self.combo = 0
        self.banner_timer = 2.0
        self._spawn_item()

    def handle_input(self, events: list[pygame.event.Event]) -> None:
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1
        self.move_direction = direction

    def update(self, dt: float) -> None:
        if self.banner_timer > 0.0:
            self.banner_timer = max(0.0, self.banner_timer - dt)

        # Move paddle horizontally within screen bounds
        self.paddle_x += self.move_direction * self.paddle_speed * dt
        self.paddle_x = max(8.0, min(float(self.width - self.paddle_width - 8), self.paddle_x))
        self.paddle_rect.x = int(self.paddle_x)

        # Spawn items progressively faster as score climbs
        self.spawn_interval = max(0.35, 0.85 - self.score * 0.002)
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self._spawn_item()

        remaining_items: list[dict[str, float | int | str]] = []
        for item in self.items:
            x = float(item["x"])
            y = float(item["y"]) + float(item["speed"]) * dt
            radius = int(item["radius"])
            item["y"] = y

            item_rect = pygame.Rect(int(x - radius), int(y - radius), radius * 2, radius * 2)
            if item_rect.colliderect(self.paddle_rect):
                self.combo += 1
                bonus_multiplier = 1 + (self.combo // 5)
                self.score += int(item["points"]) * bonus_multiplier
            elif y - radius > self.height:
                self.combo = 0
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
            else:
                remaining_items.append(item)

        self.items = remaining_items

    def _spawn_item(self) -> None:
        is_bonus = random.random() < 0.2
        radius = 12 if is_bonus else 14
        x = float(random.randint(radius + 16, self.width - radius - 16))
        speed = random.uniform(210.0, 290.0) if is_bonus else random.uniform(150.0, 230.0)
        self.items.append(
            {
                "x": x,
                "y": float(-radius),
                "radius": radius,
                "speed": speed,
                "points": 25 if is_bonus else 10,
                "kind": "bonus" if is_bonus else "standard",
            }
        )

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(self.BG_COLOR)

        # Floor strip
        pygame.draw.rect(
            surface,
            self.FLOOR_COLOR,
            pygame.Rect(0, self.height - 20, self.width, 20),
        )

        # Draw falling items
        for item in self.items:
            center = (int(item["x"]), int(item["y"]))
            radius = int(item["radius"])
            if item["kind"] == "bonus":
                # Diamond shape for bonus items
                points = [
                    (center[0], center[1] - radius),
                    (center[0] + radius, center[1]),
                    (center[0], center[1] + radius),
                    (center[0] - radius, center[1]),
                ]
                pygame.draw.polygon(surface, self.BONUS_COLOR, points)
                pygame.draw.polygon(surface, (233, 213, 255), points, width=2)
            else:
                pygame.draw.circle(surface, self.ITEM_COLOR, center, radius)
                pygame.draw.circle(surface, (254, 240, 138), center, radius - 5, width=2)

        # Draw player catcher paddle
        pygame.draw.rect(surface, self.PADDLE_COLOR, self.paddle_rect, border_radius=8)
        rim = pygame.Rect(
            self.paddle_rect.left + 6,
            self.paddle_rect.top + 3,
            self.paddle_rect.width - 12,
            5,
        )
        pygame.draw.rect(surface, self.PADDLE_RIM, rim, border_radius=3)

        # Lives indicator
        lives_label = self.small_font.render("Lives:", True, (203, 213, 225))
        surface.blit(lives_label, (16, 46))
        for idx in range(3):
            color = self.LIFE_COLOR if idx < self.lives else (51, 65, 85)
            pygame.draw.circle(surface, color, (82 + idx * 24, 56), 8)

        # Combo indicator
        if self.combo >= 2:
            combo_text = self.small_font.render(
                f"Combo x{1 + self.combo // 5} ({self.combo} streak)",
                True,
                (167, 243, 208),
            )
            surface.blit(combo_text, (16, 74))

        # Hook startup banner
        if self.banner_timer > 0.0:
            banner = self.font.render("Catch the falling items!", True, (254, 240, 138))
            surface.blit(banner, (self.width // 2 - banner.get_width() // 2, 95))

        controls = self.small_font.render("Move: Left/Right or A/D", True, (100, 116, 139))
        surface.blit(controls, (self.width // 2 - controls.get_width() // 2, self.height - 18))
