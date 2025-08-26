from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import DryerControlForm, DryerHumidityForm, DryerAspectForm
from models import DryerControl
from app import db

dryer_bp = Blueprint('dryer', __name__)

@dryer_bp.route('/')
@login_required
def dryer_controls():
    page = request.args.get('page', 1, type=int)
    controls = DryerControl.query.order_by(DryerControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('dryer/dryer_control.html', controls=controls)

@dryer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_dryer_control():
    form = DryerControlForm()
    
    if form.validate_on_submit():
        dryer_control = DryerControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            residual_humidity=form.residual_humidity.data,
            defect_grains=form.defect_grains.data,
            defect_cracks=form.defect_cracks.data,
            defect_cleaning=form.defect_cleaning.data,
            defect_foliage=form.defect_foliage.data,
            defect_chipping=form.defect_chipping.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(dryer_control)
        db.session.commit()
        
        flash('Enregistrement du contrôle séchoir ajouté avec succès', 'success')
        return redirect(url_for('dryer.dryer_controls'))
    
    return render_template('dryer/dryer_control.html', form=form)

@dryer_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dryer_control(id):
    dryer_control = DryerControl.query.get_or_404(id)
    form = DryerControlForm(obj=dryer_control)
    
    if form.validate_on_submit():
        dryer_control.date = form.date.data
        dryer_control.shift = form.shift.data
        dryer_control.measurement_number = form.measurement_number.data
        dryer_control.residual_humidity = form.residual_humidity.data
        dryer_control.defect_grains = form.defect_grains.data
        dryer_control.defect_cracks = form.defect_cracks.data
        dryer_control.defect_cleaning = form.defect_cleaning.data
        dryer_control.defect_foliage = form.defect_foliage.data
        dryer_control.defect_chipping = form.defect_chipping.data
        dryer_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du contrôle séchoir mis à jour avec succès', 'success')
        return redirect(url_for('dryer.dryer_controls'))
    
    return render_template('dryer/dryer_control.html', form=form, edit=True, control=dryer_control)

# Individual Control Routes - Humidity
@dryer_bp.route('/humidity')
@login_required
def dryer_humidity():
    page = request.args.get('page', 1, type=int)
    controls = DryerControl.query.filter(DryerControl.residual_humidity.isnot(None)).order_by(DryerControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('dryer/dryer_humidity.html', controls=controls)

@dryer_bp.route('/humidity/add', methods=['GET', 'POST'])
@login_required
def add_dryer_humidity():
    form = DryerHumidityForm()
    
    if form.validate_on_submit():
        dryer_control = DryerControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            residual_humidity=form.residual_humidity.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        # Determine compliance
        if 0.1 <= form.residual_humidity.data <= 1.5:
            dryer_control.compliance_status = 'compliant'
        else:
            dryer_control.compliance_status = 'non_compliant'
        
        db.session.add(dryer_control)
        db.session.commit()
        
        flash('Mesure d\'humidité résiduelle ajoutée avec succès', 'success')
        return redirect(url_for('dryer.dryer_humidity'))
    
    return render_template('dryer/dryer_humidity.html', form=form)

@dryer_bp.route('/humidity/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dryer_humidity(id):
    dryer_control = DryerControl.query.get_or_404(id)
    form = DryerHumidityForm(obj=dryer_control)
    
    if form.validate_on_submit():
        dryer_control.date = form.date.data
        dryer_control.shift = form.shift.data
        dryer_control.measurement_number = form.measurement_number.data
        dryer_control.residual_humidity = form.residual_humidity.data
        dryer_control.notes = form.notes.data
        
        # Determine compliance
        if 0.1 <= form.residual_humidity.data <= 1.5:
            dryer_control.compliance_status = 'compliant'
        else:
            dryer_control.compliance_status = 'non_compliant'
        
        db.session.commit()
        
        flash('Mesure d\'humidité résiduelle mise à jour avec succès', 'success')
        return redirect(url_for('dryer.dryer_humidity'))
    
    return render_template('dryer/dryer_humidity.html', form=form, edit=True, control=dryer_control)

# Individual Control Routes - Aspect
@dryer_bp.route('/aspect')
@login_required
def dryer_aspect():
    page = request.args.get('page', 1, type=int)
    controls = DryerControl.query.filter(
        (DryerControl.defect_grains.isnot(None)) | 
        (DryerControl.defect_cracks.isnot(None)) |
        (DryerControl.defect_cleaning.isnot(None)) |
        (DryerControl.defect_foliage.isnot(None)) |
        (DryerControl.defect_chipping.isnot(None))
    ).order_by(DryerControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('dryer/dryer_aspect.html', controls=controls)

@dryer_bp.route('/aspect/add', methods=['GET', 'POST'])
@login_required
def add_dryer_aspect():
    form = DryerAspectForm()
    
    if form.validate_on_submit():
        dryer_control = DryerControl(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            defect_grains=form.defect_grains.data,
            defect_cracks=form.defect_cracks.data,
            defect_cleaning=form.defect_cleaning.data,
            defect_foliage=form.defect_foliage.data,
            defect_chipping=form.defect_chipping.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        # Determine compliance for aspect defects
        defects_compliant = (
            (form.defect_grains.data or 0) <= 15 and
            (form.defect_cracks.data or 0) <= 1 and
            (form.defect_cleaning.data or 0) <= 1 and
            (form.defect_foliage.data or 0) <= 1 and
            (form.defect_chipping.data or 0) <= 1
        )
        
        dryer_control.compliance_status = 'compliant' if defects_compliant else 'non_compliant'
        
        db.session.add(dryer_control)
        db.session.commit()
        
        flash('Inspection d\'aspect ajoutée avec succès', 'success')
        return redirect(url_for('dryer.dryer_aspect'))
    
    return render_template('dryer/dryer_aspect.html', form=form)

@dryer_bp.route('/aspect/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dryer_aspect(id):
    dryer_control = DryerControl.query.get_or_404(id)
    form = DryerAspectForm(obj=dryer_control)
    
    if form.validate_on_submit():
        dryer_control.date = form.date.data
        dryer_control.shift = form.shift.data
        dryer_control.measurement_number = form.measurement_number.data
        dryer_control.defect_grains = form.defect_grains.data
        dryer_control.defect_cracks = form.defect_cracks.data
        dryer_control.defect_cleaning = form.defect_cleaning.data
        dryer_control.defect_foliage = form.defect_foliage.data
        dryer_control.defect_chipping = form.defect_chipping.data
        dryer_control.notes = form.notes.data
        
        # Determine compliance for aspect defects
        defects_compliant = (
            (form.defect_grains.data or 0) <= 15 and
            (form.defect_cracks.data or 0) <= 1 and
            (form.defect_cleaning.data or 0) <= 1 and
            (form.defect_foliage.data or 0) <= 1 and
            (form.defect_chipping.data or 0) <= 1
        )
        
        dryer_control.compliance_status = 'compliant' if defects_compliant else 'non_compliant'
        
        db.session.commit()
        
        flash('Inspection d\'aspect mise à jour avec succès', 'success')
        return redirect(url_for('dryer.dryer_aspect'))
    
    return render_template('dryer/dryer_aspect.html', form=form, edit=True, control=dryer_control)
