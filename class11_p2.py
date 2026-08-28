rows = int(input("Please enter the total number of rows: "))
number = 1

print("Floyd's Triangle")

for a in range (1, rows + 1):
    for b in range (1, a + 1):
        
        print(number, end = '   ')
        number = number + 1
    print()