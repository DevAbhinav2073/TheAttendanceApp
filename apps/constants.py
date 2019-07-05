from datetime import datetime

USER_TYPE_STUDENT = 'Student'
USER_TYPE_TEACHER = 'Teacher'

DAY_OF_WEEK_CHOICES_TUPLE = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday')
)

current_year = datetime.now().date().year
current_year_in_nepali = int(current_year) + 58
BATCH_CHOICES = [(str(year), str(year)) for year in range(2071, current_year_in_nepali)]

GROUP_CHOICES = [(i, i) for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]

YEAR_CHOICES = [(y, y) for y in ['I', 'II', 'III', 'IV', 'V']]
PART_CHOICES = [(p, p) for p in ['I', 'II']]
