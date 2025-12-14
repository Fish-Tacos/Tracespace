/**
 * Trace Space - 3D Visualization Engine
 * Renders organisms as pulsing spheres in 3D space
 */

let scene, camera, renderer, organisms = [];
let raycaster, mouse;
let currentData = null;
let controls = { mouseDown: false, mouseX: 0, mouseY: 0 };

// Configuration
const CONFIG = {
    autoRefreshInterval: 60000, // 60 seconds
    cameraDistance: 30,
    cameraRotationSpeed: 0.0002,
    pulseAmplitude: 0.15,
    driftSpeed: 0.005
};

/**
 * Initialize Three.js scene
 */
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    scene.fog = new THREE.Fog(0x000000, 20, 60);

    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = CONFIG.cameraDistance;

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00ff00, 1, 100);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);

    const pointLight2 = new THREE.PointLight(0x0088ff, 0.5, 100);
    pointLight2.position.set(-10, -10, 10);
    scene.add(pointLight2);

    // Raycaster for mouse interaction
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // Event listeners
    window.addEventListener('resize', onWindowResize);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('wheel', onMouseWheel);

    // Load data and start
    loadOrganismData();
    animate();
    
    // Auto-refresh
    setInterval(loadOrganismData, CONFIG.autoRefreshInterval);
}

/**
 * Load organism data from server
 */
async function loadOrganismData() {
    try {
        const response = await fetch('/data/latest.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        currentData = data;
        
        // Clear existing organisms
        clearOrganisms();
        
        // Create new organisms
        createOrganisms(data);
        
        // Update UI
        updateInfoPanel(data);
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('status').textContent = 'Active';
        
    } catch (error) {
        console.error('Error loading organism data:', error);
        document.getElementById('status').textContent = 'Error';
        document.getElementById('loading').textContent = 'Failed to load data. Retrying...';
    }
}

/**
 * Clear all organisms from scene
 */
function clearOrganisms() {
    organisms.forEach(org => {
        scene.remove(org.mesh);
        if (org.mesh.geometry) org.mesh.geometry.dispose();
        if (org.mesh.material) org.mesh.material.dispose();
    });
    organisms = [];
}

/**
 * Create organism meshes from data
 */
function createOrganisms(data) {
    // Level 1: Sub-components (smallest organisms)
    if (data.subcomponents) {
        data.subcomponents.forEach((subcomp, index) => {
            createOrganism(subcomp, 'subcomponent', index);
        });
    }
    
    // Level 2: Components (medium organisms)
    if (data.components) {
        data.components.forEach((comp, index) => {
            createOrganism(comp, 'component', index);
        });
    }
    
    // Level 3: Entity (largest organism)
    if (data.entity) {
        createOrganism(data.entity, 'entity', 0);
    }
}

/**
 * Create single organism mesh
 */
function createOrganism(data, level, index) {
    // Geometry - sphere with detail based on level
    const detail = level === 'entity' ? 64 : level === 'component' ? 32 : 16;
    const geometry = new THREE.SphereGeometry(data.size, detail, detail);
    
    // Material - color from data with emissive glow
    const color = new THREE.Color(
        data.color.r,
        data.color.g,
        data.color.b
    );
    
    const material = new THREE.MeshPhongMaterial({
        color: color,
        emissive: color,
        emissiveIntensity: 0.4,
        shininess: 30,
        transparent: true,
        opacity: level === 'entity' ? 0.3 : level === 'component' ? 0.6 : 0.9
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    
    // Position
    mesh.position.set(
        data.position.x,
        data.position.y,
        data.position.z
    );
    
    // Store organism data
    const organism = {
        mesh: mesh,
        data: data,
        level: level,
        baseSize: data.size,
        velocity: data.velocity,
        phase: Math.random() * Math.PI * 2 // Random starting phase for variety
    };
    
    scene.add(mesh);
    organisms.push(organism);
}

/**
 * Animation loop
 */
function animate() {
    requestAnimationFrame(animate);
    
    const time = Date.now() * 0.001; // Time in seconds
    
    // Animate each organism
    organisms.forEach(org => {
        // Pulsing effect (size oscillation)
        const pulseSpeed = org.velocity * 2 + 0.5;
        const pulse = Math.sin(time * pulseSpeed + org.phase) * CONFIG.pulseAmplitude + 1;
        org.mesh.scale.setScalar(pulse);
        
        // Gentle drift (subtle position changes)
        if (org.level === 'subcomponent') {
            org.mesh.position.x += Math.sin(time * CONFIG.driftSpeed + org.phase) * 0.01;
            org.mesh.position.y += Math.cos(time * CONFIG.driftSpeed + org.phase * 1.3) * 0.01;
        }
        
        // Rotation
        org.mesh.rotation.x += 0.001;
        org.mesh.rotation.y += 0.002;
    });
    
    // Camera orbit (slow rotation around scene)
    if (!controls.mouseDown) {
        const radius = CONFIG.cameraDistance;
        camera.position.x = Math.sin(time * CONFIG.cameraRotationSpeed) * radius;
        camera.position.z = Math.cos(time * CONFIG.cameraRotationSpeed) * radius;
        camera.lookAt(scene.position);
    }
    
    renderer.render(scene, camera);
}

/**
 * Update info panel with current data
 */
function updateInfoPanel(data) {
    if (data.stats) {
        document.getElementById('organism-count').textContent = data.stats.total_organisms || 0;
        document.getElementById('total-engagement').textContent = 
            (data.stats.total_engagement || 0).toLocaleString();
    }
    
    if (data.timestamp) {
        const time = new Date(data.timestamp);
        document.getElementById('last-update').textContent = 
            time.toLocaleTimeString();
    }
}

/**
 * Mouse move handler - show tooltip on hover
 */
function onMouseMove(event) {
    // Update mouse position
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    
    // Raycasting to detect hover
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(organisms.map(o => o.mesh));
    
    const tooltip = document.getElementById('tooltip');
    
    if (intersects.length > 0) {
        // Find the organism
        const intersectedMesh = intersects[0].object;
        const organism = organisms.find(o => o.mesh === intersectedMesh);
        
        if (organism && organism.level === 'subcomponent') {
            // Show tooltip for sub-components only (they have actual post data)
            showTooltip(event, organism);
        } else {
            tooltip.style.display = 'none';
        }
    } else {
        tooltip.style.display = 'none';
    }
    
    // Manual camera control
    if (controls.mouseDown) {
        const deltaX = event.clientX - controls.mouseX;
        const deltaY = event.clientY - controls.mouseY;
        
        camera.position.x += deltaX * 0.05;
        camera.position.y -= deltaY * 0.05;
        camera.lookAt(scene.position);
        
        controls.mouseX = event.clientX;
        controls.mouseY = event.clientY;
    }
}

/**
 * Show tooltip with organism details
 */
function showTooltip(event, organism) {
    const tooltip = document.getElementById('tooltip');
    const data = organism.data;
    
    let html = `<div class="tooltip-title">${data.metadata.source.toUpperCase()} Organism</div>`;
    
    if (data.metadata.author) {
        html += `<div class="tooltip-author">@${data.metadata.author}</div>`;
    }
    
    if (data.text) {
        html += `<div class="tooltip-text">${data.text}</div>`;
    }
    
    if (data.metadata.engagement !== undefined) {
        html += `<div class="tooltip-stats">`;
        html += `Engagement: ${data.metadata.engagement.toLocaleString()} `;
        html += `(❤️ ${data.metadata.likes} | 🔁 ${data.metadata.reposts} | 💬 ${data.metadata.replies})`;
        html += `</div>`;
    }
    
    tooltip.innerHTML = html;
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 15) + 'px';
    tooltip.style.top = (event.clientY + 15) + 'px';
}

/**
 * Mouse down handler
 */
function onMouseDown(event) {
    controls.mouseDown = true;
    controls.mouseX = event.clientX;
    controls.mouseY = event.clientY;
}

/**
 * Mouse up handler
 */
function onMouseUp(event) {
    controls.mouseDown = false;
}

/**
 * Mouse wheel handler - zoom
 */
function onMouseWheel(event) {
    event.preventDefault();
    
    const zoomSpeed = 2;
    camera.position.z += event.deltaY * 0.01 * zoomSpeed;
    
    // Clamp zoom
    camera.position.z = Math.max(10, Math.min(60, camera.position.z));
}

/**
 * Window resize handler
 */
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Initialize when page loads
window.onload = init;
