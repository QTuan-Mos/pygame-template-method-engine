# Pygame Template Method Mini-Game Engine

A runnable Python Pygame project demonstrating the **Template Method** behavioral design pattern. Two distinct playable mini-games (`DodgeGame` and `CatchGame`) share a single reusable game-loop engine defined in `BaseGame`.

## Template Method Pattern Architecture

The **Template Method** pattern defines the skeleton of an algorithm in a base class (`BaseGame.run()`) and lets subclasses override specific steps without changing the algorithm's overall structure.

```
BaseGame (ABC)                  <-- AbstractClass
 ├── run()                      <-- Template Method (invariant game loop)
 ├── handle_input(events)       <-- Abstract Step (required)
 ├── update(dt)                 <-- Abstract Step (required)
 ├── render(surface)            <-- Abstract Step (required)
 ├── on_start()                 <-- Hook Method (optional)
 └── on_game_over()             <-- Hook Method (optional)
        ▲
        │ inherits
   ┌────┴────────────────┐
   │                     │
DodgeGame            CatchGame   <-- ConcreteClasses
```

### Class Roles

1. **`BaseGame` (`engine/base_game.py`) — AbstractClass**
   - **`run()` (Template Method):** Controls the invariant lifecycle:
     1. Calls `on_start()` when starting or restarting a session.
     2. Drives the fixed-FPS clock (`pygame.time.Clock`) and computes delta time (`dt`).
     3. Polls Pygame events and handles global quit, menu return (`ESC` / `M`), and game-over restart (`R` / `SPACE`).
     4. Invokes `handle_input(events)` and `update(dt)` while the session is active, triggering `on_game_over()` once upon losing.
     5. Calls `render(surface)`, overlays the shared HUD (`Score` and menu hint), displays the shared Game Over screen when `self.game_over` is `True`, and flips the display.
   - **Abstract Methods:** `handle_input()`, `update()`, and `render()` must be implemented by every concrete mini-game.
   - **Hook Methods:** `on_start()` and `on_game_over()` provide default empty implementations that subclasses may optionally override.

2. **`DodgeGame` (`engine/dodge_game.py`) — ConcreteClass**
   - Implements `handle_input()`, `update()`, and `render()` for dodging falling red blocks.
   - Overrides `on_start()` to reset the player ship and obstacles, and `on_game_over()` to track the session's best score.

3. **`CatchGame` (`engine/catch_game.py`) — ConcreteClass**
   - Implements `handle_input()`, `update()`, and `render()` for catching falling gold circles (`+10`) and purple bonus diamonds (`+25`) with a paddle.
   - Overrides the `on_start()` hook to reset `lives` (`3`), `combo`, and `banner_timer`, and immediately spawn the first falling item.

4. **Launcher (`main.py`) — Client**
   - Presents a Pygame menu where pressing `1` launches `DodgeGame` and pressing `2` launches `CatchGame`, invoking the shared `game.run()` template method on either subclass polymorphically.

## Project Structure

```text
.
├── requirements.txt
├── README.md
├── main.py
└── engine/
    ├── __init__.py
    ├── base_game.py
    ├── dodge_game.py
    └── catch_game.py
```

## How to Run

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the menu:
   ```bash
   python main.py
   ```

## Controls

- **Launcher Menu:** `1` for DodgeGame, `2` for CatchGame, `ESC` or `Q` to quit (mouse click on cards also supported).
- **In-Game Movement:** `Left` / `Right` arrow keys or `A` / `D`.
- **Return to Menu:** `ESC` (or `M` on Game Over).
- **Restart After Game Over:** `R`, `SPACE`, or `ENTER`.
