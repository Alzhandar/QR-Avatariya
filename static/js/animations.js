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
});