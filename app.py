
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager
from ai_engine.ai_evaluator import evaluate_answer
from ai_engine.plagiarism_checker import plagiarism_percentage

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Question, GeneratedPaper, Submission

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import os
import random

app = Flask(__name__)

app.secret_key = "ai_papergen_major_project_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///questions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["ANSWER_FOLDER"] = "answers"
app.config["PAPER_FOLDER"] = "generated_papers"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

os.makedirs("answers", exist_ok=True)
os.makedirs("generated_papers", exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


def split_text(text, limit=88):
    words = text.split()

    lines = []
    line = ""

    for word in words:
        if len(line + word) <= limit:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "

    if line:
        lines.append(line.strip())

    return lines


def create_question_pdf(path, title, subject, questions, total_marks):

    pdf = canvas.Canvas(path, pagesize=A4)

    width, height = A4

    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, y, title)

    y -= 35

    pdf.setFont("Helvetica", 11)

    pdf.drawString(60, y, f"Subject: {subject}")
    pdf.drawRightString(width - 60, y, f"Total Marks: {total_marks}")

    y -= 25

    pdf.line(60, y, width - 60, y)

    y -= 35

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(60, y, "Question Paper")

    y -= 30

    pdf.setFont("Helvetica", 10)

    for index, q in enumerate(questions, start=1):

        if y < 90:
            pdf.showPage()
            y = height - 60
            pdf.setFont("Helvetica", 10)

        question_line = f"Q{index}. {q.question_text}"

        lines = split_text(question_line)

        for line in lines:
            pdf.drawString(60, y, line)
            y -= 15

        pdf.setFont("Helvetica-Bold", 10)

        pdf.drawString(
            60,
            y,
            f"Marks: {q.marks} | Difficulty: {q.difficulty} | Topic: {q.topic}"
        )

        pdf.setFont("Helvetica", 10)

        y -= 28

    pdf.save()


@app.route("/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("dashboard"))

        return redirect(url_for("student_dashboard"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("dashboard"))

            return redirect(url_for("student_dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        return redirect("/")

    total_questions = Question.query.count()

    total_students = User.query.filter_by(role="student").count()

    total_papers = GeneratedPaper.query.count()

    total_submissions = Submission.query.count()

    recent_papers = GeneratedPaper.query.order_by(
        GeneratedPaper.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_questions=total_questions,
        total_students=total_students,
        total_papers=total_papers,
        total_submissions=total_submissions,
        recent_papers=recent_papers
    )


@app.route("/student-dashboard")
@login_required
def student_dashboard():

    papers = GeneratedPaper.query.filter_by(
        assigned_to=current_user.id
    ).all()

    submissions = Submission.query.filter_by(
        student_id=current_user.id
    ).all()

    submitted_paper_ids = [s.paper_id for s in submissions]

    return render_template(
        "student_dashboard.html",
        papers=papers,
        submissions=submissions,
        submitted_paper_ids=submitted_paper_ids
    )


@app.route("/questions")
@login_required
def questions():

    question_list = Question.query.order_by(
        Question.id.desc()
    ).all()

    return render_template(
        "questions.html",
        questions=question_list,
        search=""
    )


@app.route("/add-question", methods=["GET", "POST"])
@login_required
def add_question():

    if request.method == "POST":

        q = Question(
            subject=request.form["subject"],
            topic=request.form["topic"],
            question_text=request.form["question_text"],
            marks=int(request.form["marks"]),
            difficulty=request.form["difficulty"],
            bloom_level=request.form["bloom_level"]
        )

        db.session.add(q)
        db.session.commit()

        flash("Question added successfully", "success")

    return render_template("add_question.html")


@app.route("/generate", methods=["GET", "POST"])
@login_required
def generate():

    subjects = [
        row[0]
        for row in db.session.query(Question.subject).distinct().all()
    ]

    topics = [
        row[0]
        for row in db.session.query(Question.topic).distinct().all()
    ]

    students = User.query.filter_by(role="student").all()

    if request.method == "POST":

        exam_title = request.form["exam_title"]

        subject = request.form["subject"]

        student_id = int(request.form["student_id"])

        total_marks = int(request.form["total_marks"])

        selected_questions = Question.query.filter_by(
            subject=subject
        ).all()

        random.shuffle(selected_questions)

        final_questions = []

        marks = 0

        for q in selected_questions:

            if marks + q.marks <= total_marks:

                final_questions.append(q)

                marks += q.marks

        pdf_name = secure_filename(
            f"{exam_title}_{student_id}_{random.randint(1000,9999)}.pdf"
        )

        pdf_path = os.path.join(
            app.config["PAPER_FOLDER"],
            pdf_name
        )

        create_question_pdf(
            pdf_path,
            exam_title,
            subject,
            final_questions,
            marks
        )

        paper = GeneratedPaper(
            exam_title=exam_title,
            subject=subject,
            total_marks=total_marks,
            generated_marks=marks,
            question_ids=",".join([str(q.id) for q in final_questions]),
            created_by=current_user.id,
            assigned_to=student_id,
            pdf_file=pdf_name
        )

        db.session.add(paper)
        db.session.commit()

        flash("Paper assigned successfully", "success")

        return redirect("/dashboard")

    return render_template(
        "generate.html",
        subjects=subjects,
        topics=topics,
        students=students
    )


@app.route("/download-paper/<filename>")
@login_required
def download_paper(filename):

    return send_file(
        os.path.join(
            app.config["PAPER_FOLDER"],
            filename
        ),
        as_attachment=True
    )


@app.route("/upload-answer/<int:paper_id>", methods=["POST"])
@login_required
def upload_answer(paper_id):

    file = request.files["answer_pdf"]

    filename = secure_filename(file.filename)

    file.save(
        os.path.join(
            app.config["ANSWER_FOLDER"],
            filename
        )
    )

    submission = Submission(
        paper_id=paper_id,
        student_id=current_user.id,
        answer_pdf=filename
    )

    db.session.add(submission)
    db.session.commit()

    flash("Answer uploaded successfully", "success")

    return redirect("/student-dashboard")


@app.route("/submissions")
@login_required
def submissions():

    all_submissions = Submission.query.order_by(
        Submission.id.desc()
    ).all()

    return render_template(
        "submissions.html",
        submissions=all_submissions,
        users=User.query.all(),
        papers=GeneratedPaper.query.all()
    )


@app.route("/download-answer/<filename>")
@login_required
def download_answer(filename):

    return send_file(
        os.path.join(
            app.config["ANSWER_FOLDER"],
            filename
        ),
        as_attachment=True
    )



@app.route("/grade-submission/<int:submission_id>", methods=["POST"])
@login_required
def grade_submission(submission_id):

    submission = Submission.query.get_or_404(submission_id)

    marks = int(request.form["marks_obtained"])

    feedback = request.form["feedback"]

    submission.marks_obtained = marks

    submission.feedback = feedback

    submission.ai_marks = marks

    db.session.commit()

    flash("Submission corrected successfully", "success")

    return redirect("/submissions")


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/bulk-import", methods=["GET", "POST"])
@login_required
def bulk_import():

    import pandas as pd
    from werkzeug.security import generate_password_hash

    if request.method == "POST":

        file = request.files["excel_file"]

        filepath = "uploads/students.xlsx"

        file.save(filepath)

        df = pd.read_excel(filepath)

        for _, row in df.iterrows():

            exists = User.query.filter_by(
                username=row["username"]
            ).first()

            if not exists:

                user = User(
                    username=row["username"],
                    email=row["email"],
                    password=generate_password_hash("student123"),
                    role="student",
                    full_name=row["full_name"],
                    department=row["department"],
                    section=row["section"],
                    semester=row["semester"]
                )

                db.session.add(user)

        db.session.commit()

        flash("Students imported successfully", "success")

    return """
    <h1>Bulk Student Import</h1>
    <form method='POST' enctype='multipart/form-data'>
        <input type='file' name='excel_file'>
        <button>Upload Excel</button>
    </form>
    """
