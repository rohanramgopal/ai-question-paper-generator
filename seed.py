from app import app
from models import db, Question

sample_questions = [
    {
        "subject": "Computer Science",
        "topic": "Python",
        "question_text": "Define variables in Python with an example.",
        "marks": 2,
        "difficulty": "Easy",
        "bloom_level": "Remember"
    },
    {
        "subject": "Computer Science",
        "topic": "Python",
        "question_text": "Explain list, tuple, and dictionary with examples.",
        "marks": 5,
        "difficulty": "Medium",
        "bloom_level": "Understand"
    },
    {
        "subject": "Computer Science",
        "topic": "Python",
        "question_text": "Write a Python program to implement file encryption and decryption.",
        "marks": 10,
        "difficulty": "Hard",
        "bloom_level": "Apply"
    },
    {
        "subject": "Computer Science",
        "topic": "DBMS",
        "question_text": "What is normalization in DBMS?",
        "marks": 2,
        "difficulty": "Easy",
        "bloom_level": "Remember"
    },
    {
        "subject": "Computer Science",
        "topic": "DBMS",
        "question_text": "Explain primary key, foreign key, and candidate key.",
        "marks": 5,
        "difficulty": "Medium",
        "bloom_level": "Understand"
    },
    {
        "subject": "Computer Science",
        "topic": "DBMS",
        "question_text": "Design an ER diagram for a college management system.",
        "marks": 10,
        "difficulty": "Hard",
        "bloom_level": "Create"
    },
    {
        "subject": "Computer Science",
        "topic": "Cybersecurity",
        "question_text": "Define phishing attack.",
        "marks": 2,
        "difficulty": "Easy",
        "bloom_level": "Remember"
    },
    {
        "subject": "Computer Science",
        "topic": "Cybersecurity",
        "question_text": "Explain the working of Nmap and Wireshark.",
        "marks": 5,
        "difficulty": "Medium",
        "bloom_level": "Understand"
    },
    {
        "subject": "Computer Science",
        "topic": "Cybersecurity",
        "question_text": "Explain how penetration testing is performed in a secure lab environment.",
        "marks": 10,
        "difficulty": "Hard",
        "bloom_level": "Analyze"
    }
]

with app.app_context():
    for data in sample_questions:
        question = Question(**data)
        db.session.add(question)

    db.session.commit()
    print("Sample questions inserted successfully.")