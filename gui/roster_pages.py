import streamlit as st


def show_roster_page(manager):
    st.title("Daily Roster")

    st.subheader("View Lessons")

    day = st.selectbox(
        "Select a day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    lessons = manager.get_lessons_for_day(day)

    if lessons:
        for lesson in lessons:
            st.write(
                f"**{lesson['course_name']}** | "
                f"Time: {lesson['time']} | "
                f"Room: {lesson['room']}"
            )
    else:
        st.info("No lessons scheduled for this day.")

    st.divider()

    st.subheader("Student Check-in")

    with st.form("check_in_form"):
        student_id = st.number_input(
            "Student ID",
            min_value=1,
            step=1
        )

        course_id = st.number_input(
            "Course ID",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button("Check In Student")

        if submitted:
            success = manager.check_in(
                int(student_id),
                int(course_id)
            )

            if success:
                st.success("Student checked in successfully.")
            else:
                st.error("Check-in failed. Please check the Student ID and Course ID.")