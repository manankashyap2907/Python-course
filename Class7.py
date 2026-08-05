a = (input("Did you have a medical cause?: (Y/n) ")).strip().upper()

if a == "Y":
    print("You are allowed")

else:
    attendance = int(input("Enter the attendance: "))

    if attendance >= 75:
        print("You are Allowed")

    else:
        print("Not Allowed")