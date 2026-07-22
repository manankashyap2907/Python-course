actual_cost = float(input("Please type the cost here: "))
sale_amount = float(input("Please enter the sale amount: "))

if (sale_amount > actual_cost):
    print("There is profit")
else:
    print("There is loss")