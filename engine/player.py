"""
Player logic and management
"""

import math
from utils.constants import WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH, PLAYER_REACH, BLOCK_EMPTY


class Player:
    """Manages player state and movement"""
    
    def __init__(self, x=WORLD_WIDTH//2, y=WORLD_HEIGHT-2, z=WORLD_DEPTH//2):
        """Initialize player
        
        Args:
            x, y, z: Starting position
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
        # Camera direction (yaw, pitch in degrees)
        self.yaw = 0.0
        self.pitch = 0.0
    
    def move(self, direction, distance=1):
        """Move player in cardinal direction
        
        Args:
            direction: 'forward', 'backward', 'left', 'right', 'up', 'down'
            distance: How far to move
        """
        yaw_rad = math.radians(self.yaw)
        
        if direction == 'forward':
            self.x += math.sin(yaw_rad) * distance
            self.z += math.cos(yaw_rad) * distance
        elif direction == 'backward':
            self.x -= math.sin(yaw_rad) * distance
            self.z -= math.cos(yaw_rad) * distance
        elif direction == 'left':
            self.x -= math.cos(yaw_rad) * distance
            self.z += math.sin(yaw_rad) * distance
        elif direction == 'right':
            self.x += math.cos(yaw_rad) * distance
            self.z -= math.sin(yaw_rad) * distance
        elif direction == 'up':
            self.y += distance
        elif direction == 'down':
            self.y -= distance
        
        # Clamp position to world bounds
        self._clamp_position()
    
    def look(self, yaw_delta, pitch_delta):
        """Change camera direction
        
        Args:
            yaw_delta: Change in yaw (degrees)
            pitch_delta: Change in pitch (degrees)
        """
        self.yaw = (self.yaw + yaw_delta) % 360
        self.pitch = max(-90, min(90, self.pitch + pitch_delta))
    
    def get_position(self):
        """Get player position as tuple"""
        return (self.x, self.y, self.z)
    
    def get_direction(self):
        """Get camera direction as tuple (yaw, pitch)"""
        return (self.yaw, self.pitch)
    
    def set_position(self, x, y, z):
        """Set player position"""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self._clamp_position()
    
    def set_direction(self, yaw, pitch):
        """Set camera direction"""
        self.yaw = float(yaw)
        self.pitch = float(pitch)
    
    def _clamp_position(self):
        """Clamp player position to world bounds"""
        self.x = max(0, min(WORLD_WIDTH - 0.5, self.x))
        self.y = max(0, min(WORLD_HEIGHT - 0.5, self.y))
        self.z = max(0, min(WORLD_DEPTH - 0.5, self.z))
    
    def get_forward_block(self, world):
        """Get block player is looking at
        
        Returns:
            (x, y, z) of block or None if none in reach
        """
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        # Ray direction
        dx = math.sin(yaw_rad) * math.cos(pitch_rad)
        dy = -math.sin(pitch_rad)
        dz = math.cos(yaw_rad) * math.cos(pitch_rad)
        
        # Cast ray
        for i in range(1, PLAYER_REACH + 1):
            x = int(self.x + dx * i)
            y = int(self.y + dy * i)
            z = int(self.z + dz * i)
            
            block = world.get_block(x, y, z)
            if block is not None and block != BLOCK_EMPTY:
                return (x, y, z)
        
        return None
    
    def get_place_block_position(self, world):
        """Get position where player can place a block
        
        Returns:
            (x, y, z) for placing or None
        """
        target = self.get_forward_block(world)
        if target is None:
            return None
        
        # Place block next to target in direction player is looking
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        dx = math.sin(yaw_rad) * math.cos(pitch_rad)
        dy = -math.sin(pitch_rad)
        dz = math.cos(yaw_rad) * math.cos(pitch_rad)
        
        x = int(target[0] + dx * 0.5)
        y = int(target[1] + dy * 0.5)
        z = int(target[2] + dz * 0.5)
        
        return (x, y, z) if world.get_block(x, y, z) is not None else None
