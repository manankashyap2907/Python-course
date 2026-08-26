string = input("Please enter your own word : ")
charecter = input("Please enter your own Charecter : ")

a = 0
b = 0

while (a < len(string)):

    if (string[a] == charecter):
        b = b + 1
    a = a + 1

print("The total number of", charecter,"has occured = " , b)