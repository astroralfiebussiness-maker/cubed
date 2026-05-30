// Player Controller
class Player {
  constructor(x = 16, y = 10, z = 16) {
    this.position = new THREE.Vector3(x, y, z);
    this.velocity = new THREE.Vector3(0, 0, 0);
    this.yaw = 0;
    this.pitch = 0;
    this.speed = 0.15;
    this.gravity = 0.01;
    this.jumpPower = 0.3;
    this.isGrounded = false;
    this.keys = {};
    this.setupInput();
  }

  setupInput() {
    window.addEventListener('keydown', (e) => {
      this.keys[e.key.toLowerCase()] = true;
    });
    window.addEventListener('keyup', (e) => {
      this.keys[e.key.toLowerCase()] = false;
    });
  }

  update(world) {
    // Get forward and right vectors
    const forward = new THREE.Vector3(
      Math.sin(this.yaw),
      0,
      Math.cos(this.yaw)
    );
    const right = new THREE.Vector3(
      Math.cos(this.yaw),
      0,
      -Math.sin(this.yaw)
    );

    // Movement
    if (this.keys['w']) this.position.addScaledVector(forward, this.speed);
    if (this.keys['s']) this.position.addScaledVector(forward, -this.speed);
    if (this.keys['a']) this.position.addScaledVector(right, -this.speed);
    if (this.keys['d']) this.position.addScaledVector(right, this.speed);

    // Jump
    if (this.keys[' '] && this.isGrounded) {
      this.velocity.y = this.jumpPower;
      this.isGrounded = false;
    }

    // Down
    if (this.keys['shift']) {
      this.position.y -= this.speed;
    }

    // Apply gravity
    this.velocity.y -= this.gravity;
    this.position.y += this.velocity.y;

    // Ground collision
    const groundY = world.getHeightAt(this.position.x, this.position.z);
    if (this.position.y <= groundY) {
      this.position.y = groundY;
      this.velocity.y = 0;
      this.isGrounded = true;
    } else {
      this.isGrounded = false;
    }

    // Bounds
    this.position.x = Math.max(0, Math.min(world.worldWidth - 1, this.position.x));
    this.position.z = Math.max(0, Math.min(world.worldDepth - 1, this.position.z));
    this.position.y = Math.max(0, Math.min(world.worldHeight - 1, this.position.y));
  }

  setRotation(yaw, pitch) {
    this.yaw = yaw;
    this.pitch = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, pitch));
  }
}
