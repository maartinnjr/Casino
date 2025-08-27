document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
=======
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

    // --- Lógica original de la Galería ---
>>>>>>> 1bf6cbece2dee54ab6b8d722d7355c4cef9e0304
    const galleryImages = document.querySelectorAll('.media-grid .media-card img');
    const lightboxOverlay = document.getElementById('lightbox-overlay');
    const lightboxImage = document.getElementById('lightbox-image');

<<<<<<< HEAD
    if (galleryImages.length > 0 && lightboxOverlay && lightboxImage) {
=======
    if (galleryImages.length > 0 && lightboxOverlay) {
>>>>>>> 1bf6cbece2dee54ab6b8d722d7355c4cef9e0304
        galleryImages.forEach(image => {
            image.addEventListener('click', () => {
                const imageUrl = image.getAttribute('src');
                lightboxImage.setAttribute('src', imageUrl);
                lightboxOverlay.classList.remove('hidden');
            });
        });

        lightboxOverlay.addEventListener('click', () => {
            lightboxOverlay.classList.add('hidden');
        });
    }
});