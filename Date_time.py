from datetime import date , time , datetime

today = date.today()
now = datetime.now()

print("Today's date:", today)
print("\nCurrent time is :", now.time())

print("Data components:", today.day, today.month, today.year)