def validate_clay_control(clay_control):
    """Validate clay control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Check each parameter against database specifications
    parameters = {
        'humidity_before_prep': clay_control.humidity_before_prep,
        'humidity_after_sieving': clay_control.humidity_after_sieving,
        'humidity_after_prep': clay_control.humidity_after_prep,
        'granulometry_refusal': clay_control.granulometry_refusal,
        'calcium_carbonate': clay_control.calcium_carbonate
    }
    
    for param_name, value in parameters.items():
        if value is not None:
            spec = Specification.get_spec('clay', param_name)
            if spec and not _check_value_against_spec(value, spec):
                range_str = f"{spec.min_value or ''}-{spec.max_value or ''} {spec.unit}"
                issues.append(f"{param_name.replace('_', ' ').title()} out of spec ({range_str})")
    
    return "compliant" if not issues else "non_compliant"

def validate_press_control(press_control):
    """Validate press control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Check thickness and weight with format-specific specs
    if press_control.format_type:
        # Thickness validation
        if press_control.thickness is not None:
            spec = Specification.get_spec('press', 'thickness', format_type=press_control.format_type)
            if spec and not _check_value_against_spec(press_control.thickness, spec):
                range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
                issues.append(f"Thickness out of spec for {press_control.format_type} ({range_str})")
        
        # Weight validation
        if press_control.wet_weight is not None:
            spec = Specification.get_spec('press', 'wet_weight', format_type=press_control.format_type)
            if spec and not _check_value_against_spec(press_control.wet_weight, spec):
                range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
                issues.append(f"Weight out of spec for {press_control.format_type} ({range_str})")
    
    # Surface defect validation
    defect_parameters = {
        'defect_grains': press_control.defect_grains,
        'defect_cracks': press_control.defect_cracks,
        'defect_cleaning': press_control.defect_cleaning,
        'defect_foliage': press_control.defect_foliage,
        'defect_chipping': press_control.defect_chipping
    }
    
    for param_name, value in defect_parameters.items():
        if value is not None:
            spec = Specification.get_spec('press', param_name)
            if spec and not _check_value_against_spec(value, spec):
                issues.append(f"{param_name.replace('defect_', '').replace('_', ' ').title()} defects exceed limit ({spec.max_value}{spec.unit})")
    
    return "compliant" if not issues else "non_compliant"

def validate_dryer_control(dryer_control):
    """Validate dryer control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Residual humidity validation
    if dryer_control.residual_humidity is not None:
        spec = Specification.get_spec('dryer', 'residual_humidity')
        if spec and not _check_value_against_spec(dryer_control.residual_humidity, spec):
            range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
            issues.append(f"Residual humidity out of spec ({range_str})")
    
    # Surface defect validation
    defect_parameters = {
        'defect_grains': dryer_control.defect_grains,
        'defect_cracks': dryer_control.defect_cracks,
        'defect_cleaning': dryer_control.defect_cleaning,
        'defect_foliage': dryer_control.defect_foliage,
        'defect_chipping': dryer_control.defect_chipping
    }
    
    for param_name, value in defect_parameters.items():
        if value is not None:
            spec = Specification.get_spec('dryer', param_name)
            if spec and not _check_value_against_spec(value, spec):
                issues.append(f"{param_name.replace('defect_', '').replace('_', ' ').title()} defects exceed limit ({spec.max_value}{spec.unit})")
    
    return "compliant" if not issues else "non_compliant"

def validate_biscuit_kiln_control(biscuit_control):
    """Validate biscuit kiln control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Check all parameters against specifications
    parameters = {
        'defect_cracks': biscuit_control.defect_cracks,
        'defect_chipping': biscuit_control.defect_chipping,
        'defect_cooking': biscuit_control.defect_cooking,
        'defect_foliage': biscuit_control.defect_foliage,
        'defect_flatness': biscuit_control.defect_flatness,
        'shrinkage_expansion': biscuit_control.shrinkage_expansion,
        'fire_loss': biscuit_control.fire_loss
    }
    
    for param_name, value in parameters.items():
        if value is not None:
            spec = Specification.get_spec('biscuit_kiln', param_name)
            if spec and not _check_value_against_spec(value, spec):
                if param_name.startswith('defect_'):
                    display_name = param_name.replace('defect_', '').replace('_', ' ').title() + ' defects'
                    issues.append(f"{display_name} exceed limit ({spec.max_value}{spec.unit})")
                else:
                    range_str = f"{spec.min_value or ''}-{spec.max_value or ''} {spec.unit}"
                    issues.append(f"{param_name.replace('_', ' ').title()} out of spec ({range_str})")
    
    return "compliant" if not issues else "non_compliant"

def validate_email_kiln_control(email_control):
    """Validate email kiln control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Standard parameters
    standard_params = {
        'thermal_shock': email_control.thermal_shock,
        'length_deviation': email_control.length_deviation,
        'width_deviation': email_control.width_deviation,
        'thickness_deviation': email_control.thickness_deviation,
        'water_absorption': email_control.water_absorption,
        'color_nuance': email_control.color_nuance,
        'cooking_defects': email_control.cooking_defects,
        'flatness_defects': email_control.flatness_defects
    }
    
    for param_name, value in standard_params.items():
        if value is not None:
            spec = Specification.get_spec('email_kiln', param_name)
            if spec and not _check_value_against_spec(value, spec):
                range_str = f"{spec.min_value or ''}-{spec.max_value or ''} {spec.unit}"
                issues.append(f"{param_name.replace('_', ' ').title()} out of spec ({range_str})")
    
    # Thickness-dependent rupture validation
    if (email_control.rupture_resistance is not None and 
        email_control.thickness_for_resistance is not None):
        
        thickness_category = 'thick' if email_control.thickness_for_resistance >= 7.5 else 'thin'
        spec = Specification.get_spec('email_kiln', f'rupture_resistance_{thickness_category}')
        if spec and not _check_value_against_spec(email_control.rupture_resistance, spec):
            issues.append(f"Rupture resistance below spec (>={spec.min_value} {spec.unit} for thickness {'>=7.5mm' if thickness_category == 'thick' else '<7.5mm'})")
    
    if (email_control.rupture_module is not None and 
        email_control.thickness_for_resistance is not None):
        
        thickness_category = 'thick' if email_control.thickness_for_resistance >= 7.5 else 'thin'
        spec = Specification.get_spec('email_kiln', f'rupture_module_{thickness_category}')
        if spec and not _check_value_against_spec(email_control.rupture_module, spec):
            issues.append(f"Rupture module below spec (>={spec.min_value} {spec.unit} for thickness {'>=7.5mm' if thickness_category == 'thick' else '<7.5mm'})")
    
    return "compliant" if not issues else "non_compliant"

def validate_dimensional_test(dimensional_test):
    """Validate dimensional test measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Dimensional parameters
    dimensional_params = {
        'central_curvature': dimensional_test.central_curvature,
        'veil': dimensional_test.veil,
        'angularity': dimensional_test.angularity,
        'edge_straightness': dimensional_test.edge_straightness,
        'lateral_curvature': dimensional_test.lateral_curvature
    }
    
    for param_name, value in dimensional_params.items():
        if value is not None:
            spec = Specification.get_spec('dimensional', param_name)
            if spec and not _check_value_against_spec(abs(value), spec):  # Use absolute value for tolerance check
                issues.append(f"{param_name.replace('_', ' ').title()} out of tolerance (±{spec.max_value}{spec.unit})")
    
    # Surface quality validation
    if (dimensional_test.tiles_tested is not None and 
        dimensional_test.defect_free_tiles is not None):
        
        defect_free_percentage = (dimensional_test.defect_free_tiles / dimensional_test.tiles_tested) * 100
        spec = Specification.get_spec('dimensional', 'surface_quality')
        if spec and defect_free_percentage < spec.min_value:
            issues.append(f"Surface quality below requirement ({spec.min_value}% defect-free)")
    
    # Minimum requirement validations
    min_requirements = {
        'tiles_tested': dimensional_test.tiles_tested,
        'surface_area_tested': dimensional_test.surface_area_tested,
        'lighting_level': dimensional_test.lighting_level
    }
    
    for param_name, value in min_requirements.items():
        if value is not None:
            spec = Specification.get_spec('dimensional', param_name)
            if spec and value < spec.min_value:
                issues.append(f"Insufficient {param_name.replace('_', ' ')} (minimum {spec.min_value} {spec.unit})")
    
    return "compliant" if not issues else "non_compliant"

def validate_enamel_control(enamel_control):
    """Validate enamel control measurements against database specifications"""
    from models import Specification
    issues = []
    
    # Density validation (enamel-type specific)
    if enamel_control.density is not None and enamel_control.enamel_type:
        spec = Specification.get_spec('enamel', 'density', enamel_type=enamel_control.enamel_type)
        if spec and not _check_value_against_spec(enamel_control.density, spec):
            range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
            issues.append(f"Density out of spec for {enamel_control.enamel_type} ({range_str})")
    
    # Viscosity validation (common for all types)
    if enamel_control.viscosity is not None:
        spec = Specification.get_spec('enamel', 'viscosity')
        if spec and not _check_value_against_spec(enamel_control.viscosity, spec):
            range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
            issues.append(f"Viscosity out of spec ({range_str})")
    
    # Water grammage validation (format-specific)
    if enamel_control.water_grammage is not None and enamel_control.format_type:
        spec = Specification.get_spec('enamel', 'water_grammage', format_type=enamel_control.format_type)
        if spec and not _check_value_against_spec(enamel_control.water_grammage, spec):
            range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
            issues.append(f"Water grammage out of spec for {enamel_control.format_type} ({range_str})")
    
    # Enamel grammage validation (format and enamel-type specific)
    if (enamel_control.enamel_grammage is not None and 
        enamel_control.format_type and enamel_control.enamel_type):
        
        spec = Specification.get_spec('enamel', 'enamel_grammage', 
                                    format_type=enamel_control.format_type,
                                    enamel_type=enamel_control.enamel_type)
        if spec and not _check_value_against_spec(enamel_control.enamel_grammage, spec):
            range_str = f"{spec.min_value}-{spec.max_value} {spec.unit}"
            issues.append(f"{enamel_control.enamel_type.title()} grammage out of spec for {enamel_control.format_type} ({range_str})")
    
    return "compliant" if not issues else "non_compliant"

def validate_digital_decoration(digital_decoration):
    """Validate digital decoration measurements"""
    # Digital decoration is pass/fail, so if any parameter fails, overall fails
    if (digital_decoration.sharpness == 'fail' or 
        digital_decoration.offset == 'fail' or 
        digital_decoration.tonality == 'fail'):
        return "non_compliant"
    
    return "compliant"

def _check_value_against_spec(value, spec):
    """Check if a value meets specification requirements"""
    if spec.min_value is not None and value < spec.min_value:
        return False
    if spec.max_value is not None and value > spec.max_value:
        return False
    return True

def get_compliance_summary(model_class, date_range=None):
    """Get compliance summary for a model class"""
    from app import db
    
    query = model_class.query
    if date_range:
        start_date, end_date = date_range
        query = query.filter(model_class.date.between(start_date, end_date))
    
    total = query.count()
    compliant = query.filter(model_class.compliance_status == 'compliant').count()
    non_compliant = query.filter(model_class.compliance_status == 'non_compliant').count()
    
    compliance_rate = (compliant / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'compliant': compliant,
        'non_compliant': non_compliant,
        'compliance_rate': round(compliance_rate, 1)
    }