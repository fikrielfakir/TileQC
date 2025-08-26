from models import Specification
from app import db

def initialize_default_specifications(control_type=None):
    """Initialize default specifications for quality control parameters"""
    
    default_specs = {
        'clay': [
            {'parameter_name': 'humidity_before_prep', 'min_value': 2.5, 'max_value': 4.1, 'target_value': 3.3, 'unit': '%', 'description': 'Humidity before preparation'},
            {'parameter_name': 'humidity_after_sieving', 'min_value': 2.0, 'max_value': 3.5, 'target_value': 2.75, 'unit': '%', 'description': 'Humidity after sieving'},
            {'parameter_name': 'humidity_after_prep', 'min_value': 5.3, 'max_value': 6.3, 'target_value': 5.8, 'unit': '%', 'description': 'Humidity after preparation'},
            {'parameter_name': 'granulometry_refusal', 'min_value': 10, 'max_value': 20, 'target_value': 15, 'unit': '%', 'description': 'Granulometry refusal percentage'},
            {'parameter_name': 'calcium_carbonate', 'min_value': 15, 'max_value': 25, 'target_value': 20, 'unit': '%', 'description': 'Calcium carbonate content'},
        ],
        
        'press': [
            # Thickness specs by format
            {'parameter_name': 'thickness', 'format_type': '20x20', 'min_value': 6.2, 'max_value': 7.2, 'target_value': 6.7, 'unit': 'mm', 'description': 'Thickness for 20x20 format'},
            {'parameter_name': 'thickness', 'format_type': '25x40', 'min_value': 6.8, 'max_value': 7.4, 'target_value': 7.1, 'unit': 'mm', 'description': 'Thickness for 25x40 format'},
            {'parameter_name': 'thickness', 'format_type': '25x50', 'min_value': 7.1, 'max_value': 7.7, 'target_value': 7.4, 'unit': 'mm', 'description': 'Thickness for 25x50 format'},
            
            # Weight specs by format
            {'parameter_name': 'wet_weight', 'format_type': '20x20', 'min_value': 480, 'max_value': 580, 'target_value': 530, 'unit': 'g', 'description': 'Wet weight for 20x20 format'},
            {'parameter_name': 'wet_weight', 'format_type': '25x40', 'min_value': 1150, 'max_value': 1550, 'target_value': 1350, 'unit': 'g', 'description': 'Wet weight for 25x40 format'},
            {'parameter_name': 'wet_weight', 'format_type': '25x50', 'min_value': 1800, 'max_value': 2000, 'target_value': 1900, 'unit': 'g', 'description': 'Wet weight for 25x50 format'},
            
            # Defect limits
            {'parameter_name': 'defect_grains', 'max_value': 15.0, 'target_value': 7.5, 'unit': '%', 'description': 'Maximum grains defects'},
            {'parameter_name': 'defect_cracks', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cracks defects'},
            {'parameter_name': 'defect_cleaning', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cleaning defects'},
            {'parameter_name': 'defect_foliage', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum foliage defects'},
            {'parameter_name': 'defect_chipping', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum chipping defects'},
        ],
        
        'dryer': [
            {'parameter_name': 'residual_humidity', 'min_value': 0.1, 'max_value': 1.5, 'target_value': 0.8, 'unit': '%', 'description': 'Residual humidity after drying'},
            # Same defect limits as press
            {'parameter_name': 'defect_grains', 'max_value': 15.0, 'target_value': 7.5, 'unit': '%', 'description': 'Maximum grains defects'},
            {'parameter_name': 'defect_cracks', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cracks defects'},
            {'parameter_name': 'defect_cleaning', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cleaning defects'},
            {'parameter_name': 'defect_foliage', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum foliage defects'},
            {'parameter_name': 'defect_chipping', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum chipping defects'},
        ],
        
        'biscuit_kiln': [
            {'parameter_name': 'defect_cracks', 'max_value': 5.0, 'target_value': 2.5, 'unit': '%', 'description': 'Maximum cracks defects in biscuit'},
            {'parameter_name': 'defect_chipping', 'max_value': 5.0, 'target_value': 2.5, 'unit': '%', 'description': 'Maximum chipping defects in biscuit'},
            {'parameter_name': 'defect_cooking', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cooking defects'},
            {'parameter_name': 'defect_foliage', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum foliage defects'},
            {'parameter_name': 'defect_flatness', 'max_value': 5.0, 'target_value': 2.5, 'unit': '%', 'description': 'Maximum flatness defects'},
            {'parameter_name': 'shrinkage_expansion', 'min_value': -0.2, 'max_value': 0.4, 'target_value': 0.1, 'unit': '%', 'description': 'Shrinkage/expansion range'},
            {'parameter_name': 'fire_loss', 'min_value': 10, 'max_value': 19, 'target_value': 14.5, 'unit': '%', 'description': 'Fire loss percentage'},
        ],
        
        'email_kiln': [
            {'parameter_name': 'thermal_shock', 'max_value': 5.0, 'target_value': 2.5, 'unit': '%', 'description': 'Maximum thermal shock defects'},
            {'parameter_name': 'rupture_resistance_thick', 'min_value': 600, 'unit': 'N', 'description': 'Rupture resistance for thickness >=7.5mm'},
            {'parameter_name': 'rupture_resistance_thin', 'min_value': 200, 'unit': 'N', 'description': 'Rupture resistance for thickness <7.5mm'},
            {'parameter_name': 'rupture_module_thick', 'min_value': 12, 'unit': 'N/mm²', 'description': 'Rupture module for thickness >=7.5mm'},
            {'parameter_name': 'rupture_module_thin', 'min_value': 15, 'unit': 'N/mm²', 'description': 'Rupture module for thickness <7.5mm'},
            {'parameter_name': 'length_deviation', 'min_value': -0.5, 'max_value': 0.5, 'target_value': 0, 'unit': '%', 'description': 'Length deviation tolerance'},
            {'parameter_name': 'width_deviation', 'min_value': -0.5, 'max_value': 0.5, 'target_value': 0, 'unit': '%', 'description': 'Width deviation tolerance'},
            {'parameter_name': 'thickness_deviation', 'min_value': -10, 'max_value': 10, 'target_value': 0, 'unit': '%', 'description': 'Thickness deviation tolerance'},
            {'parameter_name': 'water_absorption', 'min_value': 9.0, 'target_value': 12, 'unit': '%', 'description': 'Water absorption minimum'},
            {'parameter_name': 'color_nuance', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum color nuance defects'},
            {'parameter_name': 'cooking_defects', 'max_value': 1.0, 'target_value': 0.5, 'unit': '%', 'description': 'Maximum cooking defects'},
            {'parameter_name': 'flatness_defects', 'max_value': 5.0, 'target_value': 2.5, 'unit': '%', 'description': 'Maximum flatness defects'},
        ],
        
        'dimensional': [
            {'parameter_name': 'central_curvature', 'min_value': -2.0, 'max_value': 2.0, 'target_value': 0, 'unit': 'mm', 'description': 'Central curvature tolerance'},
            {'parameter_name': 'veil', 'min_value': -2.0, 'max_value': 2.0, 'target_value': 0, 'unit': 'mm', 'description': 'Veil tolerance'},
            {'parameter_name': 'angularity', 'min_value': -2.0, 'max_value': 2.0, 'target_value': 0, 'unit': 'mm', 'description': 'Angularity tolerance'},
            {'parameter_name': 'edge_straightness', 'min_value': -1.5, 'max_value': 1.5, 'target_value': 0, 'unit': 'mm', 'description': 'Edge straightness tolerance'},
            {'parameter_name': 'lateral_curvature', 'min_value': -2.0, 'max_value': 2.0, 'target_value': 0, 'unit': 'mm', 'description': 'Lateral curvature tolerance'},
            {'parameter_name': 'surface_quality', 'min_value': 95.0, 'target_value': 98, 'unit': '%', 'description': 'Minimum surface quality (defect-free)'},
            {'parameter_name': 'tiles_tested', 'min_value': 30, 'target_value': 50, 'unit': 'pieces', 'description': 'Minimum tiles to test'},
            {'parameter_name': 'surface_area_tested', 'min_value': 1.0, 'target_value': 2, 'unit': 'm²', 'description': 'Minimum surface area to test'},
            {'parameter_name': 'lighting_level', 'min_value': 300, 'target_value': 500, 'unit': 'lux', 'description': 'Minimum lighting level'},
        ],
        
        'enamel': [
            # Density by enamel type
            {'parameter_name': 'density', 'enamel_type': 'engobe', 'min_value': 1780, 'max_value': 1830, 'target_value': 1805, 'unit': 'g/l', 'description': 'Density for engobe'},
            {'parameter_name': 'density', 'enamel_type': 'email', 'min_value': 1730, 'max_value': 1780, 'target_value': 1755, 'unit': 'g/l', 'description': 'Density for email'},
            {'parameter_name': 'density', 'enamel_type': 'mate', 'min_value': 1780, 'max_value': 1830, 'target_value': 1805, 'unit': 'g/l', 'description': 'Density for mate'},
            
            # Viscosity (common for all types)
            {'parameter_name': 'viscosity', 'min_value': 25, 'max_value': 55, 'target_value': 40, 'unit': 'seconds', 'description': 'Viscosity range for all enamel types'},
            
            # Water grammage by format
            {'parameter_name': 'water_grammage', 'format_type': '20x20', 'min_value': 0.5, 'max_value': 3, 'target_value': 1.75, 'unit': 'g', 'description': 'Water grammage for 20x20'},
            {'parameter_name': 'water_grammage', 'format_type': '25x40', 'min_value': 1, 'max_value': 5, 'target_value': 3, 'unit': 'g', 'description': 'Water grammage for 25x40'},
            {'parameter_name': 'water_grammage', 'format_type': '25x50', 'min_value': 3, 'max_value': 7, 'target_value': 5, 'unit': 'g', 'description': 'Water grammage for 25x50'},
            
            # Enamel grammage by format and type
            {'parameter_name': 'enamel_grammage', 'format_type': '20x20', 'enamel_type': 'engobe', 'min_value': 20, 'max_value': 23, 'target_value': 21.5, 'unit': 'g', 'description': 'Engobe grammage for 20x20'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x40', 'enamel_type': 'engobe', 'min_value': 50, 'max_value': 55, 'target_value': 52.5, 'unit': 'g', 'description': 'Engobe grammage for 25x40'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x50', 'enamel_type': 'engobe', 'min_value': 70, 'max_value': 75, 'target_value': 72.5, 'unit': 'g', 'description': 'Engobe grammage for 25x50'},
            
            {'parameter_name': 'enamel_grammage', 'format_type': '20x20', 'enamel_type': 'email', 'min_value': 20, 'max_value': 23, 'target_value': 21.5, 'unit': 'g', 'description': 'Email grammage for 20x20'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x40', 'enamel_type': 'email', 'min_value': 50, 'max_value': 55, 'target_value': 52.5, 'unit': 'g', 'description': 'Email grammage for 25x40'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x50', 'enamel_type': 'email', 'min_value': 70, 'max_value': 75, 'target_value': 72.5, 'unit': 'g', 'description': 'Email grammage for 25x50'},
            
            {'parameter_name': 'enamel_grammage', 'format_type': '20x20', 'enamel_type': 'mate', 'min_value': 20, 'max_value': 23, 'target_value': 21.5, 'unit': 'g', 'description': 'Mate grammage for 20x20'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x40', 'enamel_type': 'mate', 'min_value': 50, 'max_value': 55, 'target_value': 52.5, 'unit': 'g', 'description': 'Mate grammage for 25x40'},
            {'parameter_name': 'enamel_grammage', 'format_type': '25x50', 'enamel_type': 'mate', 'min_value': 70, 'max_value': 75, 'target_value': 72.5, 'unit': 'g', 'description': 'Mate grammage for 25x50'},
        ]
    }
    
    if control_type and control_type not in default_specs:
        return 0
    
    control_types = [control_type] if control_type else default_specs.keys()
    created_count = 0
    
    for ct in control_types:
        for spec_data in default_specs[ct]:
            # Check if specification already exists
            existing = Specification.query.filter(
                Specification.control_type == ct,
                Specification.parameter_name == spec_data['parameter_name'],
                Specification.format_type == spec_data.get('format_type'),
                Specification.enamel_type == spec_data.get('enamel_type')
            ).first()
            
            if not existing:
                spec = Specification()
                spec.control_type = ct
                spec.parameter_name = spec_data['parameter_name']
                spec.format_type = spec_data.get('format_type')
                spec.enamel_type = spec_data.get('enamel_type')
                spec.min_value = spec_data.get('min_value')
                spec.max_value = spec_data.get('max_value')
                spec.target_value = spec_data.get('target_value')
                spec.unit = spec_data['unit']
                spec.description = spec_data['description']
                spec.is_active = True
                db.session.add(spec)
                created_count += 1
    
    try:
        db.session.commit()
        return created_count
    except Exception as e:
        db.session.rollback()
        print(f"Error creating specifications: {e}")
        return 0