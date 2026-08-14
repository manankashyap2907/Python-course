base = int(input("Enter the base of the number: "))
n = int(input("Enter the power number: "))

answer = 1

for i in range (n):
    answer = answer * base

print("The answer is: ", answer)