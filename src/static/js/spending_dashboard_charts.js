/**
 * Spending dashboard chart initialization
 * Category pie chart and daily spending trend chart
 */

function initCategoryChart(chartData) {
    const categoryCtx = document.getElementById('categoryChart');
    if (!categoryCtx || !chartData || !chartData.labels || chartData.labels.length === 0) {
        return;
    }

    new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Spending by Category',
                data: chartData.data,
                backgroundColor: chartData.colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            let value = context.parsed || 0;
                            return label + ': $' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function initDailyChart(chartData) {
    const dailyCtx = document.getElementById('dailyChart');
    if (!dailyCtx || !chartData || !chartData.labels || chartData.labels.length === 0) {
        return;
    }

    new Chart(dailyCtx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Daily Spending',
                data: chartData.data,
                borderColor: '#f5576c',
                backgroundColor: 'rgba(245, 87, 108, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#f5576c',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Initialize charts after page loads
document.addEventListener('DOMContentLoaded', function() {
    // Get chart data from global variable (set by template)
    if (typeof window.categoryChartData !== 'undefined') {
        initCategoryChart(window.categoryChartData);
    }
    if (typeof window.dailyChartData !== 'undefined') {
        initDailyChart(window.dailyChartData);
    }
});




