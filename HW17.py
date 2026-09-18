def calculate_due_amount(bill, paid):
    change = paid - bill
    return change

total_bill = float(input("Enter the total bill amount: "))
amount_paid = float(input("Enter the amount paid: "))

result = calculate_due_amount(total_bill, amount_paid)
print("Change to return:", result)
