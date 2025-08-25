from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from forms_admin import SpecificationForm, BulkSpecificationForm
from models import Specification
from app import db
from utils.spec_defaults import initialize_default_specifications

spec_bp = Blueprint('specifications', __name__)

@spec_bp.route('/')
@login_required
def specifications():
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes pour accéder aux spécifications', 'error')
        return redirect(url_for('main.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    control_filter = request.args.get('control_type')
    
    query = Specification.query
    if control_filter:
        query = query.filter(Specification.control_type == control_filter)
    
    specs = query.order_by(Specification.control_type, Specification.parameter_name).paginate(
        page=page, per_page=50, error_out=False)
    
    control_types = db.session.query(Specification.control_type.distinct()).all()
    control_types = [ct[0] for ct in control_types]
    
    return render_template('specifications/specifications.html', 
                         specs=specs, 
                         control_filter=control_filter,
                         control_types=control_types)

@spec_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_specification():
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes', 'error')
        return redirect(url_for('specifications.specifications'))
    
    form = SpecificationForm()
    
    if form.validate_on_submit():
        # Check for existing specification
        existing = Specification.query.filter(
            Specification.control_type == form.control_type.data,
            Specification.parameter_name == form.parameter_name.data,
            Specification.format_type == form.format_type.data or None,
            Specification.enamel_type == form.enamel_type.data or None
        ).first()
        
        if existing:
            flash('Spécification déjà existante pour cette combinaison de paramètres', 'error')
            return render_template('specifications/specification_form.html', form=form)
        
        specification = Specification(
            control_type=form.control_type.data,
            parameter_name=form.parameter_name.data,
            format_type=form.format_type.data if form.format_type.data else None,
            enamel_type=form.enamel_type.data if form.enamel_type.data else None,
            min_value=form.min_value.data,
            max_value=form.max_value.data,
            target_value=form.target_value.data,
            unit=form.unit.data,
            description=form.description.data,
            is_active=form.is_active.data,
            created_by=current_user.id
        )
        
        db.session.add(specification)
        db.session.commit()
        
        flash('Spécification ajoutée avec succès', 'success')
        return redirect(url_for('specifications.specifications'))
    
    return render_template('specifications/specification_form.html', form=form)

@spec_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_specification(id):
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes', 'error')
        return redirect(url_for('specifications.specifications'))
    
    specification = Specification.query.get_or_404(id)
    form = SpecificationForm(obj=specification)
    
    if form.validate_on_submit():
        specification.control_type = form.control_type.data
        specification.parameter_name = form.parameter_name.data
        specification.format_type = form.format_type.data if form.format_type.data else None
        specification.enamel_type = form.enamel_type.data if form.enamel_type.data else None
        specification.min_value = form.min_value.data
        specification.max_value = form.max_value.data
        specification.target_value = form.target_value.data
        specification.unit = form.unit.data
        specification.description = form.description.data
        specification.is_active = form.is_active.data
        
        db.session.commit()
        
        flash('Spécification mise à jour avec succès', 'success')
        return redirect(url_for('specifications.specifications'))
    
    return render_template('specifications/specification_form.html', form=form, edit=True, spec=specification)

@spec_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_specification(id):
    if current_user.role != 'admin':
        flash('Seuls les administrateurs peuvent supprimer les spécifications', 'error')
        return redirect(url_for('specifications.specifications'))
    
    specification = Specification.query.get_or_404(id)
    db.session.delete(specification)
    db.session.commit()
    
    flash('Spécification supprimée avec succès', 'success')
    return redirect(url_for('specifications.specifications'))

@spec_bp.route('/bulk', methods=['GET', 'POST'])
@login_required
def bulk_operations():
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes', 'error')
        return redirect(url_for('specifications.specifications'))
    
    form = BulkSpecificationForm()
    
    if form.validate_on_submit():
        if form.action.data == 'reset_defaults':
            # Reset to default specifications
            result = initialize_default_specifications(form.control_type.data)
            flash(f'Réinitialisé {result} spécifications par défaut pour {form.control_type.data}', 'success')
        
        elif form.action.data == 'deactivate_all':
            # Deactivate all specifications for the control type
            specs = Specification.query.filter(Specification.control_type == form.control_type.data).all()
            for spec in specs:
                spec.is_active = False
            db.session.commit()
            flash(f'Désactivé toutes les spécifications pour {form.control_type.data}', 'warning')
        
        return redirect(url_for('specifications.specifications'))
    
    return render_template('specifications/bulk_operations.html', form=form)

@spec_bp.route('/initialize_all')
@login_required
def initialize_all_defaults():
    if current_user.role != 'admin':
        flash('Seuls les administrateurs peuvent initialiser toutes les spécifications', 'error')
        return redirect(url_for('specifications.specifications'))
    
    total_created = 0
    control_types = ['clay', 'press', 'dryer', 'biscuit_kiln', 'email_kiln', 'dimensional', 'enamel', 'digital']
    
    for control_type in control_types:
        created = initialize_default_specifications(control_type)
        total_created += created
    
    flash(f'Initialisé {total_created} spécifications par défaut pour tous les types de contrôle', 'success')
    return redirect(url_for('specifications.specifications'))

@spec_bp.route('/api/specs/<control_type>')
@login_required
def get_specs_api(control_type):
    """API endpoint to get specifications for a control type"""
    specs = Specification.query.filter(
        Specification.control_type == control_type,
        Specification.is_active == True
    ).all()
    
    specs_data = []
    for spec in specs:
        specs_data.append({
            'id': spec.id,
            'parameter_name': spec.parameter_name,
            'format_type': spec.format_type,
            'enamel_type': spec.enamel_type,
            'min_value': spec.min_value,
            'max_value': spec.max_value,
            'target_value': spec.target_value,
            'unit': spec.unit,
            'description': spec.description
        })
    
    return jsonify(specs_data)