from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms import EnamelControlForm
from models import EnamelControl
from app import db

enamel_bp = Blueprint('enamel', __name__)

@enamel_bp.route('/')
@login_required
def enamel_controls():
    page = request.args.get('page', 1, type=int)
    enamel_filter = request.args.get('enamel_type')
    
    query = EnamelControl.query
    if enamel_filter:
        query = query.filter(EnamelControl.enamel_type == enamel_filter)
    
    controls = query.order_by(EnamelControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('enamel/enamel_control.html', controls=controls, enamel_filter=enamel_filter)

@enamel_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_enamel_control():
    form = EnamelControlForm()
    
    if form.validate_on_submit():
        enamel_control = EnamelControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_type=form.measurement_type.data,
            measurement_number=form.measurement_number.data,
            measurement_time=form.measurement_time.data,
            enamel_type=form.enamel_type.data,
            density=form.density.data,
            viscosity=form.viscosity.data,
            format_type=form.format_type.data,
            water_grammage=form.water_grammage.data,
            enamel_grammage=form.enamel_grammage.data,
            sieve_refusal=form.sieve_refusal.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(enamel_control)
        db.session.commit()
        
        flash('Enregistrement du contrôle émail ajouté avec succès', 'success')
        return redirect(url_for('enamel.enamel_controls'))
    
    return render_template('enamel/enamel_control.html', form=form)

@enamel_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_enamel_control(id):
    enamel_control = EnamelControl.query.get_or_404(id)
    form = EnamelControlForm(obj=enamel_control)
    
    if form.validate_on_submit():
        enamel_control.date = form.date.data
        enamel_control.shift = form.shift.data
        enamel_control.measurement_type = form.measurement_type.data
        enamel_control.measurement_number = form.measurement_number.data
        enamel_control.measurement_time = form.measurement_time.data
        enamel_control.enamel_type = form.enamel_type.data
        enamel_control.density = form.density.data
        enamel_control.viscosity = form.viscosity.data
        enamel_control.format_type = form.format_type.data
        enamel_control.water_grammage = form.water_grammage.data
        enamel_control.enamel_grammage = form.enamel_grammage.data
        enamel_control.sieve_refusal = form.sieve_refusal.data
        enamel_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du contrôle émail mis à jour avec succès', 'success')
        return redirect(url_for('enamel.enamel_controls'))
    
    return render_template('enamel/enamel_control.html', form=form, edit=True, control=enamel_control)

@enamel_bp.route('/api/specifications/<enamel_type>')
@login_required
def get_enamel_specifications(enamel_type):
    specs = {
        'engobe': {'density': [1780, 1830]},
        'email': {'density': [1730, 1780]},
        'mate': {'density': [1780, 1830]}
    }
    
    return jsonify(specs.get(enamel_type, {}))

@enamel_bp.route('/api/grammage/<format_type>')
@login_required
def get_grammage_specifications(format_type):
    specs = {
        '20x20': {'water': [0.5, 3], 'enamel': [20, 23]},
        '25x40': {'water': [1, 5], 'enamel': [50, 55]},
        '25x50': {'water': [3, 7], 'enamel': [70, 75]}
    }
    
    return jsonify(specs.get(format_type, {}))
