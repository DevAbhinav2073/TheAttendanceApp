# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.authuser.models import *

User = get_user_model()


class StudentDetailInline(admin.TabularInline):
    model = StudentDetail
    exclude = ()


class TeacherDetailInline(admin.TabularInline):
    model = TeacherDetail
    exclude = ()


class NewUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_type')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        model_object = self.get_object(request, object_id)
        if model_object:
            if model_object.user_type == USER_TYPE_STUDENT:
                self.inlines = [StudentDetailInline, ]
            elif model_object.user_type == USER_TYPE_TEACHER:
                self.inlines = [TeacherDetailInline, ]
        return super().changeform_view(request, object_id, form_url, extra_context)


admin.site.register(User, NewUserAdmin)
