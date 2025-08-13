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

    const contactForm = document.getElementById('contact-form');
    const confirmationModal = document.getElementById('confirmation-modal');
    
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();

        console.log('Formulario enviado!');

        contactForm.reset();

        confirmationModal.classList.remove('hidden');
    });

    confirmationModal.addEventListener('click', function(event) {
        if (event.target === confirmationModal) {
            confirmationModal.classList.add('hidden');
        }
    });
});