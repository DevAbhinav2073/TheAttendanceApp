from django.contrib import admin

# Register your models here.
from apps.information.models import Programme


class ProgrammeAdmin(admin.ModelAdmin):
    pass



admin.site.register(Programme, ProgrammeAdmin)
