from flask import current_app
import mysql.connector
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename

class Student:
    @staticmethod
    def get_all(search_query=None, filter_course=None, page=1, per_page=10):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM student"
        params = []
        if search_query:
            query += " WHERE id LIKE %s OR firstname LIKE %s OR lastname LIKE %s OR course LIKE %s OR year LIKE %s OR gender LIKE %s"
            like_query = f"%{search_query}%"
            params.extend([like_query, like_query, like_query, like_query, like_query, like_query])

        if filter_course:
            query += " AND course = %s"
            params.append(filter_course)

        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(query, params)
        students = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM student")
        total_students = cursor.fetchone()['COUNT(*)']

        cursor.close()
        connection.close()
        return students, total_students

    @staticmethod
    def add(data):
        image_url = None
        if 'image' in data:
            image = data['image']
            if image and image.filename != "":
                result = cloudinary.uploader.upload(image)
                image_url = result['secure_url']

        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = """INSERT INTO student (image_url, id, firstname, lastname, year, gender, course) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
            image_url, data['id'], data['firstname'], data['lastname'], 
            data['year'], data['gender'], data['course']
        ))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(student_id):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(data):
        image_url = data.get('image_url')  
        if data.get('image'):
            image = data['image']
            result = cloudinary.uploader.upload(image)
            image_url = result['secure_url']

        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = """UPDATE student 
                SET image_url = %s, firstname = %s, lastname = %s, year = %s, gender = %s, course = %s 
                WHERE id = %s"""
        cursor.execute(query, (
            image_url, data['firstname'], data['lastname'], data['year'], 
            data['gender'], data['course'], data['id']
        ))
        connection.commit()
        cursor.close()
        connection.close()