from django.contrib import admin

from .models import Attendance, Class, StudentProfile, UserProfile


class AttendanceAdmin(admin.ModelAdmin):
    pass


class ClassAdmin(admin.ModelAdmin):
    pass


class StudentProfileAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
