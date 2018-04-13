from datetime import datetime, timedelta

from main.models import Attendance


def update_inactive_students():
    today = datetime.now()
    students = User.objects.filter(is_staff=False, is_superuser=False)
    # TODO: Add class management config model to fetch this value
    num_days_of_inactivity = 5
    attend_dict = {}

    for i in range(num_days_of_inactivity):
        date = today - timedelta(i)
        for student in students:
            today_attendance = Attendance.objects.filter(class_date=date)
            for attend in today_attendance:
                if attend.user == student:
                    attend_dict[student.id] = attend_dict.get(student.id, 0) + 1
                    break

    for student in students:
        if attend_dict.get(student.id, 0) == 0:
            student.is_active = False
            student.save()
