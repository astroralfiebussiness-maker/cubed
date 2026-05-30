// Terrain Generator
class TerrainGenerator {
  constructor(seed = 12345) {
    this.seed = seed;
    this.worldWidth = 32;
    this.worldHeight = 16;
    this.worldDepth = 32;
  }

  // Simple noise function
  noise(x, z) {
    const n = Math.sin(x * 12.9898 + z * 78.233 + this.seed) * 43758.5453;
    return n - Math.floor(n);
  }

  getHeight(x, z) {
    const scale = 0.1;
    const height = 4 + Math.floor(this.noise(x * scale, z * scale) * 8);
    return Math.max(1, Math.min(14, height));
  }

  generate() {
    const blocks = [];

    for (let x = 0; x < this.worldWidth; x++) {
      blocks[x] = [];
      for (let y = 0; y < this.worldHeight; y++) {
        blocks[x][y] = [];
        for (let z = 0; z < this.worldDepth; z++) {
          const height = this.getHeight(x, z);

          if (y < height - 2) {
            blocks[x][y][z] = 1; // Stone
          } else if (y === height - 2) {
            blocks[x][y][z] = 2; // Dirt
          } else if (y === height - 1) {
            blocks[x][y][z] = 3; // Grass
          } else if (y < height + 1) {
            blocks[x][y][z] = 5; // Water
          } else {
            blocks[x][y][z] = 0; // Empty
          }
        }
      }
    }

    return blocks;
  }
}
