def validate_clay_control(clay_control):
    """Validate clay control measurements against specifications"""
    issues = []
    
    # Humidity before preparation: 2.5% ≤ H ≤ 4.1%
    if clay_control.humidity_before_prep is not None:
        if not (2.5 <= clay_control.humidity_before_prep <= 4.1):
            issues.append("Humidity before prep out of spec (2.5-4.1%)")
    
    # Humidity after sieving: 2% ≤ H ≤ 3.5%
    if clay_control.humidity_after_sieving is not None:
        if not (2.0 <= clay_control.humidity_after_sieving <= 3.5):
            issues.append("Humidity after sieving out of spec (2.0-3.5%)")
    
    # Humidity after preparation: 5.3% ≤ H ≤ 6.3%
    if clay_control.humidity_after_prep is not None:
        if not (5.3 <= clay_control.humidity_after_prep <= 6.3):
            issues.append("Humidity after prep out of spec (5.3-6.3%)")
    
    # Granulometry refusal: 10% ≤ Refus ≤ 20%
    if clay_control.granulometry_refusal is not None:
        if not (10 <= clay_control.granulometry_refusal <= 20):
            issues.append("Granulometry refusal out of spec (10-20%)")
    
    # Calcium carbonate: 15% ≤ CaCo3 ≤ 25%
    if clay_control.calcium_carbonate is not None:
        if not (15 <= clay_control.calcium_carbonate <= 25):
            issues.append("Calcium carbonate out of spec (15-25%)")
    
    return "compliant" if not issues else "non_compliant"

def validate_press_control(press_control):
    """Validate press control measurements against format-specific specifications"""
    issues = []
    
    format_specs = {
        '20x20': {'thickness': (6.2, 7.2), 'weight': (480, 580)},
        '25x40': {'thickness': (6.8, 7.4), 'weight': (1150, 1550)},
        '25x50': {'thickness': (7.1, 7.7), 'weight': (1800, 2000)}
    }
    
    if press_control.format_type in format_specs:
        spec = format_specs[press_control.format_type]
        
        # Thickness validation
        if press_control.thickness is not None:
            min_thick, max_thick = spec['thickness']
            if not (min_thick <= press_control.thickness <= max_thick):
                issues.append(f"Thickness out of spec for {press_control.format_type} ({min_thick}-{max_thick}mm)")
        
        # Weight validation
        if press_control.wet_weight is not None:
            min_weight, max_weight = spec['weight']
            if not (min_weight <= press_control.wet_weight <= max_weight):
                issues.append(f"Weight out of spec for {press_control.format_type} ({min_weight}-{max_weight}g)")
    
    # Surface defect validation
    defect_limits = {
        'grains': 15.0,
        'cracks': 1.0,
        'cleaning': 1.0,
        'foliage': 1.0,
        'chipping': 1.0
    }
    
    defects = {
        'grains': press_control.defect_grains,
        'cracks': press_control.defect_cracks,
        'cleaning': press_control.defect_cleaning,
        'foliage': press_control.defect_foliage,
        'chipping': press_control.defect_chipping
    }
    
    for defect_type, value in defects.items():
        if value is not None and value > defect_limits[defect_type]:
            issues.append(f"{defect_type.title()} defects exceed limit ({defect_limits[defect_type]}%)")
    
    return "compliant" if not issues else "non_compliant"

def validate_dryer_control(dryer_control):
    """Validate dryer control measurements"""
    issues = []
    
    # Residual humidity: 0.1% ≤ HR ≤ 1.5%
    if dryer_control.residual_humidity is not None:
        if not (0.1 <= dryer_control.residual_humidity <= 1.5):
            issues.append("Residual humidity out of spec (0.1-1.5%)")
    
    # Surface defects (same as press)
    defect_limits = {
        'grains': 15.0,
        'cracks': 1.0,
        'cleaning': 1.0,
        'foliage': 1.0,
        'chipping': 1.0
    }
    
    defects = {
        'grains': dryer_control.defect_grains,
        'cracks': dryer_control.defect_cracks,
        'cleaning': dryer_control.defect_cleaning,
        'foliage': dryer_control.defect_foliage,
        'chipping': dryer_control.defect_chipping
    }
    
    for defect_type, value in defects.items():
        if value is not None and value > defect_limits[defect_type]:
            issues.append(f"{defect_type.title()} defects exceed limit ({defect_limits[defect_type]}%)")
    
    return "compliant" if not issues else "non_compliant"

def validate_biscuit_kiln_control(biscuit_control):
    """Validate biscuit kiln control measurements"""
    issues = []
    
    # Defect percentages
    defect_limits = {
        'cracks': 5.0,
        'chipping': 5.0,
        'cooking': 1.0,
        'foliage': 1.0,
        'flatness': 5.0
    }
    
    defects = {
        'cracks': biscuit_control.defect_cracks,
        'chipping': biscuit_control.defect_chipping,
        'cooking': biscuit_control.defect_cooking,
        'foliage': biscuit_control.defect_foliage,
        'flatness': biscuit_control.defect_flatness
    }
    
    for defect_type, value in defects.items():
        if value is not None and value > defect_limits[defect_type]:
            issues.append(f"{defect_type.title()} defects exceed limit ({defect_limits[defect_type]}%)")
    
    # Shrinkage/expansion: -0.2% to +0.4%
    if biscuit_control.shrinkage_expansion is not None:
        if not (-0.2 <= biscuit_control.shrinkage_expansion <= 0.4):
            issues.append("Shrinkage/expansion out of spec (-0.2% to +0.4%)")
    
    # Fire loss: 10%-19%
    if biscuit_control.fire_loss is not None:
        if not (10 <= biscuit_control.fire_loss <= 19):
            issues.append("Fire loss out of spec (10-19%)")
    
    return "compliant" if not issues else "non_compliant"

def validate_email_kiln_control(email_control):
    """Validate email kiln control measurements"""
    issues = []
    
    # Thermal shock ≤ 5%
    if email_control.thermal_shock is not None and email_control.thermal_shock > 5.0:
        issues.append("Thermal shock exceeds limit (≤5%)")
    
    # Rupture resistance validation based on thickness
    if (email_control.rupture_resistance is not None and 
        email_control.thickness_for_resistance is not None):
        
        if email_control.thickness_for_resistance >= 7.5:
            if email_control.rupture_resistance < 600:
                issues.append("Rupture resistance below spec (≥600N for thickness ≥7.5mm)")
        else:
            if email_control.rupture_resistance < 200:
                issues.append("Rupture resistance below spec (≥200N for thickness <7.5mm)")
    
    # Rupture module validation based on thickness
    if (email_control.rupture_module is not None and 
        email_control.thickness_for_resistance is not None):
        
        if email_control.thickness_for_resistance >= 7.5:
            if email_control.rupture_module < 12:
                issues.append("Rupture module below spec (≥12 N/mm² for thickness ≥7.5mm)")
        else:
            if email_control.rupture_module < 15:
                issues.append("Rupture module below spec (≥15 N/mm² for thickness <7.5mm)")
    
    # Dimensional deviations
    if email_control.length_deviation is not None:
        if abs(email_control.length_deviation) > 0.5:
            issues.append("Length deviation out of spec (±0.5%)")
    
    if email_control.width_deviation is not None:
        if abs(email_control.width_deviation) > 0.5:
            issues.append("Width deviation out of spec (±0.5%)")
    
    if email_control.thickness_deviation is not None:
        if abs(email_control.thickness_deviation) > 10:
            issues.append("Thickness deviation out of spec (±10%)")
    
    # Water absorption: E>10% (individual minimum 9%)
    if email_control.water_absorption is not None:
        if email_control.water_absorption < 9.0:
            issues.append("Water absorption below minimum (individual min 9%)")
    
    # Quality parameters
    quality_limits = {
        'color_nuance': 1.0,
        'cooking_defects': 1.0,
        'flatness_defects': 5.0
    }
    
    quality_params = {
        'color_nuance': email_control.color_nuance,
        'cooking_defects': email_control.cooking_defects,
        'flatness_defects': email_control.flatness_defects
    }
    
    for param, value in quality_params.items():
        if value is not None and value > quality_limits[param]:
            issues.append(f"{param.replace('_', ' ').title()} exceeds limit ({quality_limits[param]}%)")
    
    return "compliant" if not issues else "non_compliant"

def validate_dimensional_test(dimensional_test):
    """Validate dimensional test measurements"""
    issues = []
    
    # Dimensional tolerances (±0.5% ±2mm except edge straightness)
    dimensional_limits = {
        'central_curvature': 2.0,
        'veil': 2.0,
        'angularity': 2.0,
        'edge_straightness': 1.5,  # ±0.3% ±1.5mm
        'lateral_curvature': 2.0
    }
    
    dimensions = {
        'central_curvature': dimensional_test.central_curvature,
        'veil': dimensional_test.veil,
        'angularity': dimensional_test.angularity,
        'edge_straightness': dimensional_test.edge_straightness,
        'lateral_curvature': dimensional_test.lateral_curvature
    }
    
    for dim, value in dimensions.items():
        if value is not None and abs(value) > dimensional_limits[dim]:
            issues.append(f"{dim.replace('_', ' ').title()} out of tolerance (±{dimensional_limits[dim]}mm)")
    
    # Surface quality: 95% tiles defect-free
    if (dimensional_test.tiles_tested is not None and 
        dimensional_test.defect_free_tiles is not None):
        
        defect_free_percentage = (dimensional_test.defect_free_tiles / dimensional_test.tiles_tested) * 100
        if defect_free_percentage < 95.0:
            issues.append("Surface quality below requirement (95% defect-free)")
    
    # Minimum testing requirements
    if dimensional_test.tiles_tested is not None and dimensional_test.tiles_tested < 30:
        issues.append("Insufficient tiles tested (minimum 30)")
    
    if dimensional_test.surface_area_tested is not None and dimensional_test.surface_area_tested < 1.0:
        issues.append("Insufficient surface area tested (minimum 1m²)")
    
    if dimensional_test.lighting_level is not None and dimensional_test.lighting_level < 300:
        issues.append("Insufficient lighting level (minimum 300 lux)")
    
    return "compliant" if not issues else "non_compliant"

def validate_enamel_control(enamel_control):
    """Validate enamel control measurements"""
    issues = []
    
    # Density specifications by enamel type
    density_specs = {
        'engobe': (1780, 1830),
        'email': (1730, 1780),
        'mate': (1780, 1830)
    }
    
    if (enamel_control.enamel_type in density_specs and 
        enamel_control.density is not None):
        
        min_density, max_density = density_specs[enamel_control.enamel_type]
        if not (min_density <= enamel_control.density <= max_density):
            issues.append(f"Density out of spec for {enamel_control.enamel_type} ({min_density}-{max_density} g/l)")
    
    # Viscosity: 25-55 seconds (all types)
    if enamel_control.viscosity is not None:
        if not (25 <= enamel_control.viscosity <= 55):
            issues.append("Viscosity out of spec (25-55 seconds)")
    
    # Grammage validation by format and type
    grammage_specs = {
        'water': {
            '20x20': (0.5, 3),
            '25x40': (1, 5),
            '25x50': (3, 7)
        },
        'engobe': {
            '20x20': (20, 23),
            '25x40': (50, 55),
            '25x50': (70, 75)
        },
        'email': {
            '20x20': (20, 23),
            '25x40': (50, 55),
            '25x50': (70, 75)
        },
        'mate': {
            '20x20': (20, 23),
            '25x40': (50, 55),
            '25x50': (70, 75)
        }
    }
    
    if (enamel_control.format_type and enamel_control.water_grammage is not None):
        water_spec = grammage_specs['water'].get(enamel_control.format_type)
        if water_spec:
            min_gram, max_gram = water_spec
            if not (min_gram <= enamel_control.water_grammage <= max_gram):
                issues.append(f"Water grammage out of spec for {enamel_control.format_type} ({min_gram}-{max_gram}g)")
    
    if (enamel_control.format_type and enamel_control.enamel_type and 
        enamel_control.enamel_grammage is not None and 
        enamel_control.enamel_type in grammage_specs):
        
        enamel_spec = grammage_specs[enamel_control.enamel_type].get(enamel_control.format_type)
        if enamel_spec:
            min_gram, max_gram = enamel_spec
            if not (min_gram <= enamel_control.enamel_grammage <= max_gram):
                issues.append(f"{enamel_control.enamel_type.title()} grammage out of spec for {enamel_control.format_type} ({min_gram}-{max_gram}g)")
    
    return "compliant" if not issues else "non_compliant"

def validate_digital_decoration(digital_decoration):
    """Validate digital decoration measurements"""
    # Digital decoration is pass/fail, so if any parameter fails, overall fails
    if (digital_decoration.sharpness == 'fail' or 
        digital_decoration.offset == 'fail' or 
        digital_decoration.tonality == 'fail'):
        return "non_compliant"
    
    return "compliant"

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
