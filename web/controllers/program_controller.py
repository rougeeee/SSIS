from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.models.program import Program
from web.models.college import College

program_bp = Blueprint('programs', __name__)

@program_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        program_data = {
            'code': request.form.get('courseCode'),
            'name': request.form.get('courseName'),
            'college_code': request.form.get('collegeCode')
        }
        try:
            if action == 'add':
                Program.add(program_data)
                flash("Program added successfully!", "success")
            elif action == 'edit':
                original_code = request.form.get('originalCourseCode')
                Program.edit(program_data, original_code)
                flash("Program updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
    
    if request.method == 'POST' and 'course_code' in request.args:
        course_code = request.args.get('course_code')
        try:
            Program.delete(course_code)
            flash("Program deleted successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")

    search_query = request.args.get('searchQuery', '').strip()
    programs = Program.get_all(search_query)
    colleges = College.get_all()  

    return render_template('programs.html', programs=programs, colleges=colleges)
