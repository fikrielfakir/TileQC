/**
 * Ceramic QC - Touch-Optimized Main JavaScript
 * Enhanced for tablets and tactile screens with modern interactions
 */

class CeramicQCApp {
    constructor() {
        this.touchDevice = this.detectTouchDevice();
        this.charts = new Map();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeTooltips();
        this.setupTouchInteractions();
        this.setupResponsiveFeatures();
        this.initializeAccessibility();
        this.initializeFormEnhancements();
        this.initializeAutoRefresh();
        this.initializeKeyboardShortcuts();
        this.initializeNotifications();
        
        console.log('Ceramic QC Application initialized successfully - Touch device:', this.touchDevice);
    }

    detectTouchDevice() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
    }

    setupEventListeners() {
        // Navigation enhancement
        this.setupNavigationEnhancements();
        
        // Form enhancements
        this.setupAdvancedFormEnhancements();
        
        // Card interactions
        this.setupCardInteractions();
        
        // Button enhancements
        this.setupButtonEnhancements();
        
        // Search functionality
        this.setupSearchFunctionality();
    }

    setupNavigationEnhancements() {
        const navbar = document.querySelector('.navbar');
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                if (!navbar.contains(e.target)) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            }
        });

        // Auto-close mobile menu when selecting nav item
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1200 && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });

        // Enhance dropdown interactions for touch devices
        if (this.touchDevice) {
            this.enhanceDropdownsForTouch();
        }
    }

    enhanceDropdownsForTouch() {
        const dropdowns = document.querySelectorAll('.dropdown');
        
        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            if (toggle && menu) {
                // Add touch-friendly spacing
                toggle.style.minHeight = '44px';
                
                // Prevent default behavior and manually handle dropdown
                toggle.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    const bsDropdown = new bootstrap.Dropdown(toggle);
                    bsDropdown.toggle();
                });
            }
        });
    }

    setupAdvancedFormEnhancements() {
        // Auto-resize textareas
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            this.autoResizeTextarea(textarea);
            textarea.addEventListener('input', () => this.autoResizeTextarea(textarea));
        });

        // Enhanced input focus/blur effects
        const inputs = document.querySelectorAll('.form-control, .form-select');
        inputs.forEach(input => {
            input.addEventListener('focus', (e) => {
                e.target.parentElement.classList.add('input-focused');
            });
            
            input.addEventListener('blur', (e) => {
                e.target.parentElement.classList.remove('input-focused');
            });
        });

        // Number input enhancement for touch devices
        if (this.touchDevice) {
            this.enhanceNumberInputsForTouch();
        }

        // Auto-save form data
        this.initializeAutoSave();
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    enhanceNumberInputsForTouch() {
        const numberInputs = document.querySelectorAll('input[type="number"]:not(.enhanced)');
        
        numberInputs.forEach(input => {
            // Mark as enhanced to avoid duplicate processing
            input.classList.add('enhanced');
            
            // Increase touch target size
            input.style.minHeight = '44px';
            input.style.fontSize = '16px'; // Prevent zoom on iOS
        });
    }

    initializeAutoSave() {
        const forms = document.querySelectorAll('form[data-auto-save]');
        forms.forEach(form => {
            const formId = form.id || form.getAttribute('data-auto-save');
            
            // Load saved data
            this.loadFormData(form, formId);
            
            // Save data on input
            form.addEventListener('input', this.debounce(() => {
                this.saveFormData(form, formId);
            }, 1000));
            
            // Clear saved data on successful submit
            form.addEventListener('submit', () => {
                this.clearFormData(formId);
            });
        });
    }

    saveFormData(form, formId) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem(`ceramic_qc_form_${formId}`, JSON.stringify(data));
    }

    loadFormData(form, formId) {
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

    clearFormData(formId) {
        localStorage.removeItem(`ceramic_qc_form_${formId}`);
    }

    setupCardInteractions() {
        const cards = document.querySelectorAll('.card, .stats-card, .stage-card');
        
        cards.forEach(card => {
            // Add ripple effect for touch devices
            if (this.touchDevice) {
                card.addEventListener('touchstart', (e) => {
                    this.createRippleEffect(e, card);
                });
            }
            
            // Enhance hover effects for non-touch devices
            if (!this.touchDevice) {
                card.addEventListener('mouseenter', () => {
                    card.style.transform = 'translateY(-2px)';
                });
                
                card.addEventListener('mouseleave', () => {
                    card.style.transform = '';
                });
            }
        });
    }

    setupButtonEnhancements() {
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            // Add touch feedback
            if (this.touchDevice) {
                button.addEventListener('touchstart', (e) => {
                    button.style.transform = 'scale(0.98)';
                    this.createRippleEffect(e, button);
                });
                
                button.addEventListener('touchend', () => {
                    setTimeout(() => {
                        button.style.transform = '';
                    }, 100);
                });
            }
            
            // Prevent double-tap zoom on buttons
            button.style.touchAction = 'manipulation';
        });
    }

    createRippleEffect(e, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.touches ? e.touches[0].clientX - rect.left - size / 2 : e.clientX - rect.left - size / 2;
        const y = e.touches ? e.touches[0].clientY - rect.top - size / 2 : e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple-effect');
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    setupSearchFunctionality() {
        const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
        
        searchInputs.forEach(input => {
            let searchTimeout;
            
            input.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performSearch(e.target.value, input);
                }, 300);
            });
        });
    }

    performSearch(query, inputElement) {
        const targetTable = inputElement.dataset.target;
        if (targetTable) {
            this.filterTable(targetTable, query);
        }
    }

    filterTable(tableId, query) {
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const rows = table.querySelectorAll('tbody tr');
        const searchTerm = query.toLowerCase().trim();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const shouldShow = searchTerm === '' || text.includes(searchTerm);
            row.style.display = shouldShow ? '' : 'none';
        });
    }

    setupResponsiveFeatures() {
        // Responsive table wrapper
        const tables = document.querySelectorAll('.table');
        tables.forEach(table => {
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });

        // Responsive navigation adjustments
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));
    }

    handleResize() {
        const width = window.innerWidth;
        
        // Update navigation based on screen size
        const navbarNav = document.querySelector('.navbar-nav');
        if (navbarNav) {
            if (width < 1200) {
                navbarNav.classList.add('mobile-nav');
            } else {
                navbarNav.classList.remove('mobile-nav');
            }
        }
        
        // Adjust chart responsiveness
        this.charts.forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }

    initializeTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                trigger: this.touchDevice ? 'click' : 'hover'
            });
        });

        // Initialize Bootstrap popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    setupTouchInteractions() {
        if (!this.touchDevice) return;
        
        // Disable hover effects on touch devices
        document.body.classList.add('touch-device');
        
        // Enhanced swipe detection for cards
        this.setupSwipeDetection();
        
        // Touch-friendly form validation
        this.setupTouchFormValidation();
    }

    setupSwipeDetection() {
        let startX, startY, startTime;
        
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
                startTime = Date.now();
            }
        });
        
        document.addEventListener('touchend', (e) => {
            if (e.changedTouches.length === 1) {
                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                const endTime = Date.now();
                
                const deltaX = endX - startX;
                const deltaY = endY - startY;
                const deltaTime = endTime - startTime;
                
                // Detect horizontal swipe
                if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50 && deltaTime < 300) {
                    const direction = deltaX > 0 ? 'right' : 'left';
                    this.handleSwipe(direction, e.target);
                }
            }
        });
    }

    handleSwipe(direction, element) {
        // Find the closest swipeable element
        const swipeableElement = element.closest('[data-swipe]');
        if (swipeableElement) {
            const swipeAction = swipeableElement.dataset.swipe;
            this.executeSwipeAction(swipeAction, direction, swipeableElement);
        }
    }

    executeSwipeAction(action, direction, element) {
        switch (action) {
            case 'navigate':
                if (direction === 'left') {
                    const nextButton = element.querySelector('.btn-next, .page-next');
                    if (nextButton) nextButton.click();
                } else if (direction === 'right') {
                    const prevButton = element.querySelector('.btn-prev, .page-prev');
                    if (prevButton) prevButton.click();
                }
                break;
            case 'dismiss':
                if (direction === 'right') {
                    element.style.transform = 'translateX(100%)';
                    element.style.opacity = '0';
                    setTimeout(() => {
                        element.remove();
                    }, 300);
                }
                break;
        }
    }

    setupTouchFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateInputOnTouch(input);
                });
            });
        });
    }

    validateInputOnTouch(input) {
        setTimeout(() => {
            if (input.checkValidity()) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
            }
        }, 100);
    }

    initializeAccessibility() {
        this.setupSkipLinks();
        this.setupFocusManagement();
        this.setupScreenReaderAnnouncements();
    }

    setupSkipLinks() {
        const skipLinks = document.querySelectorAll('.skip-link, .visually-hidden-focusable');
        skipLinks.forEach(link => {
            link.addEventListener('focus', () => {
                link.style.position = 'fixed';
                link.style.top = '10px';
                link.style.left = '10px';
                link.style.zIndex = '9999';
            });
        });
    }

    setupFocusManagement() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                const focusableElements = modal.querySelectorAll('button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
                if (focusableElements.length > 0) {
                    focusableElements[0].focus();
                }
            });
        });
    }

    setupScreenReaderAnnouncements() {
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'visually-hidden';
        liveRegion.id = 'liveRegion';
        document.body.appendChild(liveRegion);
        
        this.liveRegion = liveRegion;
    }

    initializeFormEnhancements() {
        // Initialize date inputs with current date
        const dateInputs = document.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            if (!input.value) {
                input.value = new Date().toISOString().split('T')[0];
            }
        });

        // Initialize number formatting
        this.initializeNumberFormatting();
    }

    initializeNumberFormatting() {
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

    initializeAutoRefresh() {
        if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
            setInterval(() => {
                if (document.visibilityState === 'visible') {
                    this.refreshDashboardData();
                }
            }, 300000);
        }
    }

    initializeKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
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
            
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                const addButton = document.querySelector('a[href*="/add"]');
                if (addButton) {
                    window.location.href = addButton.href;
                }
            }
            
            if (e.key === 'Escape') {
                const backButton = document.querySelector('a[href*="back"], .btn-outline-secondary');
                if (backButton) {
                    window.location.href = backButton.href || history.back();
                }
            }
        });
    }

    initializeNotifications() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    async refreshDashboardData() {
        const currentDate = document.getElementById('dateFilter')?.value || new Date().toISOString().split('T')[0];
        
        try {
            const response = await fetch(`/api/dashboard/stats?date=${currentDate}`);
            if (response.ok) {
                const data = await response.json();
                this.updateDashboardStats(data);
                this.showNotification('Dashboard data refreshed', 'success');
            }
        } catch (error) {
            console.error('Error refreshing dashboard:', error);
        }
    }

    updateDashboardStats(data) {
        // Update overall compliance rate
        const complianceElement = document.querySelector('[data-stat="compliance-rate"]');
        if (complianceElement) {
            complianceElement.textContent = data.overall.compliance_rate + '%';
        }
        
        // Update other stats
        const totalElement = document.querySelector('[data-stat="total-tests"]');
        if (totalElement) {
            totalElement.textContent = data.overall.total;
        }
        
        const compliantElement = document.querySelector('[data-stat="compliant-tests"]');
        if (compliantElement) {
            compliantElement.textContent = data.overall.compliant;
        }
        
        const nonCompliantElement = document.querySelector('[data-stat="non-compliant-tests"]');
        if (nonCompliantElement) {
            nonCompliantElement.textContent = data.overall.non_compliant;
        }
    }

    // Utility functions
    debounce(func, wait) {
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

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Public API methods
    showNotification(message, type = 'info') {
        const alertClass = type === 'error' ? 'danger' : type;
        const iconClass = type === 'error' ? 'exclamation-triangle-fill' : 
                         type === 'success' ? 'check-circle-fill' : 'info-circle-fill';
        
        const alertHtml = `
            <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert" aria-live="polite" 
                 style="position: fixed; top: 20px; right: 20px; z-index: 1050; min-width: 300px;">
                <i class="bi bi-${iconClass}" aria-hidden="true"></i>
                <span class="ms-1">${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert[style*="position: fixed"]');
            const lastAlert = alerts[alerts.length - 1];
            if (lastAlert) {
                const alert = new bootstrap.Alert(lastAlert);
                alert.close();
            }
        }, 5000);
        
        // Announce to screen readers
        this.announceToScreenReader(message);
    }

    announceToScreenReader(message) {
        if (this.liveRegion) {
            this.liveRegion.textContent = message;
            setTimeout(() => {
                this.liveRegion.textContent = '';
            }, 1000);
        }
    }

    showLoading(show = true) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            if (show) {
                loadingOverlay.classList.remove('d-none');
            } else {
                loadingOverlay.classList.add('d-none');
            }
        }
    }

    formatNumber(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    }

    calculateComplianceRate(compliant, total) {
        if (total === 0) return 0;
        return Math.round((compliant / total) * 100 * 10) / 10;
    }

    confirmDelete(message = 'Are you sure you want to delete this record?') {
        return confirm(message);
    }

    exportToCSV(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        window.URL.revokeObjectURL(url);
    }

    convertToCSV(data) {
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
}

// Add modern CSS styles
const modernCSS = `
.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.4);
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.touch-device .card:hover,
.touch-device .btn:hover,
.touch-device .stats-card:hover {
    transform: none !important;
}

.input-focused {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 61, 157, 0.15);
}

.mobile-nav .dropdown-menu {
    border: none;
    box-shadow: none;
    background: transparent;
    padding: 0;
}

.mobile-nav .dropdown-item {
    padding-left: 3rem;
    border-radius: 0;
}

@media (max-width: 768px) {
    .btn.w-100 {
        min-height: 60px !important;
        padding: 1rem 0.5rem !important;
    }
    
    .btn.w-100 i {
        font-size: 1.2em !important;
        margin-bottom: 0.25rem !important;
    }
    
    .stats-card {
        padding: 1.25rem !important;
    }
    
    .stats-icon {
        width: 50px !important;
        height: 50px !important;
        font-size: 1.25rem !important;
    }
    
    .stats-value {
        font-size: 1.75rem !important;
    }
}
`;

// Inject CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = modernCSS;
document.head.appendChild(styleSheet);

// Initialize the app
let ceramicQCApp;
document.addEventListener('DOMContentLoaded', () => {
    ceramicQCApp = new CeramicQCApp();
    window.CeramicQC = ceramicQCApp;
});

// Legacy compatibility
window.showNotification = (message, type = 'info', duration = 3000) => {
    if (window.CeramicQC && window.CeramicQC.showNotification) {
        window.CeramicQC.showNotification(message, type);
    }
};

window.refreshDashboardData = () => {
    if (window.CeramicQC && window.CeramicQC.refreshDashboardData) {
        return window.CeramicQC.refreshDashboardData();
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CeramicQCApp;
}