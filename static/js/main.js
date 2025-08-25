// Ceramic Tile Quality Control - Main JavaScript

/**
 * Main application initialization and utilities
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize modals
    initializeModals();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize auto-refresh for dashboard
    initializeAutoRefresh();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Initialize notification system
    initializeNotifications();
    
    console.log('Ceramic QC Application initialized successfully');
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap modals
 */
function initializeModals() {
    const modalElements = document.querySelectorAll('.modal');
    modalElements.forEach(modalEl => {
        modalEl.addEventListener('shown.bs.modal', function() {
            const firstInput = modalEl.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
}

/**
 * Initialize form enhancements
 */
function initializeFormEnhancements() {
    // Auto-save form data to localStorage
    const forms = document.querySelectorAll('form[data-auto-save]');
    forms.forEach(form => {
        const formId = form.id || form.getAttribute('data-auto-save');
        
        // Load saved data
        loadFormData(form, formId);
        
        // Save data on input
        form.addEventListener('input', debounce(() => {
            saveFormData(form, formId);
        }, 1000));
        
        // Clear saved data on successful submit
        form.addEventListener('submit', () => {
            clearFormData(formId);
        });
    });
    
    // Format number inputs
    initializeNumberFormatting();
    
    // Initialize date inputs with current date
    initializeDateInputs();
}

/**
 * Initialize auto-refresh for dashboard
 */
function initializeAutoRefresh() {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        // Refresh every 5 minutes
        setInterval(() => {
            if (document.visibilityState === 'visible') {
                refreshDashboardData();
            }
        }, 300000);
    }
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save forms
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const activeForm = document.querySelector('form:focus-within');
            if (activeForm) {
                const submitBtn = activeForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        }
        
        // Ctrl/Cmd + N for new entries
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const addButton = document.querySelector('a[href*="/add"]');
            if (addButton) {
                window.location.href = addButton.href;
            }
        }
        
        // Escape to cancel/go back
        if (e.key === 'Escape') {
            const backButton = document.querySelector('a[href*="back"], .btn-outline-secondary');
            if (backButton) {
                window.location.href = backButton.href || history.back();
            }
        }
    });
}

/**
 * Initialize notification system
 */
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Save form data to localStorage
 */
function saveFormData(form, formId) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(`ceramic_qc_form_${formId}`, JSON.stringify(data));
}

/**
 * Load form data from localStorage
 */
function loadFormData(form, formId) {
    const savedData = localStorage.getItem(`ceramic_qc_form_${formId}`);
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input && !input.value) {
                    input.value = data[key];
                }
            });
        } catch (e) {
            console.warn('Error loading saved form data:', e);
        }
    }
}

/**
 * Clear saved form data
 */
function clearFormData(formId) {
    localStorage.removeItem(`ceramic_qc_form_${formId}`);
}

/**
 * Initialize number formatting for inputs
 */
function initializeNumberFormatting() {
    const numberInputs = document.querySelectorAll('input[type="number"], input[data-type="decimal"]');
    
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const num = parseFloat(this.value);
                if (!isNaN(num)) {
                    const decimals = this.getAttribute('data-decimals') || 2;
                    this.value = num.toFixed(decimals);
                }
            }
        });
        
        // Add visual formatting
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.getAttribute('data-min'));
            const max = parseFloat(this.getAttribute('data-max'));
            
            if (!isNaN(value) && !isNaN(min) && !isNaN(max)) {
                this.classList.remove('is-valid', 'is-invalid');
                if (value >= min && value <= max) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            }
        });
    });
}

/**
 * Initialize date inputs
 */
function initializeDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = new Date().toISOString().split('T')[0];
        }
    });
}

/**
 * Refresh dashboard data
 */
function refreshDashboardData() {
    const currentDate = document.getElementById('dateFilter')?.value || new Date().toISOString().split('T')[0];
    
    fetch(`/api/dashboard/stats?date=${currentDate}`)
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
            showNotification('Dashboard data refreshed', 'info');
        })
        .catch(error => {
            console.error('Error refreshing dashboard:', error);
        });
}

/**
 * Update dashboard statistics
 */
function updateDashboardStats(data) {
    // Update overall compliance rate
    const complianceElement = document.querySelector('[data-stat="compliance-rate"]');
    if (complianceElement) {
        complianceElement.textContent = data.overall.compliance_rate + '%';
    }
    
    // Update total tests
    const totalElement = document.querySelector('[data-stat="total-tests"]');
    if (totalElement) {
        totalElement.textContent = data.overall.total;
    }
    
    // Update compliant tests
    const compliantElement = document.querySelector('[data-stat="compliant-tests"]');
    if (compliantElement) {
        compliantElement.textContent = data.overall.compliant;
    }
    
    // Update non-compliant tests
    const nonCompliantElement = document.querySelector('[data-stat="non-compliant-tests"]');
    if (nonCompliantElement) {
        nonCompliantElement.textContent = data.overall.non_compliant;
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    
    notification.innerHTML = `
        <i class="bi bi-${getIconForType(type)}"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }
    }, duration);
}

/**
 * Get icon for notification type
 */
function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'danger': 'x-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Debounce function to limit function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number for display
 */
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

/**
 * Calculate compliance percentage
 */
function calculateComplianceRate(compliant, total) {
    if (total === 0) return 0;
    return Math.round((compliant / total) * 100 * 10) / 10;
}

/**
 * Export data to CSV
 */
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    
    window.URL.revokeObjectURL(url);
}

/**
 * Convert data to CSV format
 */
function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = data.map(row => {
        return headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        }).join(',');
    });
    
    return [csvHeaders, ...csvRows].join('\n');
}

/**
 * Confirm delete action
 */
function confirmDelete(message = 'Are you sure you want to delete this record?') {
    return confirm(message);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard', 'success', 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copied to clipboard', 'success', 2000);
    });
}

/**
 * Format date for display
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    
    switch (format) {
        case 'YYYY-MM-DD':
            return `${year}-${month}-${day}`;
        case 'DD/MM/YYYY':
            return `${day}/${month}/${year}`;
        case 'MM/DD/YYYY':
            return `${month}/${day}/${year}`;
        default:
            return d.toLocaleDateString();
    }
}

/**
 * Get compliance status class
 */
function getComplianceClass(status) {
    const classes = {
        'compliant': 'text-success',
        'non_compliant': 'text-danger',
        'partial': 'text-warning'
    };
    return classes[status] || 'text-secondary';
}

/**
 * Animate number counting
 */
function animateValue(element, start, end, duration = 1000) {
    const startTimestamp = performance.now();
    const step = (timestamp) => {
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };
    requestAnimationFrame(step);
}

/**
 * Load more data (infinite scroll)
 */
function loadMoreData(url, container, page = 1) {
    const loading = document.createElement('div');
    loading.className = 'text-center p-3';
    loading.innerHTML = '<div class="loading"></div> Loading more data...';
    container.appendChild(loading);
    
    fetch(`${url}?page=${page}`)
        .then(response => response.json())
        .then(data => {
            container.removeChild(loading);
            appendDataToContainer(data, container);
        })
        .catch(error => {
            console.error('Error loading more data:', error);
            container.removeChild(loading);
            showNotification('Error loading data', 'danger');
        });
}

/**
 * Append data to container
 */
function appendDataToContainer(data, container) {
    data.forEach(item => {
        const element = createDataElement(item);
        container.appendChild(element);
    });
}

/**
 * Search and filter table data
 */
function filterTable(input, tableId) {
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('ceramic_qc_dark_mode', document.body.classList.contains('dark-mode'));
}

/**
 * Initialize dark mode from saved preference
 */
function initializeDarkMode() {
    const darkMode = localStorage.getItem('ceramic_qc_dark_mode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
}

// Global utilities
window.CeramicQC = {
    showNotification,
    confirmDelete,
    copyToClipboard,
    formatDate,
    formatNumber,
    calculateComplianceRate,
    exportToCSV,
    animateValue,
    toggleDarkMode,
    getComplianceClass
};

// Initialize dark mode on load
initializeDarkMode();
