# One More Day

A 2D top-down survival game written in Python with Pygame. Survive each day by defeating every zombie, then do it again with more of them.

## Features

- **Day-based progression:** clearing all enemies starts the next day, and each day spawns more zombies.
- **Combat:** melee (dagger) and ranged (pistol with limited ammo, unlocked on day 3) attacks, enemy knockback and damage feedback.
- **Enemy AI:** zombies have three behaviours chosen by distance to the player: roam (random wandering), chase (once the player is within notice range) and attack (within attack range, with a cooldown).
- **Inventory and items:** a five-slot inventory with consumables (health, energy, speed and attack effects) and random loot drops from defeated enemies.
- **Difficulty settings:** Easy, Normal and Hard scale enemy health, speed and damage.
- **Map and camera:** a Tiled (`.tmx`) map loaded with `pytmx`, collision objects, and a camera that follows the player.
- **Menu:** main menu, guide and settings screens (difficulty and fullscreen).

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move |
| Space | Use the selected item (attack or consume) |
| 1–5 | Select inventory slot |

## Running

```
pip install -r requirements.txt
cd code
python main.py
```

The game expects `graphics/`, `audio/` and `map/` folders next to the `code/` folder. These asset folders are **not included** in this repository because they contain third-party graphics and audio.

## Code structure

| File | Purpose |
|---|---|
| `main.py` | Game loop, menu states and difficulty |
| `level.py` | Map building, enemy spawning, days, game over, camera |
| `player.py` | Player input, combat, inventory and consumables |
| `enemy.py` | Enemy stats, AI behaviour, animation and damage |
| `entity.py`, `collider.py` | Shared movement, animation and collision logic |
| `projectile.py` | Pistol bullets |
| `ui.py`, `menu.py` | HUD and menu screens |
| `settings.py` | Constants and enemy data |

Made as my A-Level Computer Science project.
