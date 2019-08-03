from django.contrib import admin

# Register your models here.
from apps.information.models import Programme, Department


class ProgrammeAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Department, DepartmentAdmin)
