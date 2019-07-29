from django.contrib import admin

# Register your models here.
from apps.routine.models import Routine, RoutineDetail, ClassAttendingDetail, ArrivalTime, SemesterDetail, SMSCredit


class RoutineAdmin(admin.ModelAdmin):
    list_display = ('year', 'part', 'programme', 'group')


class RoutineDetailAdmin(admin.ModelAdmin):
    list_display = ('from_time', 'to_time', 'room', 'day_of_week', 'routine_of', 'subject')
    filter_horizontal = ('teachers',)


class ClassAttendingDetailAdmin(admin.ModelAdmin):
    pass


class ArrivalTimeAdmin(admin.ModelAdmin):
    pass


class SemesterDetailAdmin(admin.ModelAdmin):
    pass


class SMSCreditAdmin(admin.ModelAdmin):
    pass


admin.site.register(SMSCredit, SMSCreditAdmin)
admin.site.register(SemesterDetail, SemesterDetailAdmin)
admin.site.register(ClassAttendingDetail, ClassAttendingDetailAdmin)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(RoutineDetail, RoutineDetailAdmin)
admin.site.register(ArrivalTime, ArrivalTimeAdmin)
