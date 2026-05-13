cd ~/ai-question-paper-generator

cat > README.md <<'EOF'
# 🧠 AI Powered Automated Question Paper Generator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![AI](https://img.shields.io/badge/AI-Smart_Selection-purple?style=for-the-badge)
![PDF](https://img.shields.io/badge/PDF-Generation-red?style=for-the-badge&logo=adobeacrobatreader)
![Status](https://img.shields.io/badge/Status-Working-success?style=for-the-badge)

---

## 📌 Overview

The **AI Powered Automated Question Paper Generator** is a smart examination management system designed for teachers, admins, and students.

It allows teachers/admins to create a large question bank, generate balanced question papers using AI-style selection logic, assign different papers to different students, allow students to download papers, upload PDF answer sheets, and enable admins to correct submissions with marks and feedback.

---

## 🚀 Key Features

- Admin login
- Student login
- Role-based dashboard
- Add and manage questions
- Subject-wise question bank
- Topic-wise syllabus coverage
- Difficulty levels: Easy, Medium, Hard
- Bloom taxonomy support
- 25 / 50 / 75 / 100 marks paper generation
- Unique paper generation for each student
- Assign paper directly to selected student
- Student downloads assigned question paper
- Student uploads answer sheet PDF
- Admin views submitted answer PDFs
- Admin downloads answer sheets
- Admin enters marks and feedback
- AI difficulty support
- AI answer evaluation module
- Plagiarism checker module
- Bulk student import support
- Professional dashboard UI
- PDF generation using ReportLab
- SQLite database

---

## 🧠 How It Works

1. Admin logs into the system.
2. Admin adds questions with subject, topic, marks, difficulty, and Bloom level.
3. Admin selects exam title, subject, student, marks, and difficulty distribution.
4. AI-style engine selects questions based on rules and randomness.
5. System generates a PDF question paper.
6. Paper appears in the assigned student's dashboard.
7. Student downloads the paper.
8. Student uploads answer sheet as PDF.
9. Admin views and downloads submissions.
10. Admin enters marks and feedback.

---

## 🏗️ Architecture Diagram

```mermaid
flowchart TD

A[Admin Login] --> B[Admin Dashboard]

B --> C[Question Management]
C --> C1[Add Questions]
C --> C2[Question Bank]
C --> C3[Subject and Topic Mapping]

B --> D[AI Paper Generation Engine]
D --> D1[Select Subject]
D --> D2[Select Topics]
D --> D3[Choose Difficulty Distribution]
D --> D4[Set Total Marks]
D --> D5[Assign Student]

D1 --> E[Question Database]
D2 --> E
D3 --> E
D4 --> E

E --> F[Smart Question Selection]
F --> F1[Difficulty Balance]
F --> F2[Syllabus Coverage]
F --> F3[Randomization]
F --> F4[Duplicate Prevention]

F --> G[PDF Generator]
G --> H[Generated Question Paper]

H --> I[Student Dashboard]
I --> J[Download Question Paper]
J --> K[Student Writes Answer]
K --> L[Upload Answer Sheet PDF]

L --> M[Submission Database]
M --> N[Admin Submission Portal]

N --> O[Download Answer Sheet]
O --> P[Manual Correction]
P --> Q[Marks and Feedback]

Q --> R[Student Result View]

subgraph AI_Modules
S1[Difficulty Classifier]
S2[AI Answer Evaluator]
S3[Plagiarism Checker]
end

F --> S1
P --> S2
P --> S3
