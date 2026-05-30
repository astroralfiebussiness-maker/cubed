"""
Game constants and configuration
"""

# World dimensions
WORLD_WIDTH = 32
WORLD_HEIGHT = 16
WORLD_DEPTH = 32

# Block types
BLOCK_EMPTY = 0
BLOCK_STONE = 1
BLOCK_DIRT = 2
BLOCK_GRASS = 3
BLOCK_SAND = 4
BLOCK_WATER = 5

BLOCK_NAMES = {
    0: "Empty",
    1: "Stone",
    2: "Dirt",
    3: "Grass",
    4: "Sand",
    5: "Water",
}

# Player settings
PLAYER_SPEED = 1  # blocks per tick
PLAYER_REACH = 5  # blocks

# Game settings
TICK_RATE = 10  # ticks per second
AUTO_SAVE_INTERVAL = 100  # ticks between auto-saves
