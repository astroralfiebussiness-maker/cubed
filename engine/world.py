"""
World management system
"""

from utils.constants import (
    WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH,
    BLOCK_EMPTY, BLOCK_STONE, BLOCK_DIRT, BLOCK_GRASS, BLOCK_SAND, BLOCK_WATER
)


class World:
    """Manages the game world and blocks"""
    
    def __init__(self, terrain_data=None):
        """Initialize world
        
        Args:
            terrain_data: Optional pre-generated terrain data
        """
        if terrain_data:
            self.blocks = terrain_data
        else:
            self.blocks = [[[BLOCK_EMPTY for _ in range(WORLD_DEPTH)]
                           for _ in range(WORLD_HEIGHT)]
                          for _ in range(WORLD_WIDTH)]
    
    def get_block(self, x, y, z):
        """Get block at position
        
        Args:
            x, y, z: Coordinates
            
        Returns:
            Block type or None if out of bounds
        """
        if not self._is_in_bounds(x, y, z):
            return None
        return self.blocks[int(x)][int(y)][int(z)]
    
    def set_block(self, x, y, z, block_type):
        """Set block at position
        
        Args:
            x, y, z: Coordinates
            block_type: Block type to set
            
        Returns:
            True if successful, False if out of bounds
        """
        if not self._is_in_bounds(x, y, z):
            return False
        self.blocks[int(x)][int(y)][int(z)] = block_type
        return True
    
    def _is_in_bounds(self, x, y, z):
        """Check if position is within world bounds"""
        return (0 <= x < WORLD_WIDTH and
                0 <= y < WORLD_HEIGHT and
                0 <= z < WORLD_DEPTH)
    
    def get_block_name(self, x, y, z):
        """Get human-readable block name"""
        from utils.constants import BLOCK_NAMES
        block = self.get_block(x, y, z)
        return BLOCK_NAMES.get(block, "Unknown")
    
    def export_blocks(self):
        """Export blocks for saving"""
        return self.blocks
