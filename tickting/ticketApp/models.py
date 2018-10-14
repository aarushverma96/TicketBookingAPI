from django.db import models
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.


'''
Database Classes for the screens details 

Screen Name
Row Name
Number of Seats
Seats Structure

If seat is unbooked it is marked as -1 or -2(for asile seats)
If seat is booked  it is marked as 1 or 2(for asile seats)
'''


class Screens(models.Model):

	screen_name=models.CharField(max_length=10)
	rows=models.CharField(max_length=10)
	number_of_seats=models.IntegerField()
	seats_structure=models.CharField(validators=[validate_comma_separated_integer_list],max_length=50,default='-1,-1,-1,-1,-1,-1,-1,-1,-1,-1')


	def __str__(self):
		return str(self.screen_name + " " + self.rows)