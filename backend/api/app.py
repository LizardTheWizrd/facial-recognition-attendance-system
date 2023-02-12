from flask import Flask, jsonify, request
from test import sayhi
from student.read import *
from teacher.read import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_cors import CORS
from datetime import timedelta
from utility.error_handlers import *
app = Flask(__name__)
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=0)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=10)
jwt = JWTManager(app)
ALLOWED_STATUS = ["present", "absent", "excused"]
ALLOWED_WEEK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#login
# @app.route('/api/login', methods = ['POST'])
# def login():
#     try:
#     # placeholder
#         teacher_id = request.json['teacher_id']
#         email = request.json['email']
#         password = request.json['password']
#         return teacher_id, 200
#     except Exception as e:
#         return e, 404

#login route to create a jwt token for user
@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "123" or password != "abshir":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

#get all classes for a teacher
@app.route("/api/v1/classes", methods=["GET"])
@jwt_required()
def get_classes():
    try:
        result = all_classes(get_jwt_identity())
    except Exception as e:
        return error_response("An error occurred while retrieving classes", 500)

    if not result:
        return error_response("No classes found for the teacher", 204)
        
    return jsonify(result), 200

#tester
@app.route("/api/test/classes", methods=["GET"])
#@jwt_required()
def test_get_classes():
    result = all_classes(123)
    return jsonify(result), 200

#get attendance list for a specific session with additional query v2
@app.route("/api/v2/attendance/<subject_code>/<session_number>/<week>", methods=["GET"])
@jwt_required()
def get_session_attendance_v2(subject_code, session_number, week):
    status = request.args.get('status')
    try:
        session_number = int(session_number)
    except ValueError:
        return error_response("Invalid session number format", 400)
    
    if status is not None:
        if status not in ALLOWED_STATUS:
            return error_response(f"Invalid status: {status}", 400)
 
    try:
        if int(week) not in ALLOWED_WEEK:
            return error_response(f"Invalid week: {week}", 400)
    except ValueError:
        return error_response("Invalid week format", 400)
        
    try:
        result = session_attendance(subject_code, session_number, status, week)
    except Exception as e:
        return error_response("An error occurred while retrieving attendance", 500)
    
    if not result:
        return error_response("No attendance data found", 204)

    return jsonify(result), 200

#get attendance list for a specific session with additional query
@app.route("/api/v1/attendance/<subject_code>/<session_number>", methods=["GET"])
@jwt_required()
def get_session_attendance(subject_code, session_number):
    status = request.args.get('status')
    week = request.args.get('week')

    try:
        session_number = int(session_number)
    except ValueError:
        return error_response("Invalid session number format", 400)
    
    if status is not None:
        if status not in ALLOWED_STATUS:
            return error_response(f"Invalid status: {status}", 400)

    try:
        if week is not None:    
            if int(week) not in ALLOWED_WEEK:
                return error_response(f"Invalid week: {week}", 400)
    except Exception as e:
        return error_response("Invalid week format", 400)

    try:
        result = session_attendance(subject_code, session_number, status, week)
    except Exception as e:
        return error_response("An error occurred while retrieving attendance", 500)
    
    if not result:
        return error_response("No attendance data found", 204)

    return jsonify(result), 200

#tester
@app.route("/api/test/attendance/<subject_code>/<session_number>", methods=["GET"])
def test_get_session_attendance(subject_code, session_number):
    status = request.args.get('status')
    week = request.args.get('week')
    result = session_attendance(subject_code, session_number, status, week)
    return jsonify(result), 200

#get live attendance list for a specific session (list displayed while attendance recording is active)
@app.route("/api/v1/live-attendance/<subject_code>/<session_number>/<week>", methods=["GET"])
@jwt_required()
def get_live_session_attendance(subject_code, session_number, week):
    try:
        session_number = int(session_number)
    except ValueError:
        return error_response("Invalid session number format", 400)
 
    try:
        if int(week) not in ALLOWED_WEEK:
            return error_response(f"Invalid week: {week}", 400)
    except ValueError:
        return error_response("Invalid week format", 400)

    try:
        result = live_session_attendance(subject_code, session_number, week)
    except Exception as e:
        return error_response("An error occurred while retrieving live attendance ", 500)
    
    if not result:
        return error_response("No live attendance data found", 204)

    return jsonify(result), 200

#tester
@app.route("/api/test/live-attendance/<subject_code>/<session_number>/<week>", methods=["GET"])
def test_get_live_session_attendance(subject_code, session_number, week):
    result = live_session_attendance(subject_code, session_number, week)
    return jsonify(result), 200

#get recent attendance list for a specific session (sorted by time)
@app.route("/api/v1/recent-attendance/<subject_code>/<session_number>/<week>", methods=["GET"])
@jwt_required()
def get_recent_session_attendance(subject_code, session_number, week):
    try:
        session_number = int(session_number)
    except ValueError:
        return error_response("Invalid session number format", 400)
 
    try:
        if int(week) not in ALLOWED_WEEK:
            return error_response(f"Invalid week: {week}", 400)
    except ValueError:
        return error_response("Invalid week format", 400)

    try:
        result = recent_session_attendance(subject_code, session_number, week)
    except Exception as e:
        return error_response("An error occurred while retrieving recent attendance ", 500)
    
    if not result:
        return error_response("No recent attendance data found", 204)

    return jsonify(result), 200

#tester
@app.route("/api/test/recent-attendance/<subject_code>/<session_number>/<week>", methods=["GET"])
def test_get_recent_session_attendance(subject_code, session_number, week):
    result = recent_session_attendance(subject_code, session_number, week)
    return jsonify(result), 200

#get teacher information for dashboard
@app.route("/api/v1/teacher-info", methods=["GET"])
@jwt_required()
def get_teacher_info():
    try:
        result = teacher_info(get_jwt_identity())
    except Exception as e:
        return error_response("An error occurred while retrieving teacher information ", 500)
    
    if not result:
        return error_response("No teacher information data found", 204)
    
    return jsonify(result), 200

#tester
@app.route("/api/test/teacher-info", methods=["GET"])
#@jwt_required()
def test_get_teacher_info():
    result = teacher_info(123)
    return jsonify(result), 200

#get upcoming classes for a teacher in dashboard
@app.route("/api/v1/upcoming-classes", methods=["GET"])
@jwt_required()
def get_upcoming_classes():
    try:
        result = upcoming_classes(get_jwt_identity())
    except Exception as e:
        return error_response("An error occurred while retrieving upcoming classes", 500)
    
    if not result:
        return error_response("No upcoming classes data found", 204)

    return jsonify(result), 200

#tester
@app.route("/api/test/upcoming-classes", methods=["GET"])
#@jwt_required()
def test_get_upcoming_classes():
    result = upcoming_classes(123)
    return jsonify(result), 200

#starting the attendance 
@app.route('/api/v1/start-recognition', methods = ['GET'])
@jwt_required()
def start_recognition():
    sayhi()
    return "Success", 200



#non-necessities
#get all students
@app.route('/api/v1/students', methods = ['GET'])
def get_all_students():
    result = all_students()
    return jsonify(result), 200

#get single student
@app.route('/api/v1/students/<student_id>', methods = ['GET'])
def get_single_student(student_id):
    result = single_student(student_id)
    return jsonify(result), 200

#get all teachers
@app.route('/api/v1/teachers', methods = ['GET'])
def get_all_teachers():
    result = all_teachers()
    return jsonify(result), 200

#get single teacher
@app.route('/api/v1/teachers/<teacher_id>', methods = ['GET'])
def get_single_teacher(teacher_id):
    result = single_teacher(teacher_id)
    return jsonify(result), 200

#getting all students for a specific subject or specific session
@app.route('/api/v1/subjects/<subject_code>/students', methods = ['GET'])
def get_students_subject(subject_code):
    day = request.args.get('day')
    time = request.args.get('time')
    result = students_subject(subject_code, day, time)
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
