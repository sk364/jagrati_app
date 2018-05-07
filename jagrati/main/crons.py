from datetime import datetime, timedelta

from main.models import Attendance, Config


def update_inactive_students():
    today = datetime.now()
    students = User.objects.filter(is_staff=False, is_superuser=False)
    config = Config.objects.all().first()

    if config is None:
        config = Config.objects.create()

    num_days_of_inactivity = config.num_inactive_student_days
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
