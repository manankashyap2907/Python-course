number = int(input("Enter a number: "))

count = 0

if number == 0:
    count = 1
else:
    while number > 0:
        count += 1
        number = number // 10

print("Total digits in this number are:", count)