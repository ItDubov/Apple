// 🛑 контейнер
const container = document.getElementById("three-container");

if (!container) {
    console.log("Three disabled");
} else {

    // ======================
    // 🌌 СЦЕНА
    // ======================
    const scene = new THREE.Scene();

    // ======================
    // 📷 КАМЕРА
    // ======================
    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.z = 6;

    // ======================
    // 🎮 РЕНДЕР
    // ======================
    const renderer = new THREE.WebGLRenderer({
        alpha: true,
        antialias: true
    });

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    container.appendChild(renderer.domElement);

    // ======================
    // 💡 СВЕТ
    // ======================
    const light = new THREE.PointLight(0xffffff, 2);
    light.position.set(10, 10, 10);
    scene.add(light);

    scene.add(new THREE.AmbientLight(0xffffff, 0.4));

    // ======================
    // ✨ ЗВЁЗДЫ
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
            "position",
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
    // 📦 ОБЪЕКТЫ
    // ======================
    const objects = [];
    const labels = [];

    const colors = [0xff0055, 0x00ffcc, 0x3366ff, 0xffcc00];
    const names = ["iPhone", "MacBook", "AirPods", "Watch"];

    for (let i = 0; i < 4; i++) {

        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshStandardMaterial({
            color: colors[i]
        });

        const cube = new THREE.Mesh(geometry, material);

        cube.position.set((i - 1.5) * 3, 0, -2);

        cube.userData = {
            name: names[i],
            index: i
        };

        scene.add(cube);
        objects.push(cube);

        // 📌 label
        const div = document.createElement("div");
        div.className = "label";
        div.innerText = names[i];
        document.body.appendChild(div);

        labels.push(div);
    }

    // ======================
    // 🖱 RAYCASTER + HOVER
    // ======================
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    let hovered = null;

    window.addEventListener("mousemove", (event) => {

        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(objects);

        if (intersects.length > 0) {

            const obj = intersects[0].object;

            if (hovered !== obj) {

                if (hovered) {
                    gsap.to(hovered.scale, { x: 1, y: 1, z: 1 });
                }

                hovered = obj;

                gsap.to(obj.scale, {
                    x: 1.2,
                    y: 1.2,
                    z: 1.2,
                    duration: 0.3
                });
            }

        } else {
            if (hovered) {
                gsap.to(hovered.scale, { x: 1, y: 1, z: 1 });
                hovered = null;
            }
        }
    });

    // ======================
    // 🖱 CLICK
    // ======================
    window.addEventListener("click", () => {

        if (!hovered) return;

        const obj = hovered;

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
                window.location.href = "/product/" + obj.userData.index;
            }
        });
    });

    // ======================
    // 🔗 СВЯЗЬ С МЕНЮ
    // ======================
    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach((item, i) => {
        item.addEventListener("click", () => {

            const obj = objects[i];

            gsap.to(camera.position, {
                x: obj.position.x,
                y: obj.position.y,
                z: 2,
                duration: 1.2,
                onUpdate: () => {
                    camera.lookAt(obj.position);
                }
            });
        });
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

        // labels
        objects.forEach((obj, i) => {

            const vector = obj.position.clone().project(camera);

            const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
            const y = (-vector.y * 0.5 + 0.5) * window.innerHeight;

            labels[i].style.transform =
                `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        });

        renderer.render(scene, camera);
    }

    animate();

    // ======================
    // 📏 RESIZE
    // ======================
    window.addEventListener("resize", () => {

        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    // ======================
    // ⏳ LOADING
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

}