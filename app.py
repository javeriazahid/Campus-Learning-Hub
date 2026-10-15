import re
from datetime import date

import streamlit as st
from mysql.connector import Error

from db import friendly_error, run_command, run_query

st.set_page_config(page_title="Learning Management System", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {
        --navy: #102a43;
        --blue: #1976d2;
        --sky: #eaf4ff;
        --ink: #17324d;
        --muted: #6b7c93;
        --gold: #f2b84b;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 12%, rgba(116, 185, 255, .18), transparent 28rem),
            radial-gradient(circle at 92% 84%, rgba(242, 184, 75, .13), transparent 24rem),
            #edf5fc;
        color: var(--ink);
        font-family: "DM Sans", sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102a43 0%, #163f63 100%);
        border-right: 0;
    }

    [data-testid="stSidebar"] * { color: #f5f9ff; }
    [data-testid="stSidebar"] .stRadio label { padding: 0.35rem 0; }

    h1, h2, h3 { font-family: "DM Sans", sans-serif; color: var(--navy); }
    .brand {
        padding: 1.2rem 0 2rem;
        text-align: center;
    }
    .brand-mark {
        display: inline-flex;
        width: 3.2rem;
        height: 3.2rem;
        align-items: center;
        justify-content: center;
        border-radius: 1rem;
        background: var(--gold);
        color: var(--navy);
        font-size: 1.7rem;
        font-weight: 700;
    }
    .brand-title { margin: 0.6rem 0 0; font-size: 1.1rem; font-weight: 700; }
    .brand-subtitle { margin: 0.2rem 0 0; color: #b9d4eb !important; font-size: 0.75rem; }
    .auth-shell {
        background: rgba(255, 255, 255, .5);
        border-radius: 1.5rem;
        margin: 2rem auto;
        max-width: 560px;
        padding: 1.5rem 2rem 2rem;
    }
    .top-nav {
        align-items: center;
        background: #102a43;
        border-bottom: 4px solid #f2b84b;
        display: flex;
        justify-content: space-between;
        margin: -5rem -5rem 0;
        padding: 1rem 5rem;
    }
    .top-nav-brand {
        align-items: center;
        color: white;
        display: flex;
        font-size: 1.05rem;
        font-weight: 700;
        gap: .65rem;
    }
    .top-nav-mark {
        align-items: center;
        background: var(--gold);
        border-radius: .55rem;
        color: var(--navy);
        display: inline-flex;
        height: 2rem;
        justify-content: center;
        width: 2rem;
    }
    .top-nav-links {
        color: #d8e8f7;
        display: flex;
        font-size: .86rem;
        gap: 1.6rem;
    }
    .top-nav-links span:first-child { color: #f2b84b; font-weight: 700; }
    .auth-kicker {
        color: var(--blue);
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
        text-align: center;
    }
    .auth-heading {
        color: var(--navy);
        font-family: "Playfair Display", serif;
        font-size: 2.15rem;
        line-height: 1.1;
        margin: .35rem 0 .45rem;
        text-align: center;
    }
    .auth-copy {
        color: var(--muted);
        font-size: .92rem;
        margin: 0 auto 1.2rem;
        max-width: 460px;
        text-align: center;
    }
    [data-testid="stImage"] img {
        border-radius: 1.1rem;
        max-height: 260px;
        object-fit: cover;
        box-shadow: 0 12px 28px rgba(16,42,67,.12);
    }

    .hero {
        min-height: 245px;
        padding: 2.4rem 2.7rem;
        border-radius: 1.25rem;
        background: linear-gradient(90deg, rgba(16,42,67,.96) 0%, rgba(16,42,67,.78) 48%, rgba(16,42,67,.22) 100%),
                    url("https://images.unsplash.com/photo-1564981797816-1043664bf78d?auto=format&fit=crop&w=1500&q=85") center/cover;
        box-shadow: 0 14px 35px rgba(16,42,67,.16);
        color: white;
        margin-bottom: 1.4rem;
    }
    .hero h1 { color: white; font-family: "Playfair Display", serif; font-size: 2.45rem; margin: 0 0 .4rem; }
    .hero p { color: #d8e8f7; max-width: 550px; margin: 0; font-size: 1rem; }
    .eyebrow { color: var(--gold); text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; font-weight: 700; }

    .metric-card {
        background: white;
        border: 1px solid #e3ebf4;
        border-radius: 1rem;
        padding: 1.15rem 1.2rem;
        box-shadow: 0 8px 20px rgba(16,42,67,.06);
    }
    .metric-label { color: var(--muted); font-size: .82rem; font-weight: 600; }
    .metric-value { color: var(--navy); font-size: 1.8rem; font-weight: 700; margin-top: .3rem; }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e3ebf4;
        border-radius: 1rem;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 20px rgba(16,42,67,.06);
    }
    div[data-testid="stMetric"] label { color: var(--muted); }
    div[data-testid="stMetricValue"] { color: var(--navy); }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: .6rem;
        border: 0;
        background: var(--blue);
        color: white;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

STUDENT_STATUS = ["Active", "Inactive", "Graduated"]
INSTRUCTOR_STATUS = ["Active", "Inactive"]
COURSE_STATUS = ["Active", "Inactive"]
ENROLLMENT_STATUS = ["Enrolled", "Completed", "Dropped"]
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PHONE_PATTERN = r"^\+?[0-9-]{10,15}$"

REPORTS = {
    "BR-01 Courses with the most students": (
        """SELECT c.course_name, COUNT(e.enrollment_id) AS enrolled_students
           FROM courses c
           INNER JOIN enrollments e ON e.course_id = c.course_id
           WHERE e.status <> 'Dropped'
           GROUP BY c.course_id, c.course_name
           ORDER BY enrolled_students DESC""",
        "course_name", "enrolled_students"),
    "BR-02 Courses per instructor": (
        """SELECT i.full_name AS instructor, COUNT(c.course_id) AS courses_taught
           FROM instructors i
           LEFT JOIN courses c ON c.instructor_id = i.instructor_id
           GROUP BY i.instructor_id, i.full_name
           ORDER BY courses_taught DESC, i.full_name""",
        "instructor", "courses_taught"),
    "BR-03 Students with the highest total marks": (
        """SELECT s.full_name AS student, SUM(g.total_marks) AS total_marks
           FROM students s
           INNER JOIN enrollments e ON e.student_id = s.student_id
           INNER JOIN grades g ON g.enrollment_id = e.enrollment_id
           GROUP BY s.student_id, s.full_name
           ORDER BY total_marks DESC
           LIMIT 10""",
        "student", "total_marks"),
    "BR-04 Active students": (
        "SELECT COUNT(*) AS active_students FROM students WHERE status = 'Active'",
        None, None),
    "BR-05 Enrollments by status": (
        "SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status ORDER BY total DESC",
        "status", "total"),
    "BR-06 Courses with no students": (
        """SELECT c.course_id, c.course_name
           FROM courses c
           LEFT JOIN enrollments e ON e.course_id = c.course_id
           WHERE e.enrollment_id IS NULL""",
        None, None),
    "Instructor workload": (
        """SELECT i.full_name AS instructor,
                  COUNT(DISTINCT c.course_id) AS courses,
                  COUNT(e.enrollment_id) AS students_taught
           FROM instructors i
           LEFT JOIN courses c ON c.instructor_id = i.instructor_id
           LEFT JOIN enrollments e ON e.course_id = c.course_id AND e.status <> 'Dropped'
           GROUP BY i.instructor_id, i.full_name
           ORDER BY students_taught DESC""",
        "instructor", "students_taught"),
    "Student performance": (
        """SELECT s.full_name AS student, c.course_name AS course, g.total_marks,
                  CASE
                      WHEN g.total_marks >= 85 THEN 'A'
                      WHEN g.total_marks >= 70 THEN 'B'
                      WHEN g.total_marks >= 55 THEN 'C'
                      WHEN g.total_marks >= 40 THEN 'D'
                      ELSE 'F'
                  END AS grade
           FROM grades g
           INNER JOIN enrollments e ON e.enrollment_id = g.enrollment_id
           INNER JOIN students s ON s.student_id = e.student_id
           INNER JOIN courses c ON c.course_id = e.course_id
           ORDER BY g.total_marks DESC""",
        None, None),
}


def execute(sql, params, message):
    try:
        run_command(sql, params)
    except Error as error:
        st.error(friendly_error(error))
        return
    st.session_state["flash"] = message
    st.rerun()


def with_label(df, *columns):
    df["label"] = df[list(columns)].astype(str).agg(" - ".join, axis=1) if len(df) else []
    return df


def pick(label, df, id_col, key, current=None):
    if df.empty:
        st.info("No records available.")
        return None
    ids = df[id_col].tolist()
    names = dict(zip(df[id_col], df["label"]))
    index = ids.index(current) if current in ids else 0
    return st.selectbox(label, ids, index=index, format_func=lambda i: names[i], key=key)


def record(df, id_col, value):
    return next(row for row in df.to_dict("records") if row[id_col] == value)


def searchable(df, key):
    text = st.text_input("Search", key=key, placeholder="Type to filter the table")
    df = df.drop(columns=["label"], errors="ignore")
    if text:
        mask = df.astype(str).apply(lambda col: col.str.contains(text, case=False, regex=False)).any(axis=1)
        df = df[mask]
    st.dataframe(df, hide_index=True)


def bar(df, x, y):
    if not df.empty:
        st.bar_chart(df, x=x, y=y)


def sign_out():
    st.session_state["authenticated"] = False
    st.session_state.pop("user_email", None)
    st.session_state.pop("flash", None)


def auth_screen():
    """Presentation-only authentication until a users table is added to the schema."""
    if "accounts" not in st.session_state:
        st.session_state["accounts"] = {"admin@campus.edu": "admin123"}

    st.markdown(
        """
        <nav class="top-nav">
            <div class="top-nav-brand">
                <span class="top-nav-mark">⌂</span>
                <span>Campus LMS</span>
            </div>
            <div class="top-nav-links">
                <span>Home</span>
                <span>Programs</span>
                <span>About us</span>
                <span>Support</span>
            </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )
    _, center, _ = st.columns([1, 1.25, 1])
    with center:
        st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="brand" style="padding-bottom: 1rem;">
                <div class="brand-mark">⌂</div>
            </div>
            <div class="auth-kicker">Campus learning hub</div>
            <div class="auth-heading">Welcome to Campus LMS</div>
            <p class="auth-copy">Manage learning, people, and progress in one beautifully organized workspace.</p>
            """,
            unsafe_allow_html=True,
        )
        st.image(
            "https://images.unsplash.com/photo-1564981797816-1043664bf78d?auto=format&fit=crop&w=1000&q=80",
            use_container_width=True,
        )
        login_tab, signup_tab = st.tabs(["Sign in", "Create account"])
        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@campus.edu")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
            if submitted:
                if st.session_state["accounts"].get(email.strip().lower()) == password:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email.strip().lower()
                    st.rerun()
                else:
                    st.error("Incorrect email or password.")
            st.caption("Demo access: admin@campus.edu / admin123")
        with signup_tab:
            with st.form("signup_form"):
                email = st.text_input("Email", placeholder="you@campus.edu", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm = st.text_input("Confirm password", type="password")
                submitted = st.form_submit_button("Create account", use_container_width=True)
            if submitted:
                email = email.strip().lower()
                if not re.match(EMAIL_PATTERN, email):
                    st.error("Enter a valid email address.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif email in st.session_state["accounts"]:
                    st.error("An account with this email already exists.")
                else:
                    st.session_state["accounts"][email] = password
                    st.success("Account created. You can now sign in.")
        st.markdown("</div>", unsafe_allow_html=True)


def crud_page(title, table, id_col, loader, form, validate, insert_sql, update_sql,
              edit_form=None, view=None, delete_note=""):
    edit_form = edit_form or form
    st.title(title)
    view_tab, add_tab, update_tab, delete_tab = st.tabs(["View", "Add", "Update", "Delete"])

    with view_tab:
        if view:
            view()
        else:
            searchable(loader(), f"{table}_search")

    with add_tab:
        with st.form(f"{table}_add"):
            values = form(f"{table}_add")
            submitted = st.form_submit_button("Add")
        if submitted:
            error = validate(values)
            if error:
                st.error(error)
            else:
                execute(insert_sql, values, "Record added successfully.")

    with update_tab:
        data = loader()
        chosen = pick("Select record", data, id_col, f"{table}_update_pick")
        if chosen is not None:
            row = record(data, id_col, chosen)
            with st.form(f"{table}_update"):
                values = edit_form(f"{table}_update_{chosen}", row)
                submitted = st.form_submit_button("Save changes")
            if submitted:
                error = validate(values)
                if error:
                    st.error(error)
                else:
                    execute(update_sql, (*values, chosen), "Record updated successfully.")

    with delete_tab:
        data = loader()
        chosen = pick("Select record to delete", data, id_col, f"{table}_delete_pick")
        if chosen is not None:
            if delete_note:
                st.warning(delete_note)
            confirmed = st.checkbox("I understand this cannot be undone", key=f"{table}_confirm_{chosen}")
            if st.button("Delete record", key=f"{table}_delete", disabled=not confirmed):
                execute(f"DELETE FROM {table} WHERE {id_col} = %s", (chosen,), "Record deleted.")


def check_person(name, email, phone="0300-0000000"):
    if not name:
        return "Name is required."
    if not re.match(EMAIL_PATTERN, email):
        return "Enter a valid email address."
    if not re.match(PHONE_PATTERN, phone):
        return "Enter a valid phone number, for example 0300-1234567."
    return None


def load_students():
    return with_label(run_query("SELECT * FROM students ORDER BY full_name"), "full_name")


def load_instructors():
    return with_label(run_query("SELECT * FROM instructors ORDER BY full_name"), "full_name")


def load_courses():
    df = run_query("""SELECT c.course_id, c.course_name, c.description, c.instructor_id,
                             i.full_name AS instructor, c.duration_weeks, c.fee, c.status
                      FROM courses c
                      INNER JOIN instructors i ON i.instructor_id = c.instructor_id
                      ORDER BY c.course_name""")
    return with_label(df, "course_name")


def load_enrollments():
    df = run_query("""SELECT e.enrollment_id, s.full_name AS student, c.course_name AS course,
                             e.enrollment_date, e.status
                      FROM enrollments e
                      INNER JOIN students s ON s.student_id = e.student_id
                      INNER JOIN courses c ON c.course_id = e.course_id
                      ORDER BY e.enrollment_date DESC""")
    return with_label(df, "student", "course")


def load_grades():
    df = run_query("""SELECT g.grade_id, s.full_name AS student, c.course_name AS course,
                             g.assignment_marks, g.quiz_marks, g.final_marks, g.total_marks,
                             CASE
                                 WHEN g.total_marks >= 85 THEN 'A'
                                 WHEN g.total_marks >= 70 THEN 'B'
                                 WHEN g.total_marks >= 55 THEN 'C'
                                 WHEN g.total_marks >= 40 THEN 'D'
                                 ELSE 'F'
                             END AS grade
                      FROM grades g
                      INNER JOIN enrollments e ON e.enrollment_id = g.enrollment_id
                      INNER JOIN students s ON s.student_id = e.student_id
                      INNER JOIN courses c ON c.course_id = e.course_id
                      ORDER BY g.total_marks DESC""")
    return with_label(df, "student", "course")


def dashboard():
    kpi = run_query("""SELECT (SELECT COUNT(*) FROM students) AS students,
                              (SELECT COUNT(*) FROM students WHERE status = 'Active') AS active_students,
                              (SELECT COUNT(*) FROM instructors) AS instructors,
                              (SELECT COUNT(*) FROM courses) AS courses,
                              (SELECT COUNT(*) FROM enrollments) AS enrollments""").iloc[0]
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Campus learning hub</div>
            <h1>Grow, learn, and lead.</h1>
            <p>One calm, connected workspace for your students, instructors, courses, enrollments, and academic progress.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    labels = [("Students", "students"), ("Active students", "active_students"),
              ("Instructors", "instructors"), ("Courses", "courses"), ("Enrollments", "enrollments")]
    for column, (label, key) in zip(st.columns(len(labels)), labels):
        column.metric(label, int(kpi[key]))

    left, right = st.columns(2)
    with left:
        st.subheader("Enrollments by status")
        bar(run_query("SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status"), "status", "total")
    with right:
        st.subheader("Most popular courses")
        sql, x, y = REPORTS["BR-01 Courses with the most students"]
        bar(run_query(sql), x, y)

    st.subheader("Latest enrollments")
    latest = load_enrollments().drop(columns=["label", "enrollment_id"]).head(8)
    st.dataframe(latest, hide_index=True)


def student_view():
    search_col, status_col = st.columns([3, 1])
    text = search_col.text_input("Search by name or email", key="student_search")
    status = status_col.selectbox("Status", ["All"] + STUDENT_STATUS, key="student_status_filter")
    sql = "SELECT * FROM students WHERE (full_name LIKE %s OR email LIKE %s)"
    params = [f"%{text}%", f"%{text}%"]
    if status != "All":
        sql += " AND status = %s"
        params.append(status)
    st.dataframe(run_query(sql + " ORDER BY full_name", params), hide_index=True)


def student_form(key, row=None):
    row = row or {}
    name = st.text_input("Full name", row.get("full_name", ""), key=f"{key}_name")
    email = st.text_input("Email", row.get("email", ""), key=f"{key}_email")
    phone = st.text_input("Phone", row.get("phone", ""), key=f"{key}_phone")
    joined = st.date_input("Enrollment date", row.get("enrollment_date", date.today()), key=f"{key}_date")
    status = st.selectbox("Status", STUDENT_STATUS,
                          index=STUDENT_STATUS.index(row.get("status", "Active")), key=f"{key}_status")
    return (name or "").strip(), (email or "").strip(), (phone or "").strip(), joined, status


def students_page():
    crud_page(
        "Students", "students", "student_id", load_students, student_form,
        lambda v: check_person(v[0], v[1], v[2]),
        "INSERT INTO students (full_name, email, phone, enrollment_date, status) VALUES (%s, %s, %s, %s, %s)",
        "UPDATE students SET full_name = %s, email = %s, phone = %s, enrollment_date = %s, status = %s "
        "WHERE student_id = %s",
        view=student_view,
        delete_note="The enrollments and grades of this student will be deleted as well.",
    )


def instructor_form(key, row=None):
    row = row or {}
    name = st.text_input("Full name", row.get("full_name", ""), key=f"{key}_name")
    email = st.text_input("Email", row.get("email", ""), key=f"{key}_email")
    specialization = st.text_input("Specialization", row.get("specialization", ""), key=f"{key}_spec")
    status = st.selectbox("Status", INSTRUCTOR_STATUS,
                          index=INSTRUCTOR_STATUS.index(row.get("status", "Active")), key=f"{key}_status")
    return (name or "").strip(), (email or "").strip(), (specialization or "").strip(), status


def check_instructor(values):
    name, email, specialization, _ = values
    return check_person(name, email) or ("Specialization is required." if not specialization else None)


def instructors_page():
    crud_page(
        "Instructors", "instructors", "instructor_id", load_instructors, instructor_form, check_instructor,
        "INSERT INTO instructors (full_name, email, specialization, status) VALUES (%s, %s, %s, %s)",
        "UPDATE instructors SET full_name = %s, email = %s, specialization = %s, status = %s "
        "WHERE instructor_id = %s",
        delete_note="An instructor who still teaches a course cannot be deleted.",
    )


def course_form(key, row=None):
    row = row or {}
    name = st.text_input("Course name", row.get("course_name", ""), key=f"{key}_name")
    description = st.text_area("Description", row.get("description") or "", key=f"{key}_description")
    instructor = pick("Instructor", load_instructors(), "instructor_id", f"{key}_instructor",
                      row.get("instructor_id"))
    duration = st.number_input("Duration (weeks)", min_value=1, value=int(row.get("duration_weeks", 8)),
                               step=1, key=f"{key}_duration")
    fee = st.number_input("Fee (PKR)", min_value=0.0, value=float(row.get("fee", 20000.0)),
                          step=500.0, key=f"{key}_fee")
    status = st.selectbox("Status", COURSE_STATUS,
                          index=COURSE_STATUS.index(row.get("status", "Active")), key=f"{key}_status")
    return (name or "").strip(), (description or "").strip(), instructor, int(duration), float(fee), status


def check_course(values):
    if not values[0]:
        return "Course name is required."
    if values[2] is None:
        return "Select an instructor first."
    return None


def courses_page():
    crud_page(
        "Courses", "courses", "course_id", load_courses, course_form, check_course,
        "INSERT INTO courses (course_name, description, instructor_id, duration_weeks, fee, status) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        "UPDATE courses SET course_name = %s, description = %s, instructor_id = %s, duration_weeks = %s, "
        "fee = %s, status = %s WHERE course_id = %s",
        delete_note="A course that has enrollments cannot be deleted.",
    )


def enrollment_form(key, row=None):
    student = pick("Student", load_students(), "student_id", f"{key}_student")
    course = pick("Course", load_courses(), "course_id", f"{key}_course")
    enrolled_on = st.date_input("Enrollment date", date.today(), key=f"{key}_date")
    status = st.selectbox("Status", ENROLLMENT_STATUS, key=f"{key}_status")
    return student, course, enrolled_on, status


def enrollment_status_form(key, row):
    st.write(f"{row['student']} in {row['course']}")
    return (st.selectbox("Status", ENROLLMENT_STATUS,
                         index=ENROLLMENT_STATUS.index(row["status"]), key=f"{key}_status"),)


def check_enrollment(values):
    if len(values) == 4 and (values[0] is None or values[1] is None):
        return "Select both a student and a course."
    return None


def enrollments_page():
    crud_page(
        "Enrollments", "enrollments", "enrollment_id", load_enrollments, enrollment_form, check_enrollment,
        "INSERT INTO enrollments (student_id, course_id, enrollment_date, status) VALUES (%s, %s, %s, %s)",
        "UPDATE enrollments SET status = %s WHERE enrollment_id = %s",
        edit_form=enrollment_status_form,
        delete_note="The grade linked to this enrollment will be deleted as well.",
    )


def ungraded_enrollments():
    df = run_query("""SELECT e.enrollment_id, s.full_name AS student, c.course_name AS course
                      FROM enrollments e
                      INNER JOIN students s ON s.student_id = e.student_id
                      INNER JOIN courses c ON c.course_id = e.course_id
                      LEFT JOIN grades g ON g.enrollment_id = e.enrollment_id
                      WHERE g.grade_id IS NULL AND e.status <> 'Dropped'
                      ORDER BY s.full_name""")
    return with_label(df, "student", "course")


def marks_inputs(key, row):
    assignment = st.number_input("Assignment (out of 20)", 0.0, 20.0, float(row.get("assignment_marks", 0.0)),
                                 step=0.5, key=f"{key}_assignment")
    quiz = st.number_input("Quiz (out of 20)", 0.0, 20.0, float(row.get("quiz_marks", 0.0)),
                           step=0.5, key=f"{key}_quiz")
    final = st.number_input("Final exam (out of 60)", 0.0, 60.0, float(row.get("final_marks", 0.0)),
                            step=0.5, key=f"{key}_final")
    return assignment, quiz, final


def grade_form(key, row=None):
    enrollment = pick("Enrollment", ungraded_enrollments(), "enrollment_id", f"{key}_enrollment")
    return (enrollment, *marks_inputs(key, {}))


def grade_edit_form(key, row):
    st.write(f"{row['student']} in {row['course']}")
    return marks_inputs(key, row)


def check_grade(values):
    if len(values) == 4 and values[0] is None:
        return "There is no enrollment waiting for marks."
    return None


def grades_page():
    crud_page(
        "Grades", "grades", "grade_id", load_grades, grade_form, check_grade,
        "INSERT INTO grades (enrollment_id, assignment_marks, quiz_marks, final_marks) VALUES (%s, %s, %s, %s)",
        "UPDATE grades SET assignment_marks = %s, quiz_marks = %s, final_marks = %s WHERE grade_id = %s",
        edit_form=grade_edit_form,
    )


def reports_page():
    st.title("Reports")
    name = st.selectbox("Choose a report", list(REPORTS))
    sql, x, y = REPORTS[name]
    result = run_query(sql)
    st.dataframe(result, hide_index=True)
    if x and y:
        bar(result, x, y)


PAGES = {
    "Dashboard": dashboard,
    "Students": students_page,
    "Instructors": instructors_page,
    "Courses": courses_page,
    "Enrollments": enrollments_page,
    "Grades": grades_page,
    "Reports": reports_page,
}

if not st.session_state.get("authenticated"):
    auth_screen()
    st.stop()

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-mark">⌂</div>
        <p class="brand-title">Campus LMS</p>
        <p class="brand-subtitle">Learning made simple</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.caption(st.session_state.get("user_email", "Administrator"))
page = st.sidebar.radio("Workspace", list(PAGES), format_func=lambda item: {
    "Dashboard": "⌂  Dashboard",
    "Students": "◉  Students",
    "Instructors": "◉  Instructors",
    "Courses": "▣  Courses",
    "Enrollments": "↗  Enrollments",
    "Grades": "★  Grades",
    "Reports": "▤  Reports",
}[item])
st.sidebar.button("Sign out", use_container_width=True, on_click=sign_out)
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))
try:
    PAGES[page]()
except Error as error:
    st.error(friendly_error(error))
