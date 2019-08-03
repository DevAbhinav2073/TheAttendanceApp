from django.contrib import admin

# Register your models here.
from apps.csv_uploader.admin import CsvUploadAdmin
from apps.im.models import *


class SubjectAdmin(admin.ModelAdmin):
    pass


class StudentAdmin(CsvUploadAdmin):
    pass


class ProgrammeAdmin(admin.ModelAdmin):
    pass


class MarksInstanceAdmin(admin.ModelAdmin):
    pass


class MarksDetailInstanceAdmin(admin.ModelAdmin):
    pass


class CourseDetailAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(MarksInstance, MarksInstanceAdmin)
admin.site.register(MarksDetail, MarksDetailInstanceAdmin)
admin.site.register(SubjectDetail, SubjectAdmin)
admin.site.register(CourseDetail, CourseDetailAdmin)

admin.site.site_header = 'IOE APP Admin'
admin.site.site_title = 'IOE APP Admin'
admin.site.index_title = 'IOE APP Administration'
admin.empty_value_display = '----'
