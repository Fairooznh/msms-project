import streamlit as st
from app.schedule import ScheduleManager

def launch():
    st.set_page_config(
        page_title="Music School Management System",
        layout="wide"
    )

    # Keep the ScheduleManager alive when moving between pages
    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    st.sidebar.title("MSMS")
    st.sidebar.write("Music School Management System")

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Student Management", "Daily Roster"]
    )

    if page == "Dashboard":
        st.title("Music School Management System")
        st.write("Welcome to the MSMS dashboard.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Students", len(manager.students))

        with col2:
            st.metric("Teachers", len(manager.teachers))

        with col3:
            st.metric("Courses", len(manager.courses))

    elif page == "Student Management":
        from gui.student_pages import show_student_management_page
        show_student_management_page(manager)

    elif page == "Daily Roster":
        from gui.roster_pages import show_roster_page
        show_roster_page(manager)