"""
Terrain generation system
"""

import random
from utils.constants import (
    WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH,
    BLOCK_EMPTY, BLOCK_STONE, BLOCK_DIRT, BLOCK_GRASS, BLOCK_SAND, BLOCK_WATER
)


class TerrainGenerator:
    """Generates terrain for the game world"""
    
    def __init__(self, seed=None):
        """Initialize terrain generator
        
        Args:
            seed: Random seed for reproducible terrain
        """
        if seed is not None:
            random.seed(seed)
        self.seed = seed
    
    def generate(self):
        """Generate terrain for the entire world
        
        Returns:
            3D list of blocks
        """
        # Initialize empty world
        world = [[[BLOCK_EMPTY for _ in range(WORLD_DEPTH)]
                  for _ in range(WORLD_HEIGHT)]
                 for _ in range(WORLD_WIDTH)]
        
        # Generate terrain height map
        height_map = self._generate_height_map()
        
        # Fill world based on height map
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_DEPTH):
                height = height_map[x][z]
                
                for y in range(WORLD_HEIGHT):
                    if y < height - 1:
                        # Stone layer
                        world[x][y][z] = BLOCK_STONE
                    elif y == height - 1:
                        # Dirt layer
                        world[x][y][z] = BLOCK_DIRT
                    elif y == height:
                        # Grass on top
                        world[x][y][z] = BLOCK_GRASS
                    elif y < height + 2:  # Water level
                        # Water
                        world[x][y][z] = BLOCK_WATER
        
        return world
    
    def _generate_height_map(self):
        """Generate simple height map using random noise
        
        Returns:
            2D list of heights
        """
        # Simple grid-based generation
        # Divide world into chunks and assign heights
        
        height_map = [[0 for _ in range(WORLD_DEPTH)] for _ in range(WORLD_WIDTH)]
        
        chunk_size = 4
        
        # Generate height for each chunk
        for chunk_x in range(0, WORLD_WIDTH, chunk_size):
            for chunk_z in range(0, WORLD_DEPTH, chunk_size):
                # Random height for this chunk (between 4 and 12)
                base_height = random.randint(4, 12)
                
                # Fill chunk with this height
                for x in range(chunk_x, min(chunk_x + chunk_size, WORLD_WIDTH)):
                    for z in range(chunk_z, min(chunk_z + chunk_size, WORLD_DEPTH)):
                        # Add some variation within chunk
                        variation = random.randint(-1, 1)
                        height_map[x][z] = max(1, base_height + variation)
        
        return height_map
