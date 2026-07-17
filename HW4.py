import math

number = float(input("Enter a number: "))

print("calculating sqare root...")

if number < 0:
    print("Cannot calculate a real square root of a negative number.")
else:
    result = math.sqrt(number)
    print(f"The square root of {number} is {result}")