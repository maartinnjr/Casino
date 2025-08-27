document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    const hamburger = document.querySelector('.hamburger');
    const mainNav = document.querySelector('.main-nav');
    let lastScrollY = window.scrollY;

    if (hamburger && mainNav) {
        hamburger.addEventListener('click', function() {
            const isOpening = !mainNav.classList.contains('active');
            mainNav.classList.toggle('active');
            hamburger.classList.toggle('is-active');
            document.body.classList.toggle('menu-open');
        });
    }

    window.addEventListener('scroll', () => {
        if (mainNav && mainNav.classList.contains('active')) {
            return;
        }

        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            header.classList.add('hidden');
        } else if (window.scrollY < lastScrollY) {
            header.classList.remove('hidden');
        }
        
        lastScrollY = window.scrollY < 0 ? 0 : window.scrollY;
    });

    const backButton = document.getElementById('btn-retroceso');
    if (backButton) {
        backButton.addEventListener('click', () => {
            window.history.back();
        });
    }
});