document.addEventListener('DOMContentLoaded', function() {
    const galleryImages = document.querySelectorAll('.media-grid .media-card img');
    const lightboxOverlay = document.getElementById('lightbox-overlay');
    const lightboxImage = document.getElementById('lightbox-image');

    if (galleryImages.length > 0 && lightboxOverlay && lightboxImage) {
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