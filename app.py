from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

        return redirect("/")

    return render_template("add_student.html")

@app.route("/delete/<int:id>")
def delete_student(id):

    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)