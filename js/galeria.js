document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    let lastScrollY = window.scrollY;
    let scrollThreshold = 50;

    window.addEventListener('scroll', () => {
        if (window.scrollY > lastScrollY && window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
            header.classList.remove('up');
        } else if (window.scrollY < lastScrollY && window.scrollY > scrollThreshold) {
            header.classList.add('up');
        } else if (window.scrollY <= scrollThreshold) {
            header.classList.remove('scrolled');
            header.classList.remove('up');
        }
        lastScrollY = window.scrollY;
    });

    const hamburger = document.querySelector('.hamburger');
    const mainNav = document.querySelector('.main-nav');
    
    hamburger.addEventListener('click', function() {
        mainNav.classList.toggle('active');
    });

    const galleryImages = document.querySelectorAll('.media-grid .media-card img');
    const lightboxOverlay = document.getElementById('lightbox-overlay');
    const lightboxImage = document.getElementById('lightbox-image');

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
});