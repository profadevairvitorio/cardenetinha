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

    const newCategoryBtn = document.getElementById('new-category-btn');
    const cancelNewCategoryBtn = document.getElementById('cancel-new-category-btn');
    const categorySelectDiv = document.getElementById('category-select-div');
    const newCategoryDiv = document.getElementById('new-category-div');
    const categoryIdField = document.getElementById('category_id');
    const newCategoryField = document.getElementById('new_category');

    if (newCategoryBtn) {
        newCategoryBtn.addEventListener('click', function() {
            categorySelectDiv.style.display = 'none';
            newCategoryDiv.style.display = 'block';
            if (categoryIdField) {
                $(categoryIdField).val(null).trigger('change');
            }
        });
    }

    if (cancelNewCategoryBtn) {
        cancelNewCategoryBtn.addEventListener('click', function() {
            categorySelectDiv.style.display = 'block';
            newCategoryDiv.style.display = 'none';
            if (newCategoryField) {
                newCategoryField.value = '';
            }
        });
    }
});