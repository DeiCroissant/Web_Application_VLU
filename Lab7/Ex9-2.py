from flask import Flask, render_template, request, redirect, url_for, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['students_db']
students = db['Chapter6_Students']

# Helper function to add GPA and rank to student data
def add_gpa_and_rank(students_list):
    for student in students_list:
        if all(key in student for key in ['math', 'literature', 'english']):
            scores = [student['math'], student['literature'], student['english']]
            student['gpa'] = sum(scores) / len(scores)
            if student['gpa'] >= 8:
                student['rank'] = 'Excellent'
            elif student['gpa'] >= 6.5:
                student['rank'] = 'Good'
            else:
                student['rank'] = 'Average'
    return students_list

# Index route with search and filter by major
@app.route('/', methods=['GET'])
def index():
    name = request.args.get('name')
    major = request.args.get('major')
    query = {}
    if name:
        query['name'] = name
    if major:
        query['major'] = major
    students_list = list(students.find(query))
    students_list = add_gpa_and_rank(students_list)
    majors = students.distinct('major')
    counts = list(students.aggregate([{"$group": {"_id": "$major", "count": {"$sum": 1}}}]))
    return render_template('index.html', students=students_list, majors=majors, counts=counts)

# Add student route
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        students.insert_one({
            'name': request.form['name'],
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'major': request.form['major'],
            'math': int(request.form['math']),
            'literature': int(request.form['literature']),
            'english': int(request.form['english'])
        })
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Edit student route
@app.route('/edit_student/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = students.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        students.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'age': int(request.form['age']),
                'gender': request.form['gender'],
                'major': request.form['major'],
                'math': int(request.form['math']),
                'literature': int(request.form['literature']),
                'english': int(request.form['english'])
            }}
        )
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

# Delete student route
@app.route('/delete_student/<string:id>')
def delete_student(id):
    students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

# Fuzzy search route
@app.route('/fuzzy_search')
def fuzzy_search():
    name = request.args.get('name')
    if name:
        regex = {'$regex': name, '$options': 'i'}
        students_list = list(students.find({'name': regex}))
    else:
        students_list = list(students.find())
    students_list = add_gpa_and_rank(students_list)
    return render_template('index.html', students=students_list)

# Excellent students route
@app.route('/excellent_students')
def excellent_students():
    students_list = list(students.find())
    excellent_students = []
    for student in students_list:
        scores = [student['math'], student['literature'], student['english']]
        gpa = sum(scores) / len(scores)
        if gpa >= 8:
            student['gpa'] = gpa
            student['rank'] = 'Excellent'
            excellent_students.append(student)
    return render_template('index.html', students=excellent_students)

# Top student route
@app.route('/top_student')
def top_student():
    students_list = list(students.find())
    if not students_list:
        return "No students found"
    students_list = add_gpa_and_rank(students_list)
    top_student = max(students_list, key=lambda x: x['gpa'])
    return render_template('top_student.html', student=top_student)

# Filter by age route
@app.route('/filter_by_age')
def filter_by_age():
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    query = {}
    if min_age is not None:
        query['age'] = {'$gte': min_age}
    if max_age is not None:
        query['age'] = query.get('age', {})
        query['age']['$lte'] = max_age
    students_list = list(students.find(query))
    students_list = add_gpa_and_rank(students_list)
    return render_template('index.html', students=students_list)

# Filter by gender route
@app.route('/filter_by_gender')
def filter_by_gender():
    gender = request.args.get('gender')
    if gender:
        students_list = list(students.find({'gender': gender}))
    else:
        students_list = list(students.find())
    students_list = add_gpa_and_rank(students_list)
    return render_template('index.html', students=students_list)

if __name__ == '__main__':
    app.run(debug=True)