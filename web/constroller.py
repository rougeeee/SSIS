from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        yearLevel = request.form.get('year')
        gender = request.form.get('gender')
        course = request.form.get('program')

        if len(firstName) == 0:
            flash('Invalid first name.', category='error')
        elif len(lastName) == 0:
            flash('Invalid last name.', category='error')
        elif len(yearLevel) < 8:
            flash('Invalid Year Level.', category='error')
        else:
            flash('Student added.', category='success')
    
    return render_template('students.html')

@views.route('/college/', methods=['GET', 'POST'])
def school():
    return render_template('college.html')

@views.route('/programs', methods=['GET', 'POST'])
def course():
    return render_template('programs.html')