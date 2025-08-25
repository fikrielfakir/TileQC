from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import BiscuitKilnForm, EmailKilnForm
from models import BiscuitKilnControl, EmailKilnControl
from app import db

kilns_bp = Blueprint('kilns', __name__)

@kilns_bp.route('/biscuit')
@login_required
def biscuit_kiln_controls():
    page = request.args.get('page', 1, type=int)
    controls = BiscuitKilnControl.query.order_by(BiscuitKilnControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('kilns/biscuit_kiln.html', controls=controls)

@kilns_bp.route('/biscuit/add', methods=['GET', 'POST'])
@login_required
def add_biscuit_control():
    form = BiscuitKilnForm()
    
    if form.validate_on_submit():
        biscuit_control = BiscuitKilnControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            defect_cracks=form.defect_cracks.data,
            defect_chipping=form.defect_chipping.data,
            defect_cooking=form.defect_cooking.data,
            defect_foliage=form.defect_foliage.data,
            defect_flatness=form.defect_flatness.data,
            thermal_shock=form.thermal_shock.data,
            shrinkage_expansion=form.shrinkage_expansion.data,
            fire_loss=form.fire_loss.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(biscuit_control)
        db.session.commit()
        
        flash('Biscuit kiln control record added successfully', 'success')
        return redirect(url_for('kilns.biscuit_kiln_controls'))
    
    return render_template('kilns/biscuit_kiln.html', form=form)

@kilns_bp.route('/email')
@login_required
def email_kiln_controls():
    page = request.args.get('page', 1, type=int)
    controls = EmailKilnControl.query.order_by(EmailKilnControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('kilns/email_kiln.html', controls=controls)

@kilns_bp.route('/email/add', methods=['GET', 'POST'])
@login_required
def add_email_control():
    form = EmailKilnForm()
    
    if form.validate_on_submit():
        email_control = EmailKilnControl(
            date=form.date.data,
            shift=form.shift.data,
            thermal_shock=form.thermal_shock.data,
            rupture_resistance=form.rupture_resistance.data,
            rupture_module=form.rupture_module.data,
            thickness_for_resistance=form.thickness_for_resistance.data,
            length_deviation=form.length_deviation.data,
            width_deviation=form.width_deviation.data,
            thickness_deviation=form.thickness_deviation.data,
            water_absorption=form.water_absorption.data,
            color_nuance=form.color_nuance.data,
            cooking_defects=form.cooking_defects.data,
            flatness_defects=form.flatness_defects.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(email_control)
        db.session.commit()
        
        flash('Email kiln control record added successfully', 'success')
        return redirect(url_for('kilns.email_kiln_controls'))
    
    return render_template('kilns/email_kiln.html', form=form)

@kilns_bp.route('/biscuit/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_biscuit_control(id):
    biscuit_control = BiscuitKilnControl.query.get_or_404(id)
    form = BiscuitKilnForm(obj=biscuit_control)
    
    if form.validate_on_submit():
        biscuit_control.date = form.date.data
        biscuit_control.shift = form.shift.data
        biscuit_control.measurement_number = form.measurement_number.data
        biscuit_control.defect_cracks = form.defect_cracks.data
        biscuit_control.defect_chipping = form.defect_chipping.data
        biscuit_control.defect_cooking = form.defect_cooking.data
        biscuit_control.defect_foliage = form.defect_foliage.data
        biscuit_control.defect_flatness = form.defect_flatness.data
        biscuit_control.thermal_shock = form.thermal_shock.data
        biscuit_control.shrinkage_expansion = form.shrinkage_expansion.data
        biscuit_control.fire_loss = form.fire_loss.data
        biscuit_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Biscuit kiln control record updated successfully', 'success')
        return redirect(url_for('kilns.biscuit_kiln_controls'))
    
    return render_template('kilns/biscuit_kiln.html', form=form, edit=True, control=biscuit_control)

@kilns_bp.route('/email/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_email_control(id):
    email_control = EmailKilnControl.query.get_or_404(id)
    form = EmailKilnForm(obj=email_control)
    
    if form.validate_on_submit():
        email_control.date = form.date.data
        email_control.shift = form.shift.data
        email_control.thermal_shock = form.thermal_shock.data
        email_control.rupture_resistance = form.rupture_resistance.data
        email_control.rupture_module = form.rupture_module.data
        email_control.thickness_for_resistance = form.thickness_for_resistance.data
        email_control.length_deviation = form.length_deviation.data
        email_control.width_deviation = form.width_deviation.data
        email_control.thickness_deviation = form.thickness_deviation.data
        email_control.water_absorption = form.water_absorption.data
        email_control.color_nuance = form.color_nuance.data
        email_control.cooking_defects = form.cooking_defects.data
        email_control.flatness_defects = form.flatness_defects.data
        email_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Email kiln control record updated successfully', 'success')
        return redirect(url_for('kilns.email_kiln_controls'))
    
    return render_template('kilns/email_kiln.html', form=form, edit=True, control=email_control)
