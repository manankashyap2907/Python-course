print("The shape of a star(*): ")
a = int(input("Enter that number of rows: "))

for i in range (a):
    for j in range (i + 1):
        print("*", end="")
    print()