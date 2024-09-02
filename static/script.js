document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.background-image');
    let currentIndex = 0;

    function changeBackground() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
    }

    // Change background every 2 seconds (2000 milliseconds)
    setInterval(changeBackground, 2000);
});

document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');

    // Get the URLs from the data attributes
    const eyeIcon = togglePassword.getAttribute('data-eye-icon');
    const eyeSlashIcon = togglePassword.getAttribute('data-eye-slash-icon');

    togglePassword.addEventListener('click', function() {
        // Toggle the type attribute
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // Toggle the eye slash icon
        if (type === 'password') {
            togglePassword.querySelector('img').src = eyeIcon; // Show eye icon
        } else {
            togglePassword.querySelector('img').src = eyeSlashIcon; // Show eye slash icon
        }
    });
});

