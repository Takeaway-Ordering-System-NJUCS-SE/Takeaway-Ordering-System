from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class WorkoutCalendar(HTMLCalendar):
	def __init
