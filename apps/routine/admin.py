from django.contrib import admin

# Register your models here.
from apps.routine.models import Routine, RoutineDetail, ClassAttendingDetail


class RoutineAdmin(admin.ModelAdmin):
    list_display = ('year', 'part', 'programme', 'group')


class RoutineDetailAdmin(admin.ModelAdmin):
    list_display = ('from_time', 'to_time', 'room', 'day_of_week', 'routine_of', 'subject')
    filter_horizontal = ('teachers',)


class ClassAttendingDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(ClassAttendingDetail, ClassAttendingDetailAdmin)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(RoutineDetail, RoutineDetailAdmin)
