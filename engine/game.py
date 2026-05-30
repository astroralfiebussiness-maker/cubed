"""
Main game loop and logic
"""

import time
import sys
from engine.world import World
from engine.player import Player
from terrain.generator import TerrainGenerator
from utils.constants import TICK_RATE, AUTO_SAVE_INTERVAL, BLOCK_GRASS, BLOCK_STONE
from utils.save_load import save_world, load_world


class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize game"""
        print("[INIT] Starting Cubed...")
        
        # Try to load saved game
        world_data, player_pos, player_dir = load_world()
        
        if world_data:
            self.world = World(world_data)
            self.player = Player()
            self.player.set_position(*player_pos)
            self.player.set_direction(*player_dir)
            print("[INIT] Loaded saved world")
        else:
            # Generate new world
            print("[INIT] Generating new world...")
            generator = TerrainGenerator()
            world_data = generator.generate()
            self.world = World(world_data)
            self.player = Player()
            print("[INIT] World generated")
        
        self.running = True
        self.tick_count = 0
        self.last_time = time.time()
    
    def run(self):
        """Main game loop"""
        print("[GAME] Game started. Type 'help' for commands.")
        print(f"[PLAYER] Position: {self.player.get_position()}")
        print()
        
        while self.running:
            self.tick()
            self.render()
            self.handle_input()
            
            # Auto-save
            if self.tick_count % AUTO_SAVE_INTERVAL == 0 and self.tick_count > 0:
                self.save_game()
            
            self.tick_count += 1
            
            # Control frame rate
            time.sleep(1.0 / TICK_RATE)
    
    def tick(self):
        """Game tick update"""
        pass  # Physics, collisions, etc. would go here
    
    def render(self):
        """Render game state"""
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Draw world around player
        self._draw_world()
        
        # Draw HUD
        self._draw_hud()
    
    def _draw_world(self):
        """Draw world view around player"""
        x, y, z = self.player.get_position()
        
        print("=" * 60)
        print("CUBED - World View")
        print("=" * 60)
        
        # Draw a simple 2D cross-section around the player
        view_range = 5
        
        for view_y in range(int(y) + view_range, int(y) - view_range - 1, -1):
            row = ""
            for view_z in range(int(z) - view_range, int(z) + view_range + 1):
                if view_y == int(self.player.y) and view_z == int(self.player.z):
                    row += "@"  # Player
                else:
                    block = self.world.get_block(int(x), view_y, view_z)
                    if block == 0:
                        row += "."
                    elif block == 1:
                        row += "#"  # Stone
                    elif block == 2:
                        row += "="  # Dirt
                    elif block == 3:
                        row += "^"  # Grass
                    elif block == 4:
                        row += "~"  # Sand
                    elif block == 5:
                        row += "~"  # Water
                    else:
                        row += "?"
            print(f"Y:{view_y:2d} {row}")
        
        print("-" * 60)
    
    def _draw_hud(self):
        """Draw heads-up display"""
        x, y, z = self.player.get_position()
        yaw, pitch = self.player.get_direction()
        
        print(f"Position: X:{x:6.1f} Y:{y:6.1f} Z:{z:6.1f} | Yaw:{yaw:6.1f}° Pitch:{pitch:6.1f}°")
        print(f"Block: {self.world.get_block_name(int(x), int(y), int(z))}")
        print()
        print("Commands: move <dir> | look <yaw> <pitch> | place | break | save | load | help | quit")
    
    def handle_input(self):
        """Handle user input"""
        try:
            command = input("> ").strip().lower()
        except EOFError:
            self.running = False
            return
        
        if not command:
            return
        
        parts = command.split()
        cmd = parts[0]
        
        if cmd == "move":
            if len(parts) > 1:
                direction = parts[1]
                distance = float(parts[2]) if len(parts) > 2 else 1
                self.player.move(direction, distance)
                print(f"Moved {direction}")
        
        elif cmd == "look":
            if len(parts) > 2:
                yaw = float(parts[1])
                pitch = float(parts[2])
                self.player.set_direction(yaw, pitch)
                print(f"Looking at Yaw:{yaw} Pitch:{pitch}")
        
        elif cmd == "place":
            self._place_block()
        
        elif cmd == "break":
            self._break_block()
        
        elif cmd == "save":
            self.save_game()
        
        elif cmd == "load":
            self._load_game()
        
        elif cmd == "help":
            self._print_help()
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            print("Goodbye!")
        
        else:
            print(f"Unknown command: {cmd}")
    
    def _place_block(self):
        """Place block in front of player"""
        pos = self.player.get_place_block_position(self.world)
        if pos:
            self.world.set_block(*pos, BLOCK_GRASS)
            print(f"[PLACE] Block placed at {pos}")
        else:
            print("[PLACE] No valid position to place block")
    
    def _break_block(self):
        """Break block in front of player"""
        target = self.player.get_forward_block(self.world)
        if target:
            self.world.set_block(*target, 0)
            print(f"[BREAK] Block destroyed at {target}")
        else:
            print("[BREAK] No block in sight")
    
    def save_game(self):
        """Save current game state"""
        save_world(
            self.world.export_blocks(),
            self.player.get_position(),
            self.player.get_direction()
        )
    
    def _load_game(self):
        """Load saved game state"""
        world_data, player_pos, player_dir = load_world()
        if world_data:
            self.world = World(world_data)
            self.player = Player()
            self.player.set_position(*player_pos)
            self.player.set_direction(*player_dir)
            print("[LOAD] Game loaded successfully")
        else:
            print("[LOAD] No saved game found")
    
    def _print_help(self):
        """Print help message"""
        print("""
CUBED Commands:
  move <direction> [distance]  - Move in direction (forward/backward/left/right/up/down)
  look <yaw> <pitch>          - Set camera direction (degrees)
  place                        - Place block in front of player
  break                        - Break block in front of player
  save                         - Save game state
  load                         - Load saved game state
  help                         - Show this help message
  quit                         - Exit game

Example: move forward 2
""")
