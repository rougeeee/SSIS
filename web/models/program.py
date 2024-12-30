from flask import current_app
import mysql.connector

class Program:
    @staticmethod
    def get_all(search_query=None):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM program"
        params = []
        if search_query:
            query += " WHERE code LIKE %s OR name LIKE %s OR college_code LIKE %s"
            like_query = f"%{search_query}%"
            params.extend([like_query, like_query, like_query])

        cursor.execute(query, params)
        programs = cursor.fetchall()
        cursor.close()
        connection.close()
        return programs

    @staticmethod
    def add(data):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = "INSERT INTO program (code, name, college_code) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['code'], data['name'], data['college_code']))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(course_code):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM program WHERE code = %s", (course_code,))
        connection.commit()
        cursor.close()
        connection.close()
    
    @staticmethod
    def edit(data, original_code):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = """
            UPDATE program 
            SET code = %s, name = %s, college_code = %s
            WHERE code = %s
        """
        cursor.execute(query, (data['code'], data['name'], data['college_code'], original_code))
        connection.commit()
        cursor.close()
        connection.close()