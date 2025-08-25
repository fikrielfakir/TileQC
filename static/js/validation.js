// Contrôle Qualité Carreaux Céramiques - Validation de Formulaires en Temps Réel

/**
 * Limites de spécifications pour différents types de contrôles
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
        viscosity: { min: 25, max: 55, unit: 'secondes' },
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
 * Initialiser la validation des formulaires
 */
function initializeValidation(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Obtenir le type de formulaire depuis l'ID ou l'attribut data
    const formType = getFormType(formId);
    
    // Initialiser la validation en temps réel pour toutes les saisies
    const inputs = form.querySelectorAll('input[type="number"], input[data-validate]');
    inputs.forEach(input => {
        initializeInputValidation(input, formType);
    });
    
    // Initialiser la validation dépendante du format
    initializeFormatValidation(form, formType);
    
    // Initialiser la validation de soumission du formulaire
    form.addEventListener('submit', function(e) {
        if (!validateForm(form, formType)) {
            e.preventDefault();
            showValidationSummary(form);
        }
    });
    
    console.log(`Validation initialisée pour le formulaire ${formType}`);
}

/**
 * Obtenir le type de formulaire depuis l'ID du formulaire
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
    
    return typeMap[formId] || 'inconnu';
}

/**
 * Initialiser la validation pour une saisie individuelle
 */
function initializeInputValidation(input, formType) {
    // Obtenir les paramètres de validation depuis les attributs data ou les spécifications
    const parameter = getParameterName(input.name);
    const specs = getSpecificationForParameter(formType, parameter, input);
    
    if (!specs) return;
    
    // Définir les attributs data pour la validation
    if (specs.min !== undefined) input.setAttribute('data-min', specs.min);
    if (specs.max !== undefined) input.setAttribute('data-max', specs.max);
    if (specs.unit) input.setAttribute('data-unit', specs.unit);
    
    // Ajouter la validation en temps réel
    input.addEventListener('input', function() {
        validateInput(this, specs);
    });
    
    input.addEventListener('blur', function() {
        validateInput(this, specs, true);
    });
    
    // Ajouter un placeholder utile
    if (specs.min !== undefined && specs.max !== undefined) {
        input.placeholder = `${specs.min} - ${specs.max} ${specs.unit || ''}`;
    } else if (specs.max !== undefined) {
        input.placeholder = `≤ ${specs.max} ${specs.unit || ''}`;
    } else if (specs.min !== undefined) {
        input.placeholder = `≥ ${specs.min} ${specs.unit || ''}`;
    }
}

/**
 * Obtenir le nom du paramètre depuis le nom de la saisie
 */
function getParameterName(inputName) {
    // Supprimer les préfixes et suffixes communs
    return inputName.replace(/^(defect_|humidity_|dimension_)/, '')
                  .replace(/(_deviation|_defects)$/, '');
}

/**
 * Obtenir les spécifications pour un paramètre
 */
function getSpecificationForParameter(formType, parameter, input) {
    const specs = SPECIFICATIONS[formType];
    if (!specs) return null;
    
    // Gérer les spécifications imbriquées (ex: dépendantes du format)
    if (specs[parameter]) {
        const spec = specs[parameter];
        
        // Vérifier si c'est dépendant du format
        if (typeof spec === 'object' && spec.hasOwnProperty('20x20')) {
            const formatSelect = input.form.querySelector('[name="format_type"]');
            const format = formatSelect ? formatSelect.value : '20x20';
            return spec[format] || spec['20x20'];
        }
        
        // Vérifier si c'est dépendant du type d'émail
        if (typeof spec === 'object' && spec.hasOwnProperty('engobe')) {
            const enamelSelect = input.form.querySelector('[name="enamel_type"]');
            const enamelType = enamelSelect ? enamelSelect.value : 'engobe';
            return spec[enamelType] || spec['engobe'];
        }
        
        return spec;
    }
    
    // Vérifier dans les objets imbriqués (défauts, qualité, etc.)
    for (const [category, categorySpecs] of Object.entries(specs)) {
        if (typeof categorySpecs === 'object' && categorySpecs[parameter]) {
            return categorySpecs[parameter];
        }
    }
    
    return null;
}

/**
 * Valider une saisie individuelle
 */
function validateInput(input, specs, showFeedback = false) {
    const value = parseFloat(input.value);
    const isValid = validateValue(value, specs);
    
    // Mettre à jour les classes de saisie
    input.classList.remove('is-valid', 'is-invalid');
    if (input.value) {
        input.classList.add(isValid ? 'is-valid' : 'is-invalid');
    }
    
    // Afficher/masquer le feedback
    const feedback = getOrCreateFeedback(input);
    if (showFeedback || !isValid) {
        if (isValid) {
            feedback.textContent = '✓ Dans les spécifications';
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
 * Valider la valeur par rapport aux spécifications
 */
function validateValue(value, specs) {
    if (isNaN(value)) return false;
    
    if (specs.min !== undefined && value < specs.min) return false;
    if (specs.max !== undefined && value > specs.max) return false;
    
    return true;
}

/**
 * Obtenir le message de validation
 */
function getValidationMessage(value, specs) {
    if (isNaN(value)) {
        return 'Veuillez saisir un nombre valide';
    }
    
    if (specs.min !== undefined && specs.max !== undefined) {
        return `La valeur doit être entre ${specs.min} et ${specs.max} ${specs.unit || ''}`;
    } else if (specs.min !== undefined && value < specs.min) {
        return `La valeur doit être d'au moins ${specs.min} ${specs.unit || ''}`;
    } else if (specs.max !== undefined && value > specs.max) {
        return `La valeur ne doit pas dépasser ${specs.max} ${specs.unit || ''}`;
    }
    
    return 'Valeur hors spécification';
}

/**
 * Obtenir ou créer l'élément de feedback
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
 * Initialiser la validation dépendante du format
 */
function initializeFormatValidation(form, formType) {
    const formatSelect = form.querySelector('[name="format_type"]');
    const enamelSelect = form.querySelector('[name="enamel_type"]');
    
    if (formatSelect) {
        formatSelect.addEventListener('change', function() {
            updateFormatDependentValidation(form, formType);
        });
        
        // Déclencher la mise à jour initiale
        updateFormatDependentValidation(form, formType);
    }
    
    if (enamelSelect) {
        enamelSelect.addEventListener('change', function() {
            updateEnamelDependentValidation(form, formType);
        });
        
        // Déclencher la mise à jour initiale
        updateEnamelDependentValidation(form, formType);
    }
}

/**
 * Mettre à jour la validation dépendante du format
 */
function updateFormatDependentValidation(form, formType) {
    const formatSelect = form.querySelector('[name="format_type"]');
    const format = formatSelect ? formatSelect.value : null;
    
    if (!format) return;
    
    // Mettre à jour la validation d'épaisseur et de poids pour les contrôles de presse
    if (formType === 'press') {
        updatePressValidation(form, format);
    }
    
    // Mettre à jour la validation de grammage pour les contrôles d'émail
    if (formType === 'enamel') {
        updateGrammageValidation(form, format);
    }
}

/**
 * Mettre à jour la validation de presse selon le format
 */
function updatePressValidation(form, format) {
    const specs = SPECIFICATIONS.press;
    
    // Mettre à jour la validation d'épaisseur
    const thicknessInput = form.querySelector('[name="thickness"]');
    if (thicknessInput && specs.thickness[format]) {
        const thicknessSpec = specs.thickness[format];
        thicknessInput.setAttribute('data-min', thicknessSpec.min);
        thicknessInput.setAttribute('data-max', thicknessSpec.max);
        thicknessInput.placeholder = `${thicknessSpec.min} - ${thicknessSpec.max} ${thicknessSpec.unit}`;
        
        // Mettre à jour le texte d'aide
        const helpText = form.querySelector('#thicknessSpec');
        if (helpText) {
            helpText.textContent = `Spéc : ${thicknessSpec.min} - ${thicknessSpec.max} ${thicknessSpec.unit}`;
        }
        
        // Re-valider s'il y a une valeur
        if (thicknessInput.value) {
            validateInput(thicknessInput, thicknessSpec);
        }
    }
    
    // Mettre à jour la validation de poids
    const weightInput = form.querySelector('[name="wet_weight"]');
    if (weightInput && specs.weight[format]) {
        const weightSpec = specs.weight[format];
        weightInput.setAttribute('data-min', weightSpec.min);
        weightInput.setAttribute('data-max', weightSpec.max);
        weightInput.placeholder = `${weightSpec.min} - ${weightSpec.max} ${weightSpec.unit}`;
        
        // Mettre à jour le texte d'aide
        const helpText = form.querySelector('#weightSpec');
        if (helpText) {
            helpText.textContent = `Spéc : ${weightSpec.min} - ${weightSpec.max} ${weightSpec.unit}`;
        }
        
        // Re-valider s'il y a une valeur
        if (weightInput.value) {
            validateInput(weightInput, weightSpec);
        }
    }
}

/**
 * Mettre à jour la validation d'émail selon le type
 */
function updateEnamelDependentValidation(form, formType) {
    const enamelSelect = form.querySelector('[name="enamel_type"]');
    const enamelType = enamelSelect ? enamelSelect.value : null;
    
    if (!enamelType) return;
    
    const specs = SPECIFICATIONS.enamel;
    
    // Mettre à jour la validation de densité
    const densityInput = form.querySelector('[name="density"]');
    if (densityInput && specs.density[enamelType]) {
        const densitySpec = specs.density[enamelType];
        densityInput.setAttribute('data-min', densitySpec.min);
        densityInput.setAttribute('data-max', densitySpec.max);
        densityInput.placeholder = `${densitySpec.min} - ${densitySpec.max} ${densitySpec.unit}`;
        
        // Mettre à jour le texte d'aide
        const helpText = form.querySelector('#densitySpec');
        if (helpText) {
            helpText.textContent = `Spéc : ${densitySpec.min} - ${densitySpec.max} ${densitySpec.unit}`;
        }
        
        // Re-valider s'il y a une valeur
        if (densityInput.value) {
            validateInput(densityInput, densitySpec);
        }
    }
}

/**
 * Mettre à jour la validation de grammage selon le format
 */
function updateGrammageValidation(form, format) {
    const specs = SPECIFICATIONS.enamel.grammage;
    
    // Mettre à jour le grammage d'eau
    const waterInput = form.querySelector('[name="water_grammage"]');
    if (waterInput && specs.water[format]) {
        const waterSpec = specs.water[format];
        waterInput.setAttribute('data-min', waterSpec.min);
        waterInput.setAttribute('data-max', waterSpec.max);
        waterInput.placeholder = `${waterSpec.min} - ${waterSpec.max} ${waterSpec.unit}`;
        
        // Mettre à jour le texte d'aide
        const helpText = form.querySelector('#waterSpec');
        if (helpText) {
            helpText.textContent = `Spéc : ${waterSpec.min} - ${waterSpec.max} ${waterSpec.unit}`;
        }
    }
    
    // Mettre à jour le grammage d'émail
    const enamelInput = form.querySelector('[name="enamel_grammage"]');
    if (enamelInput && specs.enamel[format]) {
        const enamelSpec = specs.enamel[format];
        enamelInput.setAttribute('data-min', enamelSpec.min);
        enamelInput.setAttribute('data-max', enamelSpec.max);
        enamelInput.placeholder = `${enamelSpec.min} - ${enamelSpec.max} ${enamelSpec.unit}`;
        
        // Mettre à jour le texte d'aide
        const helpText = form.querySelector('#enamelSpec');
        if (helpText) {
            helpText.textContent = `Spéc : ${enamelSpec.min} - ${enamelSpec.max} ${enamelSpec.unit}`;
        }
    }
}

/**
 * Valider le formulaire entier
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
 * Afficher le résumé de validation
 */
function showValidationSummary(form) {
    const invalidInputs = form.querySelectorAll('.is-invalid');
    
    if (invalidInputs.length === 0) return;
    
    let message = `Veuillez corriger les ${invalidInputs.length} erreur(s) suivante(s) :\n\n`;
    
    invalidInputs.forEach((input, index) => {
        const label = form.querySelector(`label[for="${input.id}"]`) || 
                     form.querySelector(`label[for="${input.name}"]`);
        const labelText = label ? label.textContent : input.name;
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        const errorText = feedback ? feedback.textContent : 'Valeur invalide';
        
        message += `${index + 1}. ${labelText} : ${errorText}\n`;
    });
    
    alert(message);
    
    // Focaliser sur la première saisie invalide
    invalidInputs[0].focus();
}

/**
 * Indicateur de conformité en temps réel
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
        indicator.textContent = 'Aucune donnée saisie';
        indicator.className = 'compliance-indicator partial';
        return;
    }
    
    const complianceRate = (validInputs / totalInputs) * 100;
    
    if (complianceRate === 100) {
        indicator.textContent = 'Tous les paramètres sont conformes';
        indicator.className = 'compliance-indicator compliant';
    } else if (complianceRate === 0) {
        indicator.textContent = 'Mesures non conformes détectées';
        indicator.className = 'compliance-indicator non-compliant';
    } else {
        indicator.textContent = `${validInputs}/${totalInputs} paramètres conformes`;
        indicator.className = 'compliance-indicator partial';
    }
}

/**
 * Initialiser le calcul de qualité de surface pour les tests dimensionnels
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
                qualityIndicator.textContent = `${percentage.toFixed(1)}% sans défaut`;
                qualityIndicator.className = `badge ${isCompliant ? 'bg-success' : 'bg-danger'}`;
            }
            
            // Valider la saisie sans défaut
            defectFreeInput.classList.remove('is-valid', 'is-invalid');
            if (defectFree <= total) {
                defectFreeInput.classList.add(isCompliant ? 'is-valid' : 'is-invalid');
            }
        }
    }
    
    tilesTestedInput.addEventListener('input', updateSurfaceQuality);
    defectFreeInput.addEventListener('input', updateSurfaceQuality);
}

// Exporter les fonctions de validation
window.CeramicQCValidation = {
    initializeValidation,
    validateInput,
    validateForm,
    updateComplianceIndicator,
    SPECIFICATIONS
};

// Auto-initialiser la validation pour les formulaires avec des IDs spécifiques
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