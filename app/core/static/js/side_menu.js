document.addEventListener('DOMContentLoaded', function () {
    const burgerBtn = document.getElementById('burgerMenuBtn');
    const closeBtn = document.getElementById('closeMenuBtn');
    const sideMenu = document.getElementById('sideMenu');
    const overlay = document.getElementById('menuOverlay');
    const burgerContainer = document.querySelector('.burger-menu-container');

    burgerBtn.addEventListener('click', function () {
        sideMenu.classList.add('active');
        overlay.classList.add('active');
        burgerContainer.classList.add('hidden');
        document.body.style.overflow = 'hidden';
    });

    function closeMenu() {
        sideMenu.classList.remove('active');
        overlay.classList.remove('active');
        burgerContainer.classList.remove('hidden');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);

    const menuLinks = document.querySelectorAll('.side-menu-link');
    menuLinks.forEach(link => {
        link.addEventListener('click', function () {
            setTimeout(closeMenu, 100);
        });
    });
});