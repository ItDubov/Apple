
document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // 🌌 HERO CLICK ANIMATION
    // =========================
    const hero = document.getElementById("hero");
    const video = document.getElementById("bg-video");

    document.addEventListener("click", () => {

        if (!hero) return;

        const tl = gsap.timeline();

        // 🎬 hero exit animation
        tl.to(hero, {
            scale: 1.3,
            opacity: 0,
            duration: 1.2,
            ease: "power2.inOut"
        });

        // 🎥 background video fade
        if (video) {
            tl.to(video, {
                opacity: 0,
                duration: 1.2
            }, "<");
        }

        // 🚀 redirect (clean way instead of setTimeout)
        tl.add(() => {
            window.location.href = "/home/";
        });
    });


    // =========================
    // 📦 CARDS ANIMATION
    // =========================
    const cards = document.querySelectorAll(".card");

    if (cards.length > 0) {
        gsap.from(cards, {
            opacity: 0,
            y: 50,
            duration: 0.8,
            stagger: 0.15,
            ease: "power2.out"
        });
    }


    // =========================
    // 🌐 PAGE LOAD ANIMATION
    // =========================
    gsap.from("body", {
        opacity: 0,
        duration: 0.6,
        ease: "power2.out"
    });


    gsap.from(["h1", "h2"], {
        opacity: 0,
        y: 20,
        duration: 0.6,
        stagger: 0.1,
        ease: "power2.out"
    });

});
