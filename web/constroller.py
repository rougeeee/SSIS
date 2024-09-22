from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def students():
    return render_template('students.html')

@views.route('/college/')
def school():
    return render_template('college.html')

@views.route('/programs')
def course():
    return render_template('programs.html')