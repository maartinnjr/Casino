document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    const hamburger = document.querySelector('.hamburger');
    const mainNav = document.querySelector('.main-nav');
    let lastScrollY = window.scrollY;

    hamburger.addEventListener('click', function() {
        const isOpening = !mainNav.classList.contains('active');
        mainNav.classList.toggle('active');
        hamburger.classList.toggle('is-active');

        if (isOpening) {
            header.classList.remove('scrolled', 'up');
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });

    window.addEventListener('scroll', () => {
        if (!mainNav.classList.contains('active')) {
            if (window.scrollY > lastScrollY && window.scrollY > 100) {
                header.classList.add('scrolled');
                header.classList.remove('up');
            } else if (window.scrollY < lastScrollY) {
                header.classList.add('up');
            }
            if (window.scrollY <= 50) {
                 header.classList.remove('scrolled', 'up');
            }
            lastScrollY = window.scrollY;
        }
    });
});