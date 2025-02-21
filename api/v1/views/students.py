# i want to do authentication for the student
"""This module defines all the paths for the user moijdule"""

from models.student_models import Student
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, session, make_response, abort
from datetime import datetime, timedelta
from flask import current_app
from flasgger.utils import swag_from
from flask_login import login_required, current_user


@app_views.route("/students", methods=["POST"], strict_slashes=False)
@swag_from('documentation/student/create_student.yml', methods=['POST'])
def create_student():
    """
    Create a new student
    """
    required_fields = [
        "firstname",
        "middlename",
        "lastname",
        "email",
        "password",
        "birth_date",
        "age",
        "gender",
        "address",
        "phone_no",
        "grade",
        "section"
    ]
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    student = Student(**data)
    student.save()
    return jsonify(student.to_dict()), 201


@app_views.route("/students", methods=["GET"], strict_slashes=False)
@swag_from('documentation/student/all_students.yml', methods=['GET'])
@login_required
def get_students():
    """
    Get all users
    """
    students = storage.all(Student)
    students = [user.to_dict() for user in students.values()]

    return make_response(jsonify(students), 200)


# @app_views.route("/students/<student_id>", methods=["GET"],
#                  strict_slashes=False)
# @swag_from('documentation/student/get_student.yml', methods=['GET'])
# @token_required
# def get_student(student_id, user):
#     """Retrieves a student"""
#     print(session)
#     if session.get("logged_in") is True or not session["logged_in"]:
#         return jsonify({"error": "Unauthorized"}), 401

#     student = storage.get(Student, student_id)
#     if not student:
#         abort(404)

#     return make_response(jsonify(student.to_dict()), 200)


# @app_views.route("/students/<student_id>", methods=["DELETE"],
#                  strict_slashes=False)
# @swag_from('documentation/student/delete_student.yml', methods=['DELETE'])
# @token_required
# @require_user_class("Administrator")
# def delete_student(student_id, user):
#     """
#     Deletes a user Object
#     """
#     if session.get("logged_in") is None or not session["logged_in"]:
#         return jsonify({"error": "Unauthorized"}), 401

#     student = storage.get(Student, student_id)

#     if not student:
#         abort(404)

#     storage.delete(student)
#     storage.save()

#     return make_response(jsonify({}), 200)


# @app_views.route("/student/<student_id>", methods=["PUT"],
#                  strict_slashes=False)
# @swag_from('documentation/student/update_student.yml', methods=['PUT'])
# @token_required
# @require_user_class("Student")
# def update_student(student_id, user):
#     """
#     Updates a student
#     """
#     print(user)
#     if session.get("logged_in") is None or not session["logged_in"]:
#         return jsonify({"error": "Unauthorized"}), 401

#     student = storage.get(Student, student_id)

#     if not student:
#         abort(404)

#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     ignore = ["id", "email", "created_at", "updated_at"]

#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore:
#             setattr(student, key, value)
#     storage.save()

#     return make_response(jsonify(student.to_dict()), 200)
