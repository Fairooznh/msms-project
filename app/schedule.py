import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                
                # Load students
                for s_data in data.get("students", []):
                    student = StudentUser(s_data["id"], s_data["name"])
                    student.enrolled_course_ids = s_data.get("enrolled_course_ids", [])
                    self.students.append(student)
                
                # Load teachers
                for t_data in data.get("teachers", []):
                    teacher = TeacherUser(t_data["id"], t_data["name"], t_data.get("speciality", ""))
                    self.teachers.append(teacher)
                
                # Load courses
                for c_data in data.get("courses", []):
                    course = Course(c_data["id"], c_data["name"], c_data.get("instrument", ""), c_data.get("teacher_id"))
                    course.enrolled_student_ids = c_data.get("enrolled_student_ids", [])
                    course.lessons = c_data.get("lessons", [])
                    self.courses.append(course)

                # Load attendance log
                self.attendance_log = data.get("attendance", [])
                
                # Load or calculate counters
                self.next_student_id = data.get("next_student_id", max([s.id for s in self.students], default=0) + 1)
                self.next_teacher_id = data.get("next_teacher_id", max([t.id for t in self.teachers], default=0) + 1)
                self.next_course_id = data.get("next_course_id", max([c.id for c in self.courses], default=0) + 1)

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id
        }
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def register_new_student(self, name, instrument):
        """Registers a new student and saves the data"""
        student = StudentUser(self.next_student_id, name, instrument)
        self.students.append(student)
        self.next_student_id += 1
        self._save_data()
        return student
    
    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        self.attendance_log.append(check_in_record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def get_lessons_for_day(self, day):
        """Returns a list of lessons matching the specified day."""
        roster = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("day", "").lower() == day.lower():
                    roster.append({
                        "course_name": course.name,
                        "time": lesson.get("start_time"),
                        "room": lesson.get("room"),
                        "teacher_id": course.teacher_id
                    })
        return roster

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Switches a student from one course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Invalid Student ID or Course ID.")
            return False

        if from_course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(from_course_id)
        if student_id in from_course.enrolled_student_ids:
            from_course.enrolled_student_ids.remove(student_id)

        if to_course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(to_course_id)
        if student_id not in to_course.enrolled_student_ids:
            to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        print(f"Success: Student {student.name} switched from {from_course.name} to {to_course.name}.")
        return True