document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('type');
    const body = document.body;

    function updateBackground() {
        body.classList.remove('entrada-bg', 'saida-bg');
        if (typeSelect.value === 'entrada') {
            body.classList.add('entrada-bg');
        } else if (typeSelect.value === 'saida') {
            body.classList.add('saida-bg');
        }
    }

    updateBackground();

    typeSelect.addEventListener('change', updateBackground);
});