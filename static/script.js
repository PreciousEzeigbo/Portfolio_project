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

document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.querySelector('#togglePassword');
    const passwordField = document.querySelector('#password');

    togglePassword.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // Toggle the eye slash icon
        if (type === 'password') {
            togglePassword.src = 'static/eye1.png'; // Show eye icon
        } else {
            togglePassword.src = 'static/eye.png'; // Show eye slash icon
        }
    });
});

