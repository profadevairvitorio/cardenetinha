document.addEventListener('DOMContentLoaded', function() {
    const incomeData = JSON.parse(document.getElementById('incomeData').textContent);
    const expensesData = JSON.parse(document.getElementById('expensesData').textContent);

    function getChartOptions() {
        return {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, ticks) {
                            return new Intl.NumberFormat('pt-BR', {
                                style: 'currency', currency: 'BRL' }).format(value);
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('pt-BR', {
                                    style: 'currency', currency: 'BRL' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        };
    }

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
        options: getChartOptions()
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
        options: getChartOptions()
    });
});