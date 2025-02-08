document.addEventListener('DOMContentLoaded', function() {
    gsap.from('.header', {
        duration: 1,
        y: -100,
        opacity: 0,
        ease: 'power3.out'
    });

    gsap.from('.welcome-banner', {
        duration: 1,
        opacity: 0,
        delay: 0.5,
        ease: 'power3.out'
    });

    gsap.from('.table-info-card', {
        duration: 1,
        y: 50,
        opacity: 0,
        delay: 1,
        ease: 'power3.out'
    });
    gsap.to('.mascot-image', {
        y: -10,
        rotation: 2,
        duration: 1.5,
        yoyo: true,
        repeat: -1,
        ease: "power1.inOut"
    });

    // Остальные анимации
    gsap.from('.header', {
        duration: 1,
        y: -50,
        opacity: 0,
        ease: 'power3.out'
    });

    gsap.from('.welcome-message', {
        duration: 1,
        opacity: 0,
        delay: 0.3,
        ease: 'power3.out'
    });

    gsap.from('.menu-item', {
        duration: 0.8,
        y: 30,
        opacity: 0,
        stagger: 0.1,
        ease: 'power3.out'
    });

    gsap.from('.social-link', {
        duration: 0.5,
        x: 30,
        opacity: 0,
        stagger: 0.1,
        delay: 1,
        ease: 'power3.out'
    });
    gsap.from('.menu-choice-wrapper', {
        duration: 0.8,
        opacity: 0,
        y: 30,
        ease: 'power3.out'
    });

    gsap.from('.menu-lang-btn', {
        duration: 0.5,
        opacity: 0,
        y: 20,
        stagger: 0.1,
        delay: 0.3,
        ease: 'power3.out'
    });
    const buttons = document.querySelectorAll('.ripple-effect');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.offsetLeft;
            const y = e.clientY - e.target.offsetTop;

            const ripple = document.createElement('span');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.className = 'ripple';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
    const menuButtons = document.querySelectorAll('.menu-lang-btn');
    
    menuButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = '';
            }, 150);
        });
    });
});
