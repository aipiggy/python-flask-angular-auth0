# coding=utf-8

from flask_cors import CORS
from flask import Flask, jsonify, request
from entities.entity import Session, engine, Base
from entities.exam import Exam, ExamSchema
import json

from auth import AuthError, requires_auth, requires_role

app = Flask(__name__)
CORS(app)

# generate db schema
Base.metadata.create_all(engine)

@app.route('/')
def root():
    return jsonify({'status':'OK'}), 200

@app.route('/exams')
def get_exams():
    session = Session()
    exam_objects = session.query(Exam).all()
    
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)
    
    session.close()
    return jsonify(exams)
   
@app.route('/exams', methods=['POST'])
@requires_auth
def add_exam():
    posted_exam = ExamSchema(only=('title', 'description', 'long_description')).load(request.get_json())
    exam = Exam(**posted_exam, created_by="HTTP Post Request")

    session = Session()
    session.add(exam)
    session.commit()
    
    new_exam = ExamSchema().dump(exam)
    session.close()
    
    return jsonify(new_exam), 201

@app.route('/exams/<examId>', methods=['DELETE'])
@requires_role('admin')
def delete_exam(examId):
    session = Session()
    exam = session.query(Exam).filter_by(id=examId).first()
    session.delete(exam)
    session.commit()
    session.close()
    return '', 201

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

if __name__ == '__main__':
    app.run()
