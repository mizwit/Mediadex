// Set default theme for client
if (!localStorage.getItem('theme')) {
    localStorage.setItem('theme', 'light');
}

document.addEventListener('DOMContentLoaded', () => {

    // Apply stored theme on load
    applyTheme(localStorage.getItem('theme'));

    // Toggle between dark and light mode
    document.getElementById('theme').addEventListener('click', toggleTheme);

    function applyTheme(theme) {
        // Update Bootstrap data attribute and mode icon
        document.querySelector('html').dataset.bsTheme = theme;
        const icon = document.getElementById('mode-icon');
        if (theme === 'dark') {
            icon.classList.replace('bi-sun-fill', 'bi-moon-stars-fill');
        } else {
            icon.classList.replace('bi-moon-stars-fill', 'bi-sun-fill');
        }
    }

    function toggleTheme() {
        const currentTheme = localStorage.getItem('theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    }
});