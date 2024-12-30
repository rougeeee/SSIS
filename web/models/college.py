from flask import current_app
import mysql.connector

class College:
    @staticmethod
    def get_all(search_query=None):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM college"
        params = []
        if search_query:
            query += " WHERE code LIKE %s OR name LIKE %s"
            like_query = f"%{search_query}%"
            params.extend([like_query, like_query])
            
        cursor.execute(query, params)
        colleges = cursor.fetchall()
        cursor.close()
        connection.close()
        return colleges

    @staticmethod
    def add(data):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = "INSERT INTO college (code, name) VALUES (%s, %s)"
        cursor.execute(query, (data['code'], data['name']))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(college_code):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM college WHERE code = %s", (college_code,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(original_code, data):
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        query = """
            UPDATE college 
            SET code = %s, name = %s 
            WHERE code = %s
        """
        cursor.execute(query, (data['code'], data['name'], original_code))
        connection.commit()
        cursor.close()
        connection.close()
