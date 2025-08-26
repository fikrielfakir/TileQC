from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms import PressControlForm, PressThicknessForm, PressWetWeightForm, PressAspectForm, PressClayHumidityForm, CombinedPressForm
from models import PressControl
from app import db

press_bp = Blueprint('press', __name__)

@press_bp.route('/')
@login_required
def press_controls():
    page = request.args.get('page', 1, type=int)
    format_filter = request.args.get('format')
    
    query = PressControl.query
    if format_filter:
        query = query.filter(PressControl.format_type == format_filter)
    
    controls = query.order_by(PressControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('press/press_control.html', controls=controls, format_filter=format_filter)

@press_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_press_control():
    form = PressControlForm()
    
    if form.validate_on_submit():
        press_control = PressControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            measurement_time=form.measurement_time.data,
            format_type=form.format_type.data,
            thickness=form.thickness.data,
            wet_weight=form.wet_weight.data,
            weight_output_1=form.weight_output_1.data,
            weight_output_2=form.weight_output_2.data,
            defect_grains=form.defect_grains.data,
            defect_cracks=form.defect_cracks.data,
            defect_cleaning=form.defect_cleaning.data,
            defect_foliage=form.defect_foliage.data,
            defect_chipping=form.defect_chipping.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Enregistrement du contrôle presse ajouté avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_control.html', form=form)

@press_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_press_control(id):
    press_control = PressControl.query.get_or_404(id)
    form = PressControlForm(obj=press_control)
    
    if form.validate_on_submit():
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.measurement_number = form.measurement_number.data
        press_control.measurement_time = form.measurement_time.data
        press_control.format_type = form.format_type.data
        press_control.thickness = form.thickness.data
        press_control.wet_weight = form.wet_weight.data
        press_control.weight_output_1 = form.weight_output_1.data
        press_control.weight_output_2 = form.weight_output_2.data
        press_control.defect_grains = form.defect_grains.data
        press_control.defect_cracks = form.defect_cracks.data
        press_control.defect_cleaning = form.defect_cleaning.data
        press_control.defect_foliage = form.defect_foliage.data
        press_control.defect_chipping = form.defect_chipping.data
        press_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du contrôle presse mis à jour avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_control.html', form=form, edit=True, control=press_control)

@press_bp.route('/api/specifications/<format_type>')
@login_required
def get_specifications(format_type):
    specs = {
        '20x20': {'thickness': [6.2, 7.2], 'weight': [480, 580]},
        '25x40': {'thickness': [6.8, 7.4], 'weight': [1150, 1550]},
        '25x50': {'thickness': [7.1, 7.7], 'weight': [1800, 2000]}
    }
    
    return jsonify(specs.get(format_type, {}))

# Individual Press Control Routes as requested by user
@press_bp.route('/thickness', methods=['GET', 'POST'])
@login_required
def press_thickness():
    form = PressThicknessForm()
    
    if form.validate_on_submit():
        press_control = PressControl()
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.measurement_time = form.measurement_time.data
        press_control.format_type = form.format_type.data
        press_control.thickness = form.thickness.data
        press_control.notes = form.notes.data
        press_control.controller_id = current_user.id
        
        # Check compliance based on format
        compliance_status = 'compliant'
        thickness_value = form.thickness.data
        format_type = form.format_type.data
        
        if format_type == '20x20' and not (6.2 <= thickness_value <= 7.2):
            compliance_status = 'non_compliant'
        elif format_type == '25x40' and not (6.8 <= thickness_value <= 7.4):
            compliance_status = 'non_compliant'
        elif format_type == '25x50' and not (7.1 <= thickness_value <= 7.7):
            compliance_status = 'non_compliant'
        
        press_control.compliance_status = compliance_status
        
        if compliance_status == 'non_compliant':
            flash(f'⚠️ Épaisseur hors spécification ({thickness_value}mm) - Format {format_type}', 'warning')
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Contrôle épaisseur enregistré avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_thickness.html', form=form)

@press_bp.route('/wet-weight', methods=['GET', 'POST'])
@login_required
def press_wet_weight():
    form = PressWetWeightForm()
    
    if form.validate_on_submit():
        press_control = PressControl()
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.measurement_time = form.measurement_time.data
        press_control.format_type = form.format_type.data
        press_control.wet_weight = form.wet_weight.data
        press_control.notes = form.notes.data
        press_control.controller_id = current_user.id
        
        # Check compliance based on format
        compliance_status = 'compliant'
        weight_value = form.wet_weight.data
        format_type = form.format_type.data
        
        if format_type == '20x20' and not (480 <= weight_value <= 580):
            compliance_status = 'non_compliant'
        elif format_type == '25x40' and not (1150 <= weight_value <= 1550):
            compliance_status = 'non_compliant'
        elif format_type == '25x50' and not (1800 <= weight_value <= 2000):
            compliance_status = 'non_compliant'
        
        press_control.compliance_status = compliance_status
        
        if compliance_status == 'non_compliant':
            flash(f'⚠️ Poids hors spécification ({weight_value}g) - Format {format_type}', 'warning')
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Contrôle poids humide enregistré avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_wet_weight.html', form=form)

@press_bp.route('/aspect', methods=['GET', 'POST'])
@login_required
def press_aspect():
    form = PressAspectForm()
    
    if form.validate_on_submit():
        press_control = PressControl()
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.measurement_time = form.measurement_time.data
        press_control.defect_grains = form.defect_grains.data
        press_control.defect_cracks = form.defect_cracks.data
        press_control.defect_cleaning = form.defect_cleaning.data
        press_control.defect_foliage = form.defect_foliage.data
        press_control.defect_chipping = form.defect_chipping.data
        press_control.notes = form.notes.data
        press_control.controller_id = current_user.id
        
        # Check compliance for aspect defects
        compliance_issues = []
        if form.defect_grains.data > 15:
            compliance_issues.append(f'Grains ({form.defect_grains.data}%) > 15%')
        if form.defect_cracks.data > 1:
            compliance_issues.append(f'Fissures ({form.defect_cracks.data}%) > 1%')
        if form.defect_cleaning.data > 1:
            compliance_issues.append(f'Nettoyage ({form.defect_cleaning.data}%) > 1%')
        if form.defect_foliage.data > 1:
            compliance_issues.append(f'Feuillage ({form.defect_foliage.data}%) > 1%')
        if form.defect_chipping.data > 1:
            compliance_issues.append(f'Écornage ({form.defect_chipping.data}%) > 1%')
        
        press_control.compliance_status = 'non_compliant' if compliance_issues else 'compliant'
        
        if compliance_issues:
            flash(f'⚠️ Défauts hors spécification: {", ".join(compliance_issues)}', 'warning')
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Contrôle aspect enregistré avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_aspect.html', form=form)

@press_bp.route('/clay-humidity', methods=['GET', 'POST'])
@login_required
def press_clay_humidity():
    form = PressClayHumidityForm()
    
    if form.validate_on_submit():
        press_control = PressControl()
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.measurement_time = form.measurement_time.data
        press_control.clay_humidity = form.clay_humidity.data
        press_control.notes = form.notes.data
        press_control.controller_id = current_user.id
        
        # Check compliance for clay humidity (5.2% ≤ H ≤ 6%)
        humidity_value = form.clay_humidity.data
        if not (5.2 <= humidity_value <= 6.0):
            press_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Humidité argile hors spécification ({humidity_value}%) - Spéc: 5.2%-6%', 'warning')
        else:
            press_control.compliance_status = 'compliant'
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Contrôle humidité argile presse enregistré avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/press_clay_humidity.html', form=form)

@press_bp.route('/combined-press', methods=['GET', 'POST'])
@login_required
def combined_press():
    form = CombinedPressForm()
    
    if form.validate_on_submit():
        press_control = PressControl()
        press_control.date = form.date.data
        press_control.shift = form.shift.data
        press_control.format_type = form.format_type.data
        press_control.thickness = form.thickness.data
        press_control.wet_weight = form.wet_weight.data
        press_control.notes = form.notes.data
        press_control.controller_id = current_user.id
        
        # Check compliance for both thickness and weight
        compliance_issues = []
        format_type = form.format_type.data
        
        # Check thickness compliance
        if form.thickness.data:
            thickness_value = form.thickness.data
            if format_type == '20x20' and not (6.2 <= thickness_value <= 7.2):
                compliance_issues.append(f'Épaisseur ({thickness_value}mm)')
            elif format_type == '25x40' and not (6.8 <= thickness_value <= 7.4):
                compliance_issues.append(f'Épaisseur ({thickness_value}mm)')
            elif format_type == '25x50' and not (7.1 <= thickness_value <= 7.7):
                compliance_issues.append(f'Épaisseur ({thickness_value}mm)')
        
        # Check weight compliance
        if form.wet_weight.data:
            weight_value = form.wet_weight.data
            if format_type == '20x20' and not (480 <= weight_value <= 580):
                compliance_issues.append(f'Poids ({weight_value}g)')
            elif format_type == '25x40' and not (1150 <= weight_value <= 1550):
                compliance_issues.append(f'Poids ({weight_value}g)')
            elif format_type == '25x50' and not (1800 <= weight_value <= 2000):
                compliance_issues.append(f'Poids ({weight_value}g)')
        
        press_control.compliance_status = 'non_compliant' if compliance_issues else 'compliant'
        
        if compliance_issues:
            flash(f'⚠️ Valeurs hors spécification: {", ".join(compliance_issues)} - Format {format_type}', 'warning')
        
        db.session.add(press_control)
        db.session.commit()
        
        flash('Contrôles presse combinés enregistrés avec succès', 'success')
        return redirect(url_for('press.press_controls'))
    
    return render_template('press/combined_press.html', form=form)
