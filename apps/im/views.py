import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.im.serializers import MarksDetailSerializer
from apps.im.utils import get_remark, is_fail
from apps.im.utils import num2word
from apps.permissions import is_teacher, is_student, IsStudent
from apps.routine.utils import get_roman_value
from .forms import *


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@csrf_exempt
def get_students(request):
    response_data = []
    program = request.POST.get('prog', None)
    batch = request.POST.get('batch', None)
    group = request.POST.get('group', "A")
    students = Student.objects.filter(programme__short_form=program, batch=batch, group=group)
    for student in students:
        response_data.append([student.batch[1:], student.programme.short_form, student.roll_number, student.name])
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_subjects(request):
    program = request.POST.get('program', None)
    year = request.POST.get('year', None)
    part = request.POST.get('part', None)
    courser_details = CourseDetail.objects.filter(programme__short_form=program, year=get_roman_value(year),
                                                  part=get_roman_value(part))
    response_data = []
    for courser_detail in courser_details:
        response_data.append(
            [courser_detail.subject.subject_code, courser_detail.subject.name,
             str(courser_detail.subject.theory_full_marks), str(courser_detail.subject.practical_full_marks)])
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def display_result_ac_instance(request, marks_instance_id):
    mark_instance = MarksInstance.objects.filter(id=marks_instance_id).first()
    data = dict(
        batch=mark_instance.batch,
        group=mark_instance.group,
        pass_mark=mark_instance.pass_mark,
        full_mark=mark_instance.full_mark,
        program_name=mark_instance.programme.name,
        subject_name=mark_instance.subject.name,
        subject_code=mark_instance.subject.subject_code,
        year=mark_instance.year,
        part=mark_instance.part,
        date=mark_instance.date,
        examineer_name=mark_instance.name_of_examiner,
        th_pr_full=mark_instance.theory_practical,
    )
    mark_details = MarksDetail.objects.filter(marks_instance=mark_instance)
    students = []
    for idx, mark_detail in enumerate(mark_details):
        setattr(mark_detail.student, 'mark', mark_detail.marks)
        setattr(mark_detail.student, 'roll',
                '%s/%s/%s' % (mark_detail.student.batch[1:], mark_detail.student.programme.short_form,
                              mark_detail.student.roll_number))
        if not mark_detail.student.mark == '':
            if RepresentsInt(mark_detail.student.mark):
                setattr(mark_detail.student, 'mark_in_word', num2word(int(mark_detail.student.mark)))
            else:
                setattr(mark_detail.student, 'mark_in_word', 'Absent')
        else:
            setattr(mark_detail.student, 'mark_in_word', mark_detail.student.mark)
        setattr(mark_detail.student, 'remark', get_remark(mark_detail.student.mark, mark_instance.pass_mark))
        setattr(mark_detail.student, 'is_fail', is_fail(mark_detail.student.mark, mark_instance.pass_mark))
        students.append(mark_detail.student)
    data['students'] = students
    return render(request, template_name='im/teacher/marks.html', context=data)


def validate_student_marks(students, fm):
    error = {}
    has_error = False
    for student in students:
        if str(student.mark).lower() == 'a':
            continue
        try:
            int(student.mark)
        except:
            error[student.name] = 'Invalid mark'
            has_error = True
            continue
        if int(student.mark) > int(fm):
            error[student.name] = 'Entered marks is greater then full marks'
            has_error = True

    return has_error, error


@csrf_exempt
def display_result(request):
    th_pr = request.POST.get('thpr', 'th')
    programme_code = request.POST.get('prog', None)
    pass_mark = request.POST.get('pm', 8)
    full_mark = request.POST.get('fm', 20),
    sub_code = request.POST.get('code', '')
    batch = request.POST.get('batch', None)
    group = request.POST.get('group', "A")
    year = request.POST.get('year', "1")
    part = request.POST.get('part', "1")
    examiner_name = request.POST.get('exname', None)
    date = request.POST.get('date', None),
    programme = Programme.objects.get(short_form=programme_code)
    subject = SubjectDetail.objects.filter(subject_code=sub_code).first()
    res = MarksInstance.objects.filter(batch=batch, year=year, part=part, subject=subject,
                                       theory_practical=th_pr, group=group,
                                       programme=programme
                                       ).delete()
    mark_instance = MarksInstance.objects.create(batch=batch, year=year, part=part, subject=subject,
                                                 theory_practical=th_pr, group=group,
                                                 programme=programme,
                                                 date=str(date[0]).replace('/', '-'),
                                                 name_of_examiner=examiner_name,
                                                 pass_mark=pass_mark,
                                                 full_mark=full_mark[0])
    students = Student.objects.filter(programme__short_form=programme_code, batch=batch, group=group)
    for idx, student in enumerate(students):
        setattr(student, 'mark', request.POST.get('m%d' % (idx + 1,)))
    has_error, errors = validate_student_marks(students, full_mark[0])
    if has_error:
        context = {
            'errors': errors
        }
        print(context)
        return render(request, template_name='im/teacher/error.html', context=context)
    for idx, student in enumerate(students):
        MarksDetail.objects.create(marks_instance=mark_instance, student=student, marks=student.mark)

    url = reverse('display_result_ac_instance', kwargs={'marks_instance_id': mark_instance.id})
    return redirect(to=url)


@login_required
@user_passes_test(is_teacher)
def index(request):
    return render(request, template_name='im/home/index.html', context={})


@login_required
@user_passes_test(is_teacher)
def enter_marks(request):
    programmes = Programme.objects.all()
    data = {
        'programmes': programmes,
    }
    return render(request, template_name='im/teacher/marks_entry.html', context=data)


@login_required
@user_passes_test(is_teacher)
def see_marks(request):
    context = {}
    if request.method == 'GET':
        form = SeeMarksForm
    else:
        form = SeeMarksForm(data=request.POST)
        if form.is_valid():
            mark_instance = get_object_or_404(MarksInstance.objects.all(), **form.cleaned_data)
            url = reverse('display_result_ac_instance', kwargs={'marks_instance_id': mark_instance.id})
            return redirect(to=url)
    context['form'] = form
    return render(request, template_name='im/administration/overall_record.html', context=context)


@login_required
@user_passes_test(is_teacher)
def dept_see_records(request):
    context = {}
    if request.method == 'GET':
        form = YearPartFrom
    else:
        form = YearPartFrom(data=request.POST)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            part = form.cleaned_data.get('part')
            batch = form.cleaned_data.get('batch')
            context['year'] = year
            context['part'] = part
            context['batch'] = batch
            context['departments'] = Department.objects.all()
    context['form'] = form

    return render(request, template_name='im/administration/overall_record.html', context=context)


@login_required
@user_passes_test(is_student)
def stu_see_records(request):
    return render(request, template_name='im/student/mark_records.html')


@api_view(['GET', ])
@permission_classes([IsStudent, ])
def get_internal_marks(request):
    user = request.user.student_detail
    student_marks = MarksDetail.objects.filter(student=user)
    return Response(MarksDetailSerializer(student_marks, many=True).data, )
