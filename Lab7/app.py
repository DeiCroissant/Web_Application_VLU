from flask import Flask, render_template, request, redirect, url_for

from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db["students"]


@app.route('/')
def index():
    students = list(collection.find())
    return render_template("index.html", students=students)

#add a student
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        collection.insert_one({
            "name": request.form["name"],
            "age": request.form["age"],
            "major": request.form["major"]
        })

        return redirect(url_for("index"))
    return render_template("form.html", student=None)

#Edit a student
@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit(id):
    student = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        collection.update_one({"_id": ObjectId(id)}, {"$set": {
            "name": request.form["name"],
            "age": int(request.form["age"]),
            "major": request.form["major"]
        }})
        return redirect(url_for("index"))
    return render_template("form.html", student=student)

#Delete a student

@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))