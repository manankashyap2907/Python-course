Amount =int(input("Please enter the amount you want to widraw:"))

note1 = Amount//100
note2 = (Amount%100)//50
note3 = ((Amount%100)%50)//10

print("notes of 100", note1)
print("notes of 50", note2)
print("notes of 10", note3)