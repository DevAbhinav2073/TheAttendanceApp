from django.contrib import admin

# Register your models here.
from apps.routine.models import Routine, RoutineDetail


class RoutineAdmin(admin.ModelAdmin):
    list_display = ('year', 'part', 'programme', 'group')


class RoutineDetailAdmin(admin.ModelAdmin):
    list_display = ('from_time', 'to_time', 'room','day_of_week', 'routine_of')


admin.site.register(Routine, RoutineAdmin)
admin.site.register(RoutineDetail, RoutineDetailAdmin)
