// Main Game Class
class CubedGame {
  constructor() {
    console.log('Initializing Cubed Game...');

    // Three.js setup
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x87ceeb);
    this.scene.fog = new THREE.Fog(0x87ceeb, 80, 150);

    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    document.getElementById('gameContainer').appendChild(this.renderer.domElement);

    // Game state
    this.blockTypes = {
      0: { name: 'Air', color: 0x87ceeb },
      1: { name: 'Stone', color: 0x808080 },
      2: { name: 'Dirt', color: 0x8b7355 },
      3: { name: 'Grass', color: 0x228b22 },
      4: { name: 'Sand', color: 0xf4a460 },
      5: { name: 'Water', color: 0x4488ff }
    };

    this.selectedBlock = 3; // Grass
    this.meshGroup = new THREE.Group();
    this.scene.add(this.meshGroup);

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(50, 50, 50);
    light.castShadow = true;
    this.scene.add(light);

    const ambient = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambient);

    // Generate world
    console.log('Generating terrain...');
    const generator = new TerrainGenerator(42);
    this.blocks = generator.generate();
    this.worldWidth = generator.worldWidth;
    this.worldHeight = generator.worldHeight;
    this.worldDepth = generator.worldDepth;

    // Render blocks
    this.renderWorld();

    // Player
    this.player = new Player(16, 10, 16);
    this.camera.position.copy(this.player.position);
    this.camera.position.y += 0.6;

    // Input
    this.setupInput();

    // FPS counter
    this.frameCount = 0;
    this.lastTime = Date.now();

    // Hide loading
    document.getElementById('loading').style.display = 'none';

    console.log('Game ready!');
    this.animate();
  }

  renderWorld() {
    for (let x = 0; x < this.worldWidth; x++) {
      for (let y = 0; y < this.worldHeight; y++) {
        for (let z = 0; z < this.worldDepth; z++) {
          const blockType = this.blocks[x][y][z];
          if (blockType !== 0) {
            this.createBlockMesh(x, y, z, blockType);
          }
        }
      }
    }
  }

  createBlockMesh(x, y, z, blockType) {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const color = this.blockTypes[blockType].color;
    const material = new THREE.MeshStandardMaterial({
      color: color,
      roughness: 0.8,
      metalness: 0.1
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(x + 0.5, y + 0.5, z + 0.5);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.userData = { x, y, z, blockType };

    this.meshGroup.add(mesh);
  }

  setupInput() {
    document.addEventListener('mousemove', (e) => this.onMouseMove(e));
    document.addEventListener('mousedown', (e) => this.onMouseClick(e));
    document.addEventListener('keydown', (e) => this.onKeyDown(e));
    document.addEventListener('contextmenu', (e) => e.preventDefault());
    window.addEventListener('resize', () => this.onResize());
  }

  onMouseMove(e) {
    const sensitivity = 0.003;
    this.player.yaw -= e.movementX * sensitivity;
    this.player.pitch -= e.movementY * sensitivity;
    this.player.pitch = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.player.pitch));
  }

  onMouseClick(e) {
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(new THREE.Vector2(0, 0), this.camera);

    const intersects = raycaster.intersectObjects(this.meshGroup.children);

    if (intersects.length > 0) {
      const hit = intersects[0];
      const data = hit.object.userData;

      if (e.button === 0) { // Left click - break
        this.breakBlock(data.x, data.y, data.z);
      } else if (e.button === 2) { // Right click - place
        const normal = hit.face.normal;
        const nx = data.x + Math.round(normal.x);
        const ny = data.y + Math.round(normal.y);
        const nz = data.z + Math.round(normal.z);
        this.placeBlock(nx, ny, nz);
      }
    }
  }

  onKeyDown(e) {
    const key = e.key.toLowerCase();
    if (key === '1') this.selectedBlock = 1;
    if (key === '2') this.selectedBlock = 2;
    if (key === '3') this.selectedBlock = 3;
    if (key === '4') this.selectedBlock = 4;
    if (key === '5') this.selectedBlock = 5;
  }

  breakBlock(x, y, z) {
    if (this.isInBounds(x, y, z)) {
      this.blocks[x][y][z] = 0;
      this.refreshMesh(x, y, z);
    }
  }

  placeBlock(x, y, z) {
    if (this.isInBounds(x, y, z) && this.blocks[x][y][z] === 0) {
      this.blocks[x][y][z] = this.selectedBlock;
      this.refreshMesh(x, y, z);
    }
  }

  refreshMesh(x, y, z) {
    // Remove old mesh
    const toRemove = this.meshGroup.children.filter(
      child => child.userData.x === x && child.userData.y === y && child.userData.z === z
    );
    toRemove.forEach(mesh => this.meshGroup.remove(mesh));

    // Add new mesh if not empty
    const blockType = this.blocks[x][y][z];
    if (blockType !== 0) {
      this.createBlockMesh(x, y, z, blockType);
    }
  }

  isInBounds(x, y, z) {
    return x >= 0 && x < this.worldWidth &&
           y >= 0 && y < this.worldHeight &&
           z >= 0 && z < this.worldDepth;
  }

  getHeightAt(x, z) {
    x = Math.floor(x);
    z = Math.floor(z);
    if (!this.isInBounds(x, 0, z)) return 0;

    for (let y = this.worldHeight - 1; y >= 0; y--) {
      if (this.blocks[x][y][z] !== 0) {
        return y + 1;
      }
    }
    return 0;
  }

  updateHUD() {
    const pos = this.player.position;
    document.getElementById('posX').textContent = pos.x.toFixed(1);
    document.getElementById('posY').textContent = pos.y.toFixed(1);
    document.getElementById('posZ').textContent = pos.z.toFixed(1);

    const bx = Math.floor(pos.x);
    const by = Math.floor(pos.y);
    const bz = Math.floor(pos.z);
    if (this.isInBounds(bx, by, bz)) {
      const blockType = this.blocks[bx][by][bz];
      document.getElementById('blockType').textContent = this.blockTypes[blockType].name;
    }
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    this.player.update(this);

    // Update camera
    this.camera.position.copy(this.player.position);
    this.camera.position.y += 0.6;
    this.camera.rotation.order = 'YXZ';
    this.camera.rotation.y = this.player.yaw;
    this.camera.rotation.x = this.player.pitch;

    // FPS
    this.frameCount++;
    const now = Date.now();
    if (now - this.lastTime >= 1000) {
      document.getElementById('fpsValue').textContent = this.frameCount;
      this.frameCount = 0;
      this.lastTime = now;
    }

    this.updateHUD();
    this.renderer.render(this.scene, this.camera);
  }
}

// Lock pointer
document.addEventListener('click', () => {
  document.body.requestPointerLock();
});

// Start game
window.addEventListener('load', () => {
  try {
    window.game = new CubedGame();
  } catch (e) {
    console.error('Game error:', e);
    document.getElementById('loading').textContent = 'ERROR: ' + e.message;
    document.getElementById('loading').style.display = 'block';
  }
});
