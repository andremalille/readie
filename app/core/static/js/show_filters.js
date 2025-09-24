
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('filterToggleBtn');
    const filters = document.getElementById('filters');
    const overlay = document.getElementById('menuOverlay');

    function openFilters() {
        filters.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeFilters() {
        filters.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    toggleBtn.addEventListener('click', openFilters);
    overlay.addEventListener('click', closeFilters);
});
