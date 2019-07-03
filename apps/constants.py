from datetime import datetime

USER_TYPE_STUDENT = 'Student'
USER_TYPE_TEACHER = 'Teacher'

DAY_OF_WEEK_CHOICES_TUPLE = (
    (1, 'Sunday'),
    (2, 'Monday'),
    (3, 'Tuesday'),
    (4, 'Wednesday'),
    (5, 'Thursday'),
    (6, 'Friday'),
    (7, 'Saturday')
)

current_year = datetime.now().date().year
current_year_in_nepali = int(current_year) + 58
BATCH_CHOICES = [(str(year), str(year)) for year in range(2071, current_year_in_nepali)]

GROUP_CHOICES = [(i, i) for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]
