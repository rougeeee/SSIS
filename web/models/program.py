from db import get_connection

class Program:
    @staticmethod
    def get_all(search_query=None):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT p.code, p.name, p.college_code, c.name AS college_name
            FROM program p
            LEFT JOIN college c ON p.college_code = c.code
        """
        params = []

        if search_query:
            query += """
                WHERE p.code LIKE %s OR p.name LIKE %s 
                OR p.college_code LIKE %s OR c.name LIKE %s
            """
            like_query = f"%{search_query}%"
            params.extend([like_query, like_query, like_query, like_query])

        cursor.execute(query, params)
        programs = cursor.fetchall()
        cursor.close()
        connection.close()
        return programs

    @staticmethod
    def add(data):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO program (code, name, college_code) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['code'], data['name'], data['college_code']))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(course_code):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM program WHERE code = %s", (course_code,))
        connection.commit()
        cursor.close()
        connection.close()
    
    @staticmethod
    def edit(data, original_code):
        connection = get_connection()
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
