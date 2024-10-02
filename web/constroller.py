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

@views.route('/college/', methods=['GET', 'POST'])
def college():
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            action = request.form.get('action')
            college_code = request.form.get('collegeCode')
            college_name = request.form.get('collegeName')
            original_college_code = request.form.get('originalCollegeCode')

            if len(college_code) == 0 or len(college_name) == 0:
                flash('College code and name are required.', category='error')
            else:
                if action == 'add':
                    try:
                        query = "INSERT INTO college (code, name) VALUES (%s, %s)"
                        cursor.execute(query, (college_code, college_name))
                        connection.commit()
                        flash('College added successfully!', category='success')
                    except mysql.connector.Error as err:
                        flash(f"Error: {err}", category='error')
                elif action == 'edit':
                    try:
                        # Check if the new college code already exists
                        query = "SELECT COUNT(*) FROM college WHERE code = %s AND code != %s"
                        cursor.execute(query, (college_code, original_college_code))  # Compare with original code
                        count = cursor.fetchone()['COUNT(*)']

                        if count > 0:
                            flash('College code must be unique.', category='error')
                        else:
                            query = "UPDATE college SET code = %s, name = %s WHERE code = %s"
                            cursor.execute(query, (college_code, college_name, original_college_code))  # Use original code for the WHERE clause
                            connection.commit()
                            flash('College updated successfully!', category='success')

                    except mysql.connector.Error as err:
                        flash(f"Error updating college: {err}", category='error')

        cursor.execute("SELECT * FROM college")
        colleges = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')
        colleges = []

    finally:
        cursor.close()
        connection.close()

    return render_template('college.html', colleges=colleges)

@views.route('/delete-college/<string:college_code>', methods=['POST'])
def delete_college(college_code):
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()

        delete_query = "DELETE FROM college WHERE code = %s"
        cursor.execute(delete_query, (college_code,))

        connection.commit()
        flash('College and associated programs deleted successfully, students\' courses set to NULL.', category='success')

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('views.college'))

@views.route('/programs', methods=['GET', 'POST'])
def programs():
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            action = request.form.get('action')
            course_code = request.form.get('courseCode')
            course_name = request.form.get('courseName')
            college_code = request.form.get('collegeCode')
            original_course_code = request.form.get('originalCourseCode')  # Get original course code

            if len(course_code) == 0 or len(course_name) == 0 or len(college_code) == 0:
                flash('All fields are required.', category='error')
            else:
                if action == 'add':
                    try:
                        query = "INSERT INTO program (code, name, college_code) VALUES (%s, %s, %s)"
                        cursor.execute(query, (course_code, course_name, college_code))
                        connection.commit()
                        flash('Program added successfully!', category='success')
                    except mysql.connector.Error as err:
                        flash(f"Error adding program: {err}", category='error')

                elif action == 'edit':
                    try:
                        # Check if the new course code already exists (and is not the original code)
                        query = "SELECT COUNT(*) FROM program WHERE code = %s AND code != %s"
                        cursor.execute(query, (course_code, original_course_code))
                        count = cursor.fetchone()['COUNT(*)']

                        if count > 0:
                            flash('Course code must be unique.', category='error')
                        else:
                            # Update the program with the new course code and other fields
                            query = "UPDATE program SET code = %s, name = %s, college_code = %s WHERE code = %s"
                            cursor.execute(query, (course_code, course_name, college_code, original_course_code))
                            connection.commit()
                            flash('Program updated successfully!', category='success')

                    except mysql.connector.Error as err:
                        flash(f"Error updating program: {err}", category='error')

        cursor.execute("SELECT * FROM program")
        programs = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", category='error')
        programs = []

    finally:
        cursor.close()
        connection.close()

    return render_template('programs.html', programs=programs)

@views.route('/delete_program/<course_code>', methods=['POST'])
def delete_program(course_code):
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = """DELETE FROM program WHERE code=%s"""
        cursor.execute(query, (course_code,))
        connection.commit()
        flash('Program deleted successfully.', category='success')

    except mysql.connector.Error as err:
        flash(f"Error: {err}", category='error')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('views.programs'))
