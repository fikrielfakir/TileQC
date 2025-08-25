from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from utils.helpers import get_dashboard_stats, get_recent_non_conformities, get_weekly_trend_data, get_format_distribution
from datetime import date, timedelta
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Get date filter from request
    date_filter = request.args.get('date')
    if date_filter:
        try:
            selected_date = date.fromisoformat(date_filter)
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Get dashboard statistics
    stats = get_dashboard_stats(selected_date)
    
    # Get recent non-conformities
    recent_nc = get_recent_non_conformities(10)
    
    # Get weekly trend data
    trend_data = get_weekly_trend_data()
    
    # Get format distribution
    format_dist = get_format_distribution()
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_nc=recent_nc,
                         trend_data=json.dumps(trend_data),
                         format_dist=json.dumps(format_dist),
                         selected_date=selected_date)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
