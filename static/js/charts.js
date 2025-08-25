// Ceramic Tile Quality Control - Charts and Analytics

/**
 * Chart.js default configuration for QC application
 */
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#6c757d';

/**
 * Default chart colors
 */
const CHART_COLORS = {
    primary: '#0d6efd',
    success: '#198754',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#0dcaf0',
    secondary: '#6c757d',
    light: '#f8f9fa',
    dark: '#212529',
    
    // Quality control specific colors
    compliant: '#28a745',
    nonCompliant: '#dc3545',
    partial: '#fd7e14',
    
    // Production stages
    clay: '#ffc107',
    press: '#17a2b8',
    dryer: '#fd7e14',
    biscuitKiln: '#dc3545',
    emailKiln: '#6f42c1',
    enamel: '#e83e8c',
    
    // Gradients
    primaryGradient: ['#0d6efd', '#0056b3'],
    successGradient: ['#28a745', '#1e7e34'],
    warningGradient: ['#ffc107', '#e0a800'],
    dangerGradient: ['#dc3545', '#c82333']
};

/**
 * Create compliance trend chart
 */
function createComplianceTrendChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Compliance Rate (%)',
                data: data.map(d => d.compliance_rate),
                borderColor: CHART_COLORS.primary,
                backgroundColor: createGradient(ctx, CHART_COLORS.primaryGradient),
                borderWidth: 3,
                pointBackgroundColor: CHART_COLORS.primary,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: CHART_COLORS.primary,
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `Compliance: ${context.parsed.y.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0,0,0,0.1)',
                        lineWidth: 1
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            elements: {
                point: {
                    hitRadius: 10
                }
            }
        }
    });
}

/**
 * Create format distribution pie chart
 */
function createFormatDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const labels = Object.keys(data);
    const values = Object.values(data);
    const colors = [
        CHART_COLORS.primary,
        CHART_COLORS.success,
        CHART_COLORS.warning,
        CHART_COLORS.info,
        CHART_COLORS.secondary
    ];
    
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 3,
                borderColor: '#ffffff',
                hoverBorderWidth: 4,
                hoverBorderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

/**
 * Create SPC (Statistical Process Control) chart
 */
function createSPCChart(canvasId, data, specs) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const chartData = {
        labels: data.map(d => d.date),
        datasets: [
            {
                label: 'Measurement',
                data: data.map(d => d.value),
                borderColor: CHART_COLORS.primary,
                backgroundColor: data.map(d => 
                    d.compliance === 'compliant' ? CHART_COLORS.success : CHART_COLORS.danger
                ),
                pointBackgroundColor: data.map(d => 
                    d.compliance === 'compliant' ? CHART_COLORS.success : CHART_COLORS.danger
                ),
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                type: 'scatter',
                showLine: true,
                tension: 0.1
            }
        ]
    };
    
    // Add specification limits if provided
    if (specs) {
        if (specs.upper) {
            chartData.datasets.push({
                label: 'Upper Limit',
                data: Array(data.length).fill(specs.upper),
                borderColor: CHART_COLORS.danger,
                borderDash: [5, 5],
                borderWidth: 2,
                pointRadius: 0,
                fill: false
            });
        }
        
        if (specs.lower) {
            chartData.datasets.push({
                label: 'Lower Limit',
                data: Array(data.length).fill(specs.lower),
                borderColor: CHART_COLORS.danger,
                borderDash: [5, 5],
                borderWidth: 2,
                pointRadius: 0,
                fill: false
            });
        }
        
        if (specs.target) {
            chartData.datasets.push({
                label: 'Target',
                data: Array(data.length).fill(specs.target),
                borderColor: CHART_COLORS.success,
                borderDash: [2, 2],
                borderWidth: 2,
                pointRadius: 0,
                fill: false
            });
        }
    }
    
    return new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 8,
                    callbacks: {
                        afterBody: function(tooltipItems) {
                            const item = tooltipItems[0];
                            const dataPoint = data[item.dataIndex];
                            return `Status: ${dataPoint.compliance}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    },
                    ticks: {
                        precision: 2
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            elements: {
                point: {
                    hitRadius: 10
                }
            }
        }
    });
}

/**
 * Create defect analysis bar chart
 */
function createDefectAnalysisChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const stages = Object.keys(data);
    const defectTypes = new Set();
    
    // Get all defect types
    stages.forEach(stage => {
        Object.keys(data[stage]).forEach(defect => {
            defectTypes.add(defect);
        });
    });
    
    const datasets = Array.from(defectTypes).map((defect, index) => ({
        label: defect.charAt(0).toUpperCase() + defect.slice(1),
        data: stages.map(stage => data[stage][defect] || 0),
        backgroundColor: Object.values(CHART_COLORS)[index % 8],
        borderWidth: 1,
        borderColor: '#ffffff'
    }));
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: stages.map(stage => stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
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

/**
 * Create production volume chart
 */
function createProductionVolumeChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.date),
            datasets: [
                {
                    label: 'Compliant',
                    data: data.map(d => d.compliant),
                    backgroundColor: CHART_COLORS.success,
                    borderWidth: 1,
                    borderColor: '#ffffff'
                },
                {
                    label: 'Non-Compliant',
                    data: data.map(d => d.non_compliant),
                    backgroundColor: CHART_COLORS.danger,
                    borderWidth: 1,
                    borderColor: '#ffffff'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Create process capability histogram
 */
function createCapabilityHistogram(canvasId, data, specs) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Calculate histogram bins
    const values = data.map(d => d.value);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const binCount = Math.min(20, Math.max(5, Math.ceil(Math.sqrt(values.length))));
    const binWidth = (max - min) / binCount;
    
    const bins = Array(binCount).fill(0).map((_, i) => ({
        x: min + (i * binWidth),
        y: 0,
        width: binWidth
    }));
    
    // Count values in each bin
    values.forEach(value => {
        const binIndex = Math.min(binCount - 1, Math.floor((value - min) / binWidth));
        bins[binIndex].y++;
    });
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bins.map(bin => bin.x.toFixed(2)),
            datasets: [{
                label: 'Frequency',
                data: bins.map(bin => bin.y),
                backgroundColor: CHART_COLORS.primary,
                borderWidth: 1,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
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

/**
 * Create gradient for chart backgrounds
 */
function createGradient(ctx, colors) {
    const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
    gradient.addColorStop(0, colors[0] + '40'); // 25% opacity
    gradient.addColorStop(1, colors[1] + '10'); // 6% opacity
    return gradient;
}

/**
 * Update chart data
 */
function updateChartData(chart, newData) {
    chart.data.datasets[0].data = newData;
    chart.update('none');
}

/**
 * Add data point to chart
 */
function addDataPoint(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset, index) => {
        dataset.data.push(data[index]);
    });
    
    // Keep only last 30 points for performance
    if (chart.data.labels.length > 30) {
        chart.data.labels.shift();
        chart.data.datasets.forEach(dataset => {
            dataset.data.shift();
        });
    }
    
    chart.update('none');
}

/**
 * Download chart as PNG
 */
function downloadChart(chart, filename) {
    const url = chart.toBase64Image();
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.png';
    a.click();
}

/**
 * Create real-time chart updater
 */
function createRealTimeUpdater(chart, updateInterval = 30000) {
    return setInterval(() => {
        if (document.visibilityState === 'visible') {
            updateChartFromAPI(chart);
        }
    }, updateInterval);
}

/**
 * Update chart from API
 */
function updateChartFromAPI(chart) {
    const chartType = chart.canvas.id;
    const apiUrl = `/api/charts/${chartType}`;
    
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            updateChartData(chart, data);
        })
        .catch(error => {
            console.error('Error updating chart:', error);
        });
}

/**
 * Initialize all charts on page
 */
function initializeCharts() {
    // Find all chart canvases and initialize them
    const chartCanvases = document.querySelectorAll('canvas[data-chart-type]');
    
    chartCanvases.forEach(canvas => {
        const chartType = canvas.getAttribute('data-chart-type');
        const chartData = JSON.parse(canvas.getAttribute('data-chart-data') || '[]');
        
        switch (chartType) {
            case 'compliance-trend':
                createComplianceTrendChart(canvas.id, chartData);
                break;
            case 'format-distribution':
                createFormatDistributionChart(canvas.id, chartData);
                break;
            case 'spc':
                const specs = JSON.parse(canvas.getAttribute('data-chart-specs') || '{}');
                createSPCChart(canvas.id, chartData, specs);
                break;
            case 'defect-analysis':
                createDefectAnalysisChart(canvas.id, chartData);
                break;
            case 'production-volume':
                createProductionVolumeChart(canvas.id, chartData);
                break;
            case 'capability-histogram':
                const capSpecs = JSON.parse(canvas.getAttribute('data-chart-specs') || '{}');
                createCapabilityHistogram(canvas.id, chartData, capSpecs);
                break;
        }
    });
}

// Export chart functions for global use
window.CeramicQCCharts = {
    createComplianceTrendChart,
    createFormatDistributionChart,
    createSPCChart,
    createDefectAnalysisChart,
    createProductionVolumeChart,
    createCapabilityHistogram,
    updateChartData,
    addDataPoint,
    downloadChart,
    createRealTimeUpdater,
    initializeCharts,
    CHART_COLORS
};

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});
