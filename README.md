##Completed Tasks

1.	Only 6 people can book one slot
userapp\serializers.py:
if existing >= 6:

2.	Add drop down for animal, bird, amphibian, reptile for admin dashboard

3.	 Status management - 4 statuses: booked, payment completed, cancelled, completed
userapp\models.py – line 129

4.	Sheet (15th)
Cancellation frees up slot - When appointment is cancelled, slot becomes available for others
Real-time seat count - Shows "Available (X seats left)"

5.	Sheet (4th)
Pet Deletion Option: Users should have the ability to delete their pet profile whenever Required

6.	Sheet (14th)
Appointment Cancellation Time Limit
Appointments can only be cancelled 3 hours before the scheduled time.
userapp\models.py – line 172

7.	Sheet(8th)
Email & Phone Number – Validation (using Regex)

8. Extending existing payment system instead of creating a seperate one for appointment (doctor) payment.
