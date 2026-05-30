# Cubed

A Minecraft-like voxel game built in Python.

## Features

- Grid-based terrain generation
- Player movement and controls
- Block placement and destruction
- Save/load game world
- Console-based gameplay

## Installation

```bash
pip install numpy
```

## Running the Game

```bash
python main.py
```

## Controls

- **W/A/S/D** - Move forward/left/backward/right
- **Q/E** - Move up/down
- **P** - Place block
- **B** - Break block
- **SPACE** - Save game
- **L** - Load game
- **ESC** - Quit game

## Project Structure

```
cubed/
├── main.py              # Game entry point
├── engine/
│   ├── game.py         # Main game loop
│   ├── world.py        # World management
│   └── player.py       # Player logic
├── terrain/
│   └── generator.py    # Terrain generation
└── utils/
    ├── constants.py    # Game constants
    └── save_load.py    # Save/load system
```
