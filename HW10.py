a = int(input("Enter a decimal number: "))

if a == 0:
    b = "0"
else:
    b = ""
    while a > 0:
        remainder = a % 2
        b = str(remainder) + b
        a = a // 2

print(f"The binary number is: {b}")
