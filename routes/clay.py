from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms import ClayControlForm, HumidityBeforePrepForm, HumidityAfterSievingForm, HumidityAfterPrepForm, GranulometryForm, CalciumCarbonateForm, R2F1LaboForm
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

# Separate routes for each clay sub-control

@clay_bp.route('/humidity-before-prep', methods=['GET', 'POST'])
@login_required
def humidity_before_prep():
    form = HumidityBeforePrepForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time.data,
            humidity_before_prep=form.humidity_before_prep.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité trémie générale enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_before_prep.html', form=form)

@clay_bp.route('/humidity-after-sieving', methods=['GET', 'POST'])
@login_required
def humidity_after_sieving():
    form = HumidityAfterSievingForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time.data,
            humidity_after_sieving=form.humidity_after_sieving.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité après tamisage enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_after_sieving.html', form=form)

@clay_bp.route('/humidity-after-prep', methods=['GET', 'POST'])
@login_required
def humidity_after_prep():
    form = HumidityAfterPrepForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time.data,
            humidity_after_prep=form.humidity_after_prep.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité niveau silo enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_after_prep.html', form=form)

@clay_bp.route('/granulometry', methods=['GET', 'POST'])
@login_required
def granulometry():
    form = GranulometryForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time.data,
            granulometry_refusal=form.granulometry_refusal.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Granulométrie enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/granulometry.html', form=form)

@clay_bp.route('/calcium-carbonate', methods=['GET', 'POST'])
@login_required
def calcium_carbonate():
    form = CalciumCarbonateForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_time_1=form.measurement_time.data,
            calcium_carbonate=form.calcium_carbonate.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('% Chaux CaCO₃ enregistré avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/calcium_carbonate.html', form=form)

@clay_bp.route('/r2-f1-labo', methods=['GET', 'POST'])
@login_required
def r2_f1_labo_form():
    form = R2F1LaboForm()
    
    if form.validate_on_submit():
        # Create a comprehensive clay control record from the R2-F1-LABO form
        clay_control = ClayControl(
            date=form.date.data,
            measurement_time_1=form.measurement_time_1.data,
            measurement_time_2=form.measurement_time_2.data,
            humidity_before_prep=form.humidity_before_prep.data,
            humidity_after_sieving=form.humidity_after_sieving.data,
            humidity_after_prep=form.humidity_after_prep.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Fiche R2-F1-LABO enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/r2_f1_labo_form.html', form=form)

@clay_bp.route('/print-r2-f1-labo/<int:id>')
@login_required
def print_r2_f1_labo(id):
    clay_control = ClayControl.query.get_or_404(id)
    
    # Check if the record has the required humidity measurements for R2-F1-LABO
    if not (clay_control.humidity_before_prep and 
            clay_control.humidity_after_sieving and 
            clay_control.humidity_after_prep):
        flash('Ce contrôle ne contient pas toutes les mesures requises pour la fiche R2-F1-LABO', 'error')
        return redirect(url_for('clay.clay_controls'))
    
    # Create a form pre-filled with the data
    form = R2F1LaboForm()
    form.date.data = clay_control.date
    form.humidity_before_prep.data = clay_control.humidity_before_prep
    form.humidity_after_sieving.data = clay_control.humidity_after_sieving
    form.humidity_after_prep.data = clay_control.humidity_after_prep
    form.measurement_time_1.data = clay_control.measurement_time_1
    form.measurement_time_2.data = clay_control.measurement_time_2
    form.notes.data = clay_control.notes
    
    return render_template('clay/r2_f1_labo_print.html', form=form, control=clay_control)
