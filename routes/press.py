from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms import PressControlForm
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
