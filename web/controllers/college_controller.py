from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.models.college import College

college_bp = Blueprint('colleges', __name__)

@college_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        college_data = {
            'code': request.form.get('collegeCode'),
            'name': request.form.get('collegeName'),
        }
        try:
            if action == 'add':
                College.add(college_data)
                flash("College added successfully!", "success")
            elif action == 'edit':
                original_code = request.form.get('originalCollegeCode')
                College.update(original_code, college_data)
                flash("College updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
    elif request.args.get('action') == 'delete':
        college_code = request.args.get('college_code')
        try:
            College.delete(college_code)
            flash("College deleted successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")

    search_query = request.args.get('searchQuery', '').strip()
    colleges = College.get_all(search_query)
    return render_template('college.html', colleges=colleges)