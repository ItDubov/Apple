
// ======================
// 🌌 СЦЕНА
// ======================
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

// ======================
// 📷 КАМЕРА
// ======================
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.z = 6;

// ======================
// 🎮 РЕНДЕР
// ======================
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// ======================
// 💡 СВЕТ
// ======================
const light = new THREE.PointLight(0xffffff, 2);
light.position.set(10, 10, 10);
scene.add(light);

const ambient = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambient);

// ======================
// ✨ ЗВЁЗДЫ (КОСМОС)
// ======================
function addStars() {
    const geometry = new THREE.BufferGeometry();
    const vertices = [];

    for (let i = 0; i < 1500; i++) {
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
        size: 0.5
    });

    const stars = new THREE.Points(geometry, material);
    scene.add(stars);
}

addStars();

// ======================
// 📦 ОБЪЕКТЫ (ТОВАРЫ)
// ======================
const objects = [];

const colors = [0xff0055, 0x00ffcc, 0x3366ff, 0xffcc00];
const names = ["iPhone", "MacBook", "AirPods", "Watch"];

for (let i = 0; i < 4; i++) {

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({
        color: colors[i]
    });

    const cube = new THREE.Mesh(geometry, material);

    cube.position.set(
        (i - 1.5) * 3,
        0,
        -2
    );

    cube.userData = {
        name: names[i],
        index: i
    };

    scene.add(cube);
    objects.push(cube);

    // 🌐 HTML LABEL
    const div = document.createElement("div");
    div.className = "label";
    div.innerText = names[i];
    div.style.position = "absolute";
    div.style.color = "white";
    div.style.fontSize = "14px";
    div.style.pointerEvents = "none";

    document.body.appendChild(div);
}

// ======================
// 🖱 RAYCASTER
// ======================
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener("click", (event) => {

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(objects);

    if (intersects.length > 0) {

        const obj = intersects[0].object;

        gsap.to(camera.position, {
            x: obj.position.x,
            y: obj.position.y,
            z: 2,
            duration: 1.2,
            ease: "power2.inOut",
            onComplete: () => {
                window.location.href = "/product/" + obj.userData.index;
            }
        });
    }
});

// ======================
// 🌀 АНИМАЦИЯ
// ======================
function animate() {
    requestAnimationFrame(animate);

    objects.forEach((obj, i) => {
        obj.rotation.y += 0.01;
        obj.position.y = Math.sin(Date.now() * 0.001 + i) * 0.2;
    });

    // 📌 labels follow objects
    objects.forEach((obj, i) => {

        const vector = obj.position.clone();
        vector.project(camera);

        const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-vector.y * 0.5 + 0.5) * window.innerHeight;

        const label = document.getElementsByClassName("label")[i];

        if (label) {
            label.style.transform =
                `translate(-50%, -50%) translate(${x}px,${y}px)`;
        }
    });

    renderer.render(scene, camera);
}

animate();

// ======================
// 📏 RESIZE FIX
// ======================
window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ======================
// ⏳ LOADING FIX
// ======================
window.addEventListener("load", () => {
    const loader = document.getElementById("loading");

    if (loader) {
        gsap.to(loader, {
            opacity: 0,
            duration: 1,
            onComplete: () => loader.remove()
        });
    }
});
