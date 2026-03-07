from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


@app.route("/")
def home():
    students = Student.query.all()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]

        new_student = Student(name=name, email=email)

        db.session.add(new_student)
        db.session.commit()

        flash("Student added successfully!")
        return redirect("/")

    return render_template("add_student.html")

@app.route("/delete/<int:id>")
def delete_student(id):

    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!")
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Student.query.get(id)

    if request.method == "POST":

        student.name = request.form["name"]
        student.email = request.form["email"]

        db.session.commit()

        flash("Student updated successfully!")
        return redirect("/")

    return render_template("edit_student.html", student=student)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)