# Campus Learning Hub

A complete Learning Management System built with **Python**, **Streamlit**, and **MySQL**. The project provides a clean campus-style interface for managing students, instructors, courses, enrollments, grades, and academic reports.

## Features

- Dashboard with enrollment, student, instructor, and course KPIs
- Session-based demo sign-in and account creation screen
- Student management with search, validation, add, update, and delete
- Instructor management with course assignment support
- Course management with instructor relationships
- Enrollment management with duplicate-enrollment protection
- Grade management with marks validation and generated total marks
- Reports for course popularity, instructor workload, student performance, and enrollment status
- MySQL foreign keys, unique constraints, cascading deletes, and check constraints
- Responsive Streamlit layout with campus branding and navigation

## Screenshots

The application opens with a branded campus login screen and continues to a dashboard with KPI cards, charts, and workspace navigation.

## Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit application and user interface |
| `db.py` | MySQL connection and database helper functions |
| `lms_database.sql` | Database schema, constraints, and sample data |
| `lms_queries.sql` | SQL CRUD statements and business reports |
| `01_setup_and_connection.ipynb` | Creates and verifies the database |
| `02_crud_operations.ipynb` | Demonstrates CRUD operations and constraints |
| `03_reports_and_kpis.ipynb` | Demonstrates reports and KPI queries |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example database environment configuration |

## Requirements

- Python 3.10 or newer
- MySQL Server 8.0 or newer
- VS Code with the Python and Jupyter extensions (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/javeriazahid/Campus-Learning-Hub.git
   cd Campus-Learning-Hub
   ```

2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database connection. Copy `.env.example` to `.env`, then set your MySQL password:

   ```text
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   ```

   The application reads these values from environment variables. Do not commit `.env` or real credentials.

4. Create the database:

   - Open `01_setup_and_connection.ipynb` in VS Code and run the cells, or
   - Run `lms_database.sql` from MySQL Workbench.

## Run the application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

For the presentation-only demo login:

```text
Email: admin@campus.edu
Password: admin123
```

The demo accounts are stored only in the current Streamlit session. A production system should store users in MySQL and hash passwords.

## Database design

- `students` and `instructors` use unique email addresses.
- `courses` reference instructors through a foreign key.
- `enrollments` connect students and courses and prevent duplicate pairs.
- `grades` belong to one enrollment and calculate `total_marks` automatically.
- Deleting a student removes related enrollments and grades.
- Courses and instructors with dependent records cannot be deleted.

## Troubleshooting

- **Access denied:** verify `MYSQL_USER` and `MYSQL_PASSWORD`.
- **Cannot connect to MySQL:** start the MySQL service and confirm `MYSQL_HOST`.
- **Unknown database `lms_db`:** run `lms_database.sql` or the setup notebook first.
- **Missing Python package:** run `pip install -r requirements.txt` again using the same Python interpreter selected by VS Code.

## Academic scope

This project demonstrates a relational LMS database, CRUD workflows, integrity constraints, and reporting dashboards. The authentication screen is included as a presentation layer; authentication data is intentionally not part of the academic database schema.
