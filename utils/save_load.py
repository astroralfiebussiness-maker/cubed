"""
Save and load game world
"""

import json
import os
from utils.constants import WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH


SAVE_DIR = "saves"
SAVE_FILE = os.path.join(SAVE_DIR, "world.json")
PLAYER_FILE = os.path.join(SAVE_DIR, "player.json")


def ensure_save_dir():
    """Ensure save directory exists"""
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_world(world_data, player_pos, player_dir):
    """
    Save world and player data to files
    
    Args:
        world_data: 3D list of blocks
        player_pos: (x, y, z) tuple
        player_dir: (yaw, pitch) tuple
    """
    ensure_save_dir()
    
    # Save world
    world_dict = {
        "width": WORLD_WIDTH,
        "height": WORLD_HEIGHT,
        "depth": WORLD_DEPTH,
        "blocks": world_data
    }
    
    with open(SAVE_FILE, 'w') as f:
        json.dump(world_dict, f)
    
    # Save player
    player_dict = {
        "position": list(player_pos),
        "direction": list(player_dir)
    }
    
    with open(PLAYER_FILE, 'w') as f:
        json.dump(player_dict, f)
    
    print(f"[SAVE] Game saved to {SAVE_DIR}/")


def load_world():
    """
    Load world and player data from files
    
    Returns:
        (world_data, player_pos, player_dir) or (None, None, None) if not found
    """
    if not os.path.exists(SAVE_FILE) or not os.path.exists(PLAYER_FILE):
        return None, None, None
    
    # Load world
    with open(SAVE_FILE, 'r') as f:
        world_dict = json.load(f)
    
    # Load player
    with open(PLAYER_FILE, 'r') as f:
        player_dict = json.load(f)
    
    world_data = world_dict["blocks"]
    player_pos = tuple(player_dict["position"])
    player_dir = tuple(player_dict["direction"])
    
    print(f"[LOAD] Game loaded from {SAVE_DIR}/")
    return world_data, player_pos, player_dir
