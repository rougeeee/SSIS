from web import create_app
from web.controllers.student_controller import student_bp
from web.controllers.college_controller import college_bp
from web.controllers.program_controller import program_bp

app = create_app()
app.register_blueprint(student_bp, url_prefix='/')
app.register_blueprint(college_bp, url_prefix='/colleges')
app.register_blueprint(program_bp, url_prefix='/programs')

if __name__ == '__main__':
    app.run(debug=True)