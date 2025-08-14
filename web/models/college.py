from db import get_connection

class College:
    @staticmethod
    def get_all(search_query=None):
        connection = get_connection()
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
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO college (code, name) VALUES (%s, %s)"
        cursor.execute(query, (data['code'], data['name']))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(college_code):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM college WHERE code = %s", (college_code,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(original_code, data):
        connection = get_connection()
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
