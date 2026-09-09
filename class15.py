def calc (bill, tip_perc):
    print("")

    total = bill*(1 + 0.01 *tip_perc)
    total = round(total, 2)

    print(f"Please pay ${total}")
          
calc(273, 10.5)