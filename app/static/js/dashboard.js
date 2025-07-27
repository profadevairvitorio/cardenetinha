document.addEventListener('DOMContentLoaded', function() {
    const incomeData = JSON.parse(document.getElementById('incomeData').textContent);
    const expensesData = JSON.parse(document.getElementById('expensesData').textContent);

    var incomeCtx = document.getElementById('incomeChart').getContext('2d');
    var incomeChart = new Chart(incomeCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(incomeData),
            datasets: [{
                label: 'Receitas por Categoria',
                data: Object.values(incomeData),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var expensesCtx = document.getElementById('expensesChart').getContext('2d');
    var expensesChart = new Chart(expensesCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(expensesData),
            datasets: [{
                label: 'Despesas por Categoria',
                data: Object.values(expensesData),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});