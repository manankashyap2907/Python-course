U = int(input(" Please enter Number of Units you Consumed : "))

if(U < 50):
    amount = U * 2.60 
    surcharge = 25 

elif(U <= 100):
    amount = 130 + ((U - 50) * 3.25)
    surcharge = 35

elif(U <= 200):
    amount = 130 + 162.50 + ((U - 100) * 5.26)
    surcharge = 45

else:
    amount = 130 + 162.50 + 526 + ((U - 200) * 8.45)
    surcharge = 75

total = amount + surcharge
print("\nElectricity Bill = %.2f"  %total)