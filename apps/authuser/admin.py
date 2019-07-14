# Register your models here.
import csv
import io

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.authuser.forms import DetailsForUploadingStudentCSVForm, DetailsForUploadingTeacherCSVForm
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
    list_display = ('username', 'password_text')

    def password_text(self, obj):
        if hasattr(obj, 'student_detail'):
            return obj.student_detail.password
        elif hasattr(obj, 'teacher_detail'):
            return obj.teacher_detail.password

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        model_object = self.get_object(request, object_id)
        if model_object:
            if model_object.user_type == USER_TYPE_STUDENT:
                self.inlines = [StudentDetailInline, ]
            elif model_object.user_type == USER_TYPE_TEACHER:
                self.inlines = [TeacherDetailInline, ]
        return super().changeform_view(request, object_id, form_url, extra_context)


class StudentDetailAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('name', 'email', 'password', 'phone', 'batch',
                    'programme', 'roll_number', 'current_year', 'current_part',
                    'group',)
    change_list_template = 'admin/authuser/authuser_student_change_list.html'

    def get_urls(self, *args, **kwargs):
        urls = super().get_urls(*args, **kwargs)
        custom_urls = [
            path('upload-student-csv', self.admin_site.admin_view(self.handle_csv_upload),
                 name='handle-student-csv-upload')
        ]
        return custom_urls + urls

    @staticmethod
    def create_student_record_from_uploaded_csv(csv_file, batch, programme):
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string, delimiter=',', quotechar='|')
        list_of_created_username = []
        for row in reader:
            name = row.get(NAME_FIELD)
            email = row.get(EMAIL_FIELD)
            roll_number = row.get(ROLL_NUMBER_FIELD)
            phone = row.get(PHONE_FIELD, None)
            group = row.get(GROUP_FIELD)

            try:
                student_detail = StudentDetail.objects.create(email=email,
                                                              name=name,
                                                              roll_number=roll_number,
                                                              programme=programme,
                                                              batch=batch,
                                                              group=group,
                                                              phone=phone)
                list_of_created_username.append(email)
            except IntegrityError as e:
                for username in list_of_created_username:
                    User.objects.get(username=username).delete()
                raise IntegrityError(
                    'A student with email %s is already registered. Please handle this manually.' % (
                        email,))

    def handle_csv_upload(self, request, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            form = DetailsForUploadingStudentCSVForm
        else:
            form = DetailsForUploadingStudentCSVForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    batch = form.cleaned_data.get('batch')
                    programme = form.cleaned_data.get('programme')
                    csv_file = request.FILES['csv_file']
                    self.create_student_record_from_uploaded_csv(csv_file, batch, programme)
                    return redirect(reverse('admin:authuser_studentdetail_changelist'))
                except Exception as e:
                    self.message_user(request, 'Failure: ' + str(e), messages.ERROR)

        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = 'Upload .csv file with students detail'
        return TemplateResponse(
            request,
            'admin/authuser/upload_csv.html',
            context,
        )


class TeacherDetailAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('name', 'email', 'phone', 'subjects', 'password')
    change_list_template = 'admin/authuser/authuser_teacher_change_list.html'

    def get_urls(self, *args, **kwargs):
        urls = super().get_urls(*args, **kwargs)
        custom_urls = [
            path('upload-teacher-csv', self.admin_site.admin_view(self.handle_csv_upload),
                 name='handle-teacher-csv-upload')
        ]
        return custom_urls + urls

    @staticmethod
    def create_student_record_from_uploaded_csv(csv_file, department):
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string, delimiter=',', quotechar='|')
        list_of_created_username = []
        for row in reader:
            name = row.get(NAME_FIELD)
            email = row.get(EMAIL_FIELD)
            phone = row.get(PHONE_FIELD, None)

            try:
                teacher_detail = TeacherDetail.objects.create(email=email,
                                                              name=name,
                                                              department=department,
                                                              phone=phone)
                list_of_created_username.append(email)
            except IntegrityError as e:
                for username in list_of_created_username:
                    User.objects.get(username=username).delete()
                raise IntegrityError(
                    'A teacher with email %s is already registered. Please handle this manually.' % (
                        email,))

    def handle_csv_upload(self, request, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            form = DetailsForUploadingTeacherCSVForm
        else:
            form = DetailsForUploadingTeacherCSVForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    department = form.cleaned_data.get('department')
                    csv_file = request.FILES['csv_file']
                    self.create_student_record_from_uploaded_csv(csv_file, department)
                    return redirect(reverse('admin:authuser_teacherdetail_changelist'))
                except Exception as e:
                    self.message_user(request, 'Failure: ' + str(e), messages.ERROR)

        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = 'Upload .csv file with teacher detail'
        return TemplateResponse(
            request,
            'admin/authuser/upload_csv.html',
            context,
        )


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(StudentDetail, StudentDetailAdmin)
admin.site.register(TeacherDetail, TeacherDetailAdmin)
admin.site.register(User, NewUserAdmin)
admin.site.register(Department, DepartmentAdmin)

admin.site.site_header = 'Classroom Updates'
admin.site.site_title = 'Classroom Updates Admin'
admin.site.site_url = 'http://minor.abhinavdev.com.np/'
admin.site.index_title = 'Classroom Updates'
admin.empty_value_display = '----'
