// Ceramic Tile Quality Control - Real-time Form Validation

/**
 * Specification limits for different control types
 */
const SPECIFICATIONS = {
    clay: {
        humidity_before_prep: { min: 2.5, max: 4.1, unit: '%' },
        humidity_after_sieving: { min: 2.0, max: 3.5, unit: '%' },
        humidity_after_prep: { min: 5.3, max: 6.3, unit: '%' },
        granulometry_refusal: { min: 10, max: 20, unit: '%' },
        calcium_carbonate: { min: 15, max: 25, unit: '%' }
    },
    
    press: {
        thickness: {
            '20x20': { min: 6.2, max: 7.2, unit: 'mm' },
            '25x40': { min: 6.8, max: 7.4, unit: 'mm' },
            '25x50': { min: 7.1, max: 7.7, unit: 'mm' }
        },
        weight: {
            '20x20': { min: 480, max: 580, unit: 'g' },
            '25x40': { min: 1150, max: 1550, unit: 'g' },
            '25x50': { min: 1800, max: 2000, unit: 'g' }
        },
        defects: {
            grains: { max: 15, unit: '%' },
            cracks: { max: 1, unit: '%' },
            cleaning: { max: 1, unit: '%' },
            foliage: { max: 1, unit: '%' },
            chipping: { max: 1, unit: '%' }
        }
    },
    
    dryer: {
        residual_humidity: { min: 0.1, max: 1.5, unit: '%' },
        defects: {
            grains: { max: 15, unit: '%' },
            cracks: { max: 1, unit: '%' },
            cleaning: { max: 1, unit: '%' },
            foliage: { max: 1, unit: '%' },
            chipping: { max: 1, unit: '%' }
        }
    },
    
    biscuit_kiln: {
        defects: {
            cracks: { max: 5, unit: '%' },
            chipping: { max: 5, unit: '%' },
            cooking: { max: 1, unit: '%' },
            foliage: { max: 1, unit: '%' },
            flatness: { max: 5, unit: '%' }
        },
        shrinkage_expansion: { min: -0.2, max: 0.4, unit: '%' },
        fire_loss: { min: 10, max: 19, unit: '%' }
    },
    
    email_kiln: {
        thermal_shock: { max: 5, unit: '%' },
        rupture_resistance: {
            thick: { min: 600, unit: 'N' },  // ≥7.5mm
            thin: { min: 200, unit: 'N' }    // <7.5mm
        },
        rupture_module: {
            thick: { min: 12, unit: 'N/mm²' },  // ≥7.5mm
            thin: { min: 15, unit: 'N/mm²' }    // <7.5mm
        },
        dimensional_deviation: {
            length: { min: -0.5, max: 0.5, unit: '%' },
            width: { min: -0.5, max: 0.5, unit: '%' },
            thickness: { min: -10, max: 10, unit: '%' }
        },
        water_absorption: { min: 9, unit: '%' },
        quality: {
            color_nuance: { max: 1, unit: '%' },
            cooking_defects: { max: 1, unit: '%' },
            flatness_defects: { max: 5, unit: '%' }
        }
    },
    
    dimensional: {
        curvature: { min: -2, max: 2, unit: 'mm' },
        edge_straightness: { min: -1.5, max: 1.5, unit: 'mm' },
        surface_quality: { min: 95, unit: '%' },
        min_tiles: 30,
        min_area: 1, // m²
        min_lighting: 300 // lux
    },
    
    enamel: {
        density: {
            engobe: { min: 1780, max: 1830, unit: 'g/l' },
            email: { min: 1730, max: 1780, unit: 'g/l' },
            mate: { min: 1780, max: 1830, unit: 'g/l' }
        },
        viscosity: { min: 25, max: 55, unit: 'seconds' },
        grammage: {
            water: {
                '20x20': { min: 0.5, max: 3, unit: 'g' },
                '25x40': { min: 1, max: 5, unit: 'g' },
                '25x50': { min: 3, max: 7, unit: 'g' }
            },
            enamel: {
                '20x20': { min: 20, max: 23, unit: 'g' },
                '25x40': { min: 50, max: 55, unit: 'g' },
                '25x50': { min: 70, max: 75, unit: 'g' }
            }
        }
    }
};

/**
 * Initialize form validation
 */
function initializeValidation(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Get form type from ID or data attribute
    const formType = getFormType(formId);
    
    // Initialize real-time validation for all inputs
    const inputs = form.querySelectorAll('input[type="number"], input[data-validate]');
    inputs.forEach(input => {
        initializeInputValidation(input, formType);
    });
    
    // Initialize format-dependent validation
    initializeFormatValidation(form, formType);
    
    // Initialize form submission validation
    form.addEventListener('submit', function(e) {
        if (!validateForm(form, formType)) {
            e.preventDefault();
            showValidationSummary(form);
        }
    });
    
    console.log(`Initialized validation for ${formType} form`);
}

/**
 * Get form type from form ID
 */
function getFormType(formId) {
    const typeMap = {
        'clayControlForm': 'clay',
        'pressControlForm': 'press',
        'dryerControlForm': 'dryer',
        'biscuitKilnForm': 'biscuit_kiln',
        'emailKilnForm': 'email_kiln',
        'dimensionalTestForm': 'dimensional',
        'enamelControlForm': 'enamel',
        'digitalDecorationForm': 'digital'
    };
    
    return typeMap[formId] || 'unknown';
}

/**
 * Initialize validation for individual input
 */
function initializeInputValidation(input, formType) {
    // Get validation parameters from data attributes or specifications
    const parameter = getParameterName(input.name);
    const specs = getSpecificationForParameter(formType, parameter, input);
    
    if (!specs) return;
    
    // Set data attributes for validation
    if (specs.min !== undefined) input.setAttribute('data-min', specs.min);
    if (specs.max !== undefined) input.setAttribute('data-max', specs.max);
    if (specs.unit) input.setAttribute('data-unit', specs.unit);
    
    // Add real-time validation
    input.addEventListener('input', function() {
        validateInput(this, specs);
    });
    
    input.addEventListener('blur', function() {
        validateInput(this, specs, true);
    });
    
    // Add helpful placeholder
    if (specs.min !== undefined && specs.max !== undefined) {
        input.placeholder = `${specs.min} - ${specs.max} ${specs.unit || ''}`;
    } else if (specs.max !== undefined) {
        input.placeholder = `≤ ${specs.max} ${specs.unit || ''}`;
    } else if (specs.min !== undefined) {
        input.placeholder = `≥ ${specs.min} ${specs.unit || ''}`;
    }
}

/**
 * Get parameter name from input name
 */
function getParameterName(inputName) {
    // Remove common prefixes and suffixes
    return inputName.replace(/^(defect_|humidity_|dimension_)/, '')
                  .replace(/(_deviation|_defects)$/, '');
}

/**
 * Get specification for parameter
 */
function getSpecificationForParameter(formType, parameter, input) {
    const specs = SPECIFICATIONS[formType];
    if (!specs) return null;
    
    // Handle nested specifications (e.g., format-dependent)
    if (specs[parameter]) {
        const spec = specs[parameter];
        
        // Check if it's format-dependent
        if (typeof spec === 'object' && spec.hasOwnProperty('20x20')) {
            const formatSelect = input.form.querySelector('[name="format_type"]');
            const format = formatSelect ? formatSelect.value : '20x20';
            return spec[format] || spec['20x20'];
        }
        
        // Check if it's enamel type dependent
        if (typeof spec === 'object' && spec.hasOwnProperty('engobe')) {
            const enamelSelect = input.form.querySelector('[name="enamel_type"]');
            const enamelType = enamelSelect ? enamelSelect.value : 'engobe';
            return spec[enamelType] || spec['engobe'];
        }
        
        return spec;
    }
    
    // Check in nested objects (defects, quality, etc.)
    for (const [category, categorySpecs] of Object.entries(specs)) {
        if (typeof categorySpecs === 'object' && categorySpecs[parameter]) {
            return categorySpecs[parameter];
        }
    }
    
    return null;
}

/**
 * Validate individual input
 */
function validateInput(input, specs, showFeedback = false) {
    const value = parseFloat(input.value);
    const isValid = validateValue(value, specs);
    
    // Update input classes
    input.classList.remove('is-valid', 'is-invalid');
    if (input.value) {
        input.classList.add(isValid ? 'is-valid' : 'is-invalid');
    }
    
    // Show/hide feedback
    const feedback = getOrCreateFeedback(input);
    if (showFeedback || !isValid) {
        if (isValid) {
            feedback.textContent = '✓ Within specification';
            feedback.className = 'valid-feedback';
        } else {
            feedback.textContent = getValidationMessage(value, specs);
            feedback.className = 'invalid-feedback';
        }
        feedback.style.display = 'block';
    }
    
    return isValid;
}

/**
 * Validate value against specifications
 */
function validateValue(value, specs) {
    if (isNaN(value)) return false;
    
    if (specs.min !== undefined && value < specs.min) return false;
    if (specs.max !== undefined && value > specs.max) return false;
    
    return true;
}

/**
 * Get validation message
 */
function getValidationMessage(value, specs) {
    if (isNaN(value)) {
        return 'Please enter a valid number';
    }
    
    if (specs.min !== undefined && specs.max !== undefined) {
        return `Value must be between ${specs.min} and ${specs.max} ${specs.unit || ''}`;
    } else if (specs.min !== undefined && value < specs.min) {
        return `Value must be at least ${specs.min} ${specs.unit || ''}`;
    } else if (specs.max !== undefined && value > specs.max) {
        return `Value must not exceed ${specs.max} ${specs.unit || ''}`;
    }
    
    return 'Value is out of specification';
}

/**
 * Get or create feedback element
 */
function getOrCreateFeedback(input) {
    let feedback = input.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    
    if (!feedback) {
        feedback = document.createElement('div');
        input.parentNode.appendChild(feedback);
    }
    
    return feedback;
}

/**
 * Initialize format-dependent validation
 */
function initializeFormatValidation(form, formType) {
    const formatSelect = form.querySelector('[name="format_type"]');
    const enamelSelect = form.querySelector('[name="enamel_type"]');
    
    if (formatSelect) {
        formatSelect.addEventListener('change', function() {
            updateFormatDependentValidation(form, formType);
        });
        
        // Trigger initial update
        updateFormatDependentValidation(form, formType);
    }
    
    if (enamelSelect) {
        enamelSelect.addEventListener('change', function() {
            updateEnamelDependentValidation(form, formType);
        });
        
        // Trigger initial update
        updateEnamelDependentValidation(form, formType);
    }
}

/**
 * Update format-dependent validation
 */
function updateFormatDependentValidation(form, formType) {
    const formatSelect = form.querySelector('[name="format_type"]');
    const format = formatSelect ? formatSelect.value : null;
    
    if (!format) return;
    
    // Update thickness and weight validation for press controls
    if (formType === 'press') {
        updatePressValidation(form, format);
    }
    
    // Update grammage validation for enamel controls
    if (formType === 'enamel') {
        updateGrammageValidation(form, format);
    }
}

/**
 * Update press validation based on format
 */
function updatePressValidation(form, format) {
    const specs = SPECIFICATIONS.press;
    
    // Update thickness validation
    const thicknessInput = form.querySelector('[name="thickness"]');
    if (thicknessInput && specs.thickness[format]) {
        const thicknessSpec = specs.thickness[format];
        thicknessInput.setAttribute('data-min', thicknessSpec.min);
        thicknessInput.setAttribute('data-max', thicknessSpec.max);
        thicknessInput.placeholder = `${thicknessSpec.min} - ${thicknessSpec.max} ${thicknessSpec.unit}`;
        
        // Update help text
        const helpText = form.querySelector('#thicknessSpec');
        if (helpText) {
            helpText.textContent = `Spec: ${thicknessSpec.min} - ${thicknessSpec.max} ${thicknessSpec.unit}`;
        }
        
        // Revalidate if has value
        if (thicknessInput.value) {
            validateInput(thicknessInput, thicknessSpec);
        }
    }
    
    // Update weight validation
    const weightInput = form.querySelector('[name="wet_weight"]');
    if (weightInput && specs.weight[format]) {
        const weightSpec = specs.weight[format];
        weightInput.setAttribute('data-min', weightSpec.min);
        weightInput.setAttribute('data-max', weightSpec.max);
        weightInput.placeholder = `${weightSpec.min} - ${weightSpec.max} ${weightSpec.unit}`;
        
        // Update help text
        const helpText = form.querySelector('#weightSpec');
        if (helpText) {
            helpText.textContent = `Spec: ${weightSpec.min} - ${weightSpec.max} ${weightSpec.unit}`;
        }
        
        // Revalidate if has value
        if (weightInput.value) {
            validateInput(weightInput, weightSpec);
        }
    }
}

/**
 * Update enamel validation based on type
 */
function updateEnamelDependentValidation(form, formType) {
    const enamelSelect = form.querySelector('[name="enamel_type"]');
    const enamelType = enamelSelect ? enamelSelect.value : null;
    
    if (!enamelType) return;
    
    const specs = SPECIFICATIONS.enamel;
    
    // Update density validation
    const densityInput = form.querySelector('[name="density"]');
    if (densityInput && specs.density[enamelType]) {
        const densitySpec = specs.density[enamelType];
        densityInput.setAttribute('data-min', densitySpec.min);
        densityInput.setAttribute('data-max', densitySpec.max);
        densityInput.placeholder = `${densitySpec.min} - ${densitySpec.max} ${densitySpec.unit}`;
        
        // Update help text
        const helpText = form.querySelector('#densitySpec');
        if (helpText) {
            helpText.textContent = `Spec: ${densitySpec.min} - ${densitySpec.max} ${densitySpec.unit}`;
        }
        
        // Revalidate if has value
        if (densityInput.value) {
            validateInput(densityInput, densitySpec);
        }
    }
}

/**
 * Update grammage validation based on format
 */
function updateGrammageValidation(form, format) {
    const specs = SPECIFICATIONS.enamel.grammage;
    
    // Update water grammage
    const waterInput = form.querySelector('[name="water_grammage"]');
    if (waterInput && specs.water[format]) {
        const waterSpec = specs.water[format];
        waterInput.setAttribute('data-min', waterSpec.min);
        waterInput.setAttribute('data-max', waterSpec.max);
        waterInput.placeholder = `${waterSpec.min} - ${waterSpec.max} ${waterSpec.unit}`;
        
        // Update help text
        const helpText = form.querySelector('#waterSpec');
        if (helpText) {
            helpText.textContent = `Spec: ${waterSpec.min} - ${waterSpec.max} ${waterSpec.unit}`;
        }
    }
    
    // Update enamel grammage
    const enamelInput = form.querySelector('[name="enamel_grammage"]');
    if (enamelInput && specs.enamel[format]) {
        const enamelSpec = specs.enamel[format];
        enamelInput.setAttribute('data-min', enamelSpec.min);
        enamelInput.setAttribute('data-max', enamelSpec.max);
        enamelInput.placeholder = `${enamelSpec.min} - ${enamelSpec.max} ${enamelSpec.unit}`;
        
        // Update help text
        const helpText = form.querySelector('#enamelSpec');
        if (helpText) {
            helpText.textContent = `Spec: ${enamelSpec.min} - ${enamelSpec.max} ${enamelSpec.unit}`;
        }
    }
}

/**
 * Validate entire form
 */
function validateForm(form, formType) {
    const inputs = form.querySelectorAll('input[type="number"], input[data-validate]');
    let isValid = true;
    
    inputs.forEach(input => {
        const parameter = getParameterName(input.name);
        const specs = getSpecificationForParameter(formType, parameter, input);
        
        if (specs && input.value) {
            const inputValid = validateInput(input, specs, true);
            if (!inputValid) {
                isValid = false;
            }
        }
    });
    
    return isValid;
}

/**
 * Show validation summary
 */
function showValidationSummary(form) {
    const invalidInputs = form.querySelectorAll('.is-invalid');
    
    if (invalidInputs.length === 0) return;
    
    let message = `Please correct the following ${invalidInputs.length} error(s):\n\n`;
    
    invalidInputs.forEach((input, index) => {
        const label = form.querySelector(`label[for="${input.id}"]`) || 
                     form.querySelector(`label[for="${input.name}"]`);
        const labelText = label ? label.textContent : input.name;
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        const errorText = feedback ? feedback.textContent : 'Invalid value';
        
        message += `${index + 1}. ${labelText}: ${errorText}\n`;
    });
    
    alert(message);
    
    // Focus first invalid input
    invalidInputs[0].focus();
}

/**
 * Real-time compliance indicator
 */
function updateComplianceIndicator(form, formType) {
    const indicator = form.querySelector('.compliance-indicator');
    if (!indicator) return;
    
    const inputs = form.querySelectorAll('input[type="number"]');
    let totalInputs = 0;
    let validInputs = 0;
    
    inputs.forEach(input => {
        if (input.value) {
            totalInputs++;
            if (input.classList.contains('is-valid')) {
                validInputs++;
            }
        }
    });
    
    if (totalInputs === 0) {
        indicator.textContent = 'No data entered';
        indicator.className = 'compliance-indicator partial';
        return;
    }
    
    const complianceRate = (validInputs / totalInputs) * 100;
    
    if (complianceRate === 100) {
        indicator.textContent = 'All parameters compliant';
        indicator.className = 'compliance-indicator compliant';
    } else if (complianceRate === 0) {
        indicator.textContent = 'Non-compliant measurements detected';
        indicator.className = 'compliance-indicator non-compliant';
    } else {
        indicator.textContent = `${validInputs}/${totalInputs} parameters compliant`;
        indicator.className = 'compliance-indicator partial';
    }
}

/**
 * Initialize surface quality calculation for dimensional tests
 */
function initializeSurfaceQualityCalculation(form) {
    const tilesTestedInput = form.querySelector('[name="tiles_tested"]');
    const defectFreeInput = form.querySelector('[name="defect_free_tiles"]');
    const qualityIndicator = form.querySelector('#surfaceQualityIndicator');
    
    if (!tilesTestedInput || !defectFreeInput) return;
    
    function updateSurfaceQuality() {
        const total = parseInt(tilesTestedInput.value) || 0;
        const defectFree = parseInt(defectFreeInput.value) || 0;
        
        if (total > 0 && defectFree >= 0) {
            const percentage = (defectFree / total) * 100;
            const isCompliant = percentage >= 95;
            
            if (qualityIndicator) {
                qualityIndicator.textContent = `${percentage.toFixed(1)}% defect-free`;
                qualityIndicator.className = `badge ${isCompliant ? 'bg-success' : 'bg-danger'}`;
            }
            
            // Validate defect-free input
            defectFreeInput.classList.remove('is-valid', 'is-invalid');
            if (defectFree <= total) {
                defectFreeInput.classList.add(isCompliant ? 'is-valid' : 'is-invalid');
            }
        }
    }
    
    tilesTestedInput.addEventListener('input', updateSurfaceQuality);
    defectFreeInput.addEventListener('input', updateSurfaceQuality);
}

// Export validation functions
window.CeramicQCValidation = {
    initializeValidation,
    validateInput,
    validateForm,
    updateComplianceIndicator,
    SPECIFICATIONS
};

// Auto-initialize validation for forms with specific IDs
document.addEventListener('DOMContentLoaded', function() {
    const formIds = [
        'clayControlForm',
        'pressControlForm', 
        'dryerControlForm',
        'biscuitKilnForm',
        'emailKilnForm',
        'dimensionalTestForm',
        'enamelControlForm',
        'digitalDecorationForm'
    ];
    
    formIds.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            initializeValidation(formId);
        }
    });
});
