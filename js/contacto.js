document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    const confirmationModal = document.getElementById('confirmation-modal');
    
    if (contactForm && confirmationModal) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            contactForm.reset();
            confirmationModal.classList.remove('hidden');
        });

        confirmationModal.addEventListener('click', function() {
            confirmationModal.classList.add('hidden');
        });
    }
});