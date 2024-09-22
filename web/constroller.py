from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
import mysql.connector

views = Blueprint('views', __name__)

# Route to handle both displaying and adding students
@views.route('/', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        # Retrieve form data
        student_id = request.form.get('id')
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        yearLevel = request.form.get('year')
        gender = request.form.get('gender')
        course = request.form.get('course')

        # Input validation
        if len(firstName) == 0:
            flash('Invalid first name.', category='error')
        elif len(lastName) == 0:
            flash('Invalid last name.', category='error')
        elif not yearLevel.isdigit() or int(yearLevel) not in range(1, 5):
            flash('Invalid Year Level. Must be between 1 and 4.', category='error')
        else:
            # Add student to database
            try:
                connection = mysql.connector.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    database=current_app.config['MYSQL_DB']
                )
                cursor = connection.cursor()

                query = """INSERT INTO student (id, firstname, lastname, year, gender, course) 
                           VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (student_id, firstName, lastName, yearLevel, gender, course))

                connection.commit()
                flash('Student added successfully.', category='success')

            except mysql.connector.Error as err:
                flash(f"Error: {err}", category='error')

            finally:
                cursor.close()
                connection.close()

    # Retrieve all students from the database to display
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')
        students = []

    finally:
        cursor.close()
        connection.close()

    return render_template('students.html', students=students)

# College route (not much happening here, but placeholder for future)
@views.route('/college/', methods=['GET', 'POST'])
def school():
    return render_template('college.html')

# Programs route (another placeholder)
@views.route('/programs', methods=['GET', 'POST'])
def course():
    return render_template('programs.html')