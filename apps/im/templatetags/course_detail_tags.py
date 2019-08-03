from django import template

register = template.Library()


@register.simple_tag
def has_marks(course_detail, batch, th_pr, group):
    return course_detail.has_marks(batch, th_pr, group)


@register.simple_tag
def get_marks_detail(course_detail, batch, th_pr, group):
    return course_detail.get_marks_detail(batch, th_pr, group)


@register.simple_tag
def get_marks_seeing_url(course_detail, batch, th_pr, group):
    return course_detail.get_marks_seeing_url(batch, th_pr, group)
