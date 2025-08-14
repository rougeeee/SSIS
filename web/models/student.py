from db import get_connection
import cloudinary.uploader

class Student:
    @staticmethod
    def get_all(search_query=None, filter_course=None, page=1, per_page=10):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT s.*, p.name AS program_name, c.name AS college_name
        FROM student s
        LEFT JOIN program p ON s.course = p.code
        LEFT JOIN college c ON p.college_code = c.code
        """
        conditions = []
        params = []

        if search_query:
            like_query = f"%{search_query}%"
            conditions.append("""
                (s.id LIKE %s OR s.firstname LIKE %s OR s.lastname LIKE %s 
                OR s.course LIKE %s OR s.year LIKE %s OR s.gender LIKE %s
                OR p.name LIKE %s OR c.name LIKE %s)
            """)
            params.extend([like_query]*8)

        if filter_course:
            conditions.append("s.course = %s")
            params.append(filter_course)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(query, params)
        students = cursor.fetchall()

        # Count total with same filter/search
        count_query = """
        SELECT COUNT(*) AS total
        FROM student s
        LEFT JOIN program p ON s.course = p.code
        LEFT JOIN college c ON p.college_code = c.code
        """
        if conditions:
            count_query += " WHERE " + " AND ".join(conditions)
        cursor.execute(count_query, params[:-2])
        total_students = cursor.fetchone()['total']

        cursor.close()
        connection.close()
        return students, total_students

    @staticmethod
    def add(data):
        image_url = None
        if 'image' in data and data['image'].filename != "":
            result = cloudinary.uploader.upload(data['image'])
            image_url = result['secure_url']

        connection = get_connection()
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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update(data):
        image_url = data.get('image_url')  
        if data.get('image') and data['image'].filename != "":
            result = cloudinary.uploader.upload(data['image'])
            image_url = result['secure_url']

        connection = get_connection()
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
