from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
import mysql.connector

views = Blueprint('views', __name__)

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
        action = request.form.get('action')  # Get the action (add or edit)

        # Input validation
        if len(firstName) == 0:
            flash('Invalid first name.', category='error')
        elif len(lastName) == 0:
            flash('Invalid last name.', category='error')
        elif not yearLevel.isdigit() or int(yearLevel) not in range(1, 5):
            flash('Invalid Year Level. Must be between 1 and 4.', category='error')
        else:
            # Add or update student in the database based on action
            try:
                connection = mysql.connector.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    database=current_app.config['MYSQL_DB']
                )
                cursor = connection.cursor()

                if action == "add":
                    # Check if the ID already exists
                    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
                    existing_student = cursor.fetchone()
                    if existing_student:
                        flash('Student ID already exists. Please use a different ID.', category='error')
                    else:
                        query = """INSERT INTO student (id, firstname, lastname, year, gender, course) 
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                        cursor.execute(query, (student_id, firstName, lastName, yearLevel, gender, course))
                        flash('Student added successfully.', category='success')

                elif action == "edit":
                    query = """UPDATE student 
                               SET firstname = %s, lastname = %s, year = %s, gender = %s, course = %s 
                               WHERE id = %s"""
                    cursor.execute(query, (firstName, lastName, yearLevel, gender, course, student_id))
                    flash('Student updated successfully.', category='success')

                connection.commit()

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

# Route to handle fetching student data for editing
@views.route('/edit/<student_id>', methods=['GET'])
def edit_student(student_id):
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        student = cursor.fetchone()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')
        student = None

    finally:
        cursor.close()
        connection.close()

    if student:
        return render_template('students.html', students=[student])  # Render the student for editing
    else:
        flash('Student not found.', category='error')
        return redirect(url_for('views.students'))
    
@views.route('/delete/<student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()

        # Delete student with the given ID
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        connection.commit()
        flash('Student deleted successfully.', category='success')

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('views.students'))  # Redirect back to the student list

# College route
@views.route('/college/', methods=['GET', 'POST'])
def school():   
    return render_template('college.html')

# Programs route
@views.route('/programs', methods=['GET', 'POST'])
def course():
    return render_template('programs.html')