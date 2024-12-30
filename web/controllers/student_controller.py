from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.models.student import Student
from web.models.program import Program
from math import ceil

student_bp = Blueprint('students', __name__)

@student_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        student_data = {
            'image': request.files.get('image'),
            'id': request.form.get('id'),
            'firstname': request.form.get('firstname'),
            'lastname': request.form.get('lastname'),
            'year': request.form.get('year'),
            'gender': request.form.get('gender'),
            'course': request.form.get('course')
        }
        try:
            if action == "add":
                Student.add(student_data)
                flash("Student added successfully!", "success")
            elif action == "edit":
                Student.update(student_data)
                flash("Student updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
      
    search_query = request.args.get('searchQuery', '').strip()
    filter_course = request.args.get('filterCourse', '').strip()

    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = 10  # Number of students per page

    students, total_students = Student.get_all(search_query, filter_course, page, per_page)
    total_pages = (total_students + per_page - 1)

    return render_template(
        'students.html',
        students=students,
        programs=Program.get_all(),
        search_query=search_query,
        filter_course=filter_course,
        page=page,
        total_pages=total_pages
    )

@student_bp.route('/delete/<string:student_id>', methods=['POST'])
def delete(student_id):
    try:
        Student.delete(student_id)
        flash("Student deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for('students.index'))