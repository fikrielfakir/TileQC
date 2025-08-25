from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms import ClayControlForm
from models import ClayControl
from app import db
from datetime import date

clay_bp = Blueprint('clay', __name__)

@clay_bp.route('/')
@login_required
def clay_controls():
    page = request.args.get('page', 1, type=int)
    controls = ClayControl.query.order_by(ClayControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('clay/clay_control.html', controls=controls)

@clay_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_clay_control():
    form = ClayControlForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time_1.data,
            measurement_time_2=form.measurement_time_2.data,
            humidity_before_prep=form.humidity_before_prep.data,
            humidity_after_sieving=form.humidity_after_sieving.data,
            humidity_after_prep=form.humidity_after_prep.data,
            granulometry_refusal=form.granulometry_refusal.data,
            calcium_carbonate=form.calcium_carbonate.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Enregistrement du contrôle argile ajouté avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/clay_control.html', form=form)

@clay_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_clay_control(id):
    clay_control = ClayControl.query.get_or_404(id)
    form = ClayControlForm(obj=clay_control)
    
    if form.validate_on_submit():
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time_1.data
        clay_control.measurement_time_2 = form.measurement_time_2.data
        clay_control.humidity_before_prep = form.humidity_before_prep.data
        clay_control.humidity_after_sieving = form.humidity_after_sieving.data
        clay_control.humidity_after_prep = form.humidity_after_prep.data
        clay_control.granulometry_refusal = form.granulometry_refusal.data
        clay_control.calcium_carbonate = form.calcium_carbonate.data
        clay_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du contrôle argile mis à jour avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/clay_control.html', form=form, edit=True, control=clay_control)

@clay_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_clay_control(id):
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes', 'error')
        return redirect(url_for('clay.clay_controls'))
    
    clay_control = ClayControl.query.get_or_404(id)
    db.session.delete(clay_control)
    db.session.commit()
    
    flash('Enregistrement du contrôle argile supprimé avec succès', 'success')
    return redirect(url_for('clay.clay_controls'))

@clay_bp.route('/api/trend/<parameter>')
@login_required
def clay_trend_api(parameter):
    from utils.helpers import get_control_chart_data
    data = get_control_chart_data(ClayControl, parameter, days=30)
    return jsonify(data)
