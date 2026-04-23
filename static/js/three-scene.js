
// 🛑 safety check
const container = document.getElementById("three-container");

if (!container) {
    console.log("Three.js disabled");
} else {

    // =====================
    // 🌌 SCENE
    // =====================
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    // =====================
    // 📷 CAMERA
    // =====================
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 6;

    // =====================
    // 🎮 RENDERER
    // =====================
    const renderer = new THREE.WebGLRenderer({
        alpha: true,
        antialias: true
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // =====================
    // 💡 LIGHT
    // =====================
    const light = new THREE.DirectionalLight(0xffffff, 1.2);
    light.position.set(3, 3, 5);
    scene.add(light);

    scene.add(new THREE.AmbientLight(0xffffff, 0.4));

    // =====================
    // ✨ STARS (COSMOS BACKGROUND)
    // =====================
    function addStars() {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];

        for (let i = 0; i < 2000; i++) {
            vertices.push(
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200
            );
        }

        geometry.setAttribute(
            'position',
            new THREE.Float32BufferAttribute(vertices, 3)
        );

        const material = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.4
        });

        const stars = new THREE.Points(geometry, material);
        scene.add(stars);
    }

    addStars();

    // =====================
    // 📦 PRODUCTS
    // =====================
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const products = [];

    for (let i = 0; i < 5; i++) {

        const material = new THREE.MeshStandardMaterial({
            color: new THREE.Color(`hsl(${i * 60}, 80%, 55%)`)
        });

        const cube = new THREE.Mesh(geometry, material);

        cube.position.set((i - 2) * 2.2, 0, -2);

        cube.userData = {
            id: i
        };

        scene.add(cube);
        products.push(cube);
    }

    // =====================
    // 🖱 RAYCASTER
    // =====================
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    let selected = null;

    window.addEventListener("click", (event) => {

        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);

        const intersects = raycaster.intersectObjects(products);

        if (intersects.length > 0) {

            const obj = intersects[0].object;
            const id = obj.userData.id;

            selected = obj;

            // 🎥 CAMERA ANIMATION
            gsap.to(camera.position, {
                x: obj.position.x,
                y: obj.position.y,
                z: 2,
                duration: 1.2,
                ease: "power2.inOut",
                onUpdate: () => {
                    camera.lookAt(obj.position);
                },
                onComplete: () => {
                    window.location.href = `/product/${id}/`;
                }
            });

            // 💥 click effect
            gsap.to(obj.scale, {
                x: 1.3,
                y: 1.3,
                z: 1.3,
                duration: 0.2,
                yoyo: true,
                repeat: 1
            });
        }
    });

    // =====================
    // 🌀 FLOAT ANIMATION
    // =====================
    function animate() {
        requestAnimationFrame(animate);

        products.forEach((p, i) => {

            p.rotation.y += 0.005;

            // floating effect
            p.position.y = Math.sin(Date.now() * 0.001 + i) * 0.3;
        });

        renderer.render(scene, camera);
    }

    animate();

    // =====================
    // 📱 RESIZE FIX
    // =====================
    window.addEventListener("resize", () => {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}
