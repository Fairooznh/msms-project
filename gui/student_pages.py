import streamlit as st

def show_student_management_page(manager):
    st.title("Student Management")

    st.subheader("Register New Student")

    with st.form("register_student_form"):
        name = st.text_input("Student Name")
        instrument = st.text_input("Instrument")

        submitted = st.form_submit_button("Register Student")

        if submitted:
            if not name.strip():
                st.error("Please enter a student name.")
            elif not instrument.strip():
                st.error("Please enter an instrument.")
            else:
                student = manager.register_new_student(
                    name.strip(),
                    instrument.strip(),
                )

                st.success(
                    f"Student registered successfully! "
                    f"Student ID: {student.id}"
                )

    st.divider()

    st.subheader("Search Students")

    search_term = st.text_input(
        "Search by name, ID, or instrument"
    ).strip().lower()

    st.subheader("Students")

    if manager.students:
        for student in manager.students:
            if (
                not search_term
                or search_term in student.name.lower()
                or search_term in str(student.id)
                or search_term in student.instrument.lower()
            ):
                st.write(
                    f"**ID:** {student.id} | "
                    f"**Name:** {student.name} | "
                    f"**Instrument:** {student.instrument}"
                )
    else:
        st.info("No students registered.")