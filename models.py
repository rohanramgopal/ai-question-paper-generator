from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject = db.Column(db.String(120), nullable=False)
    topic = db.Column(db.String(120), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    marks = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)

    bloom_level = db.Column(db.String(50), default="Understand")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Question {self.subject} - {self.topic}>"