print("Marks obtained in 4 subjects")

Math = int(input("Maths :"))
English = int(input("English :"))
Hindi = int(input("Hindi :"))
Science = int(input("Science :"))

sum = Math+English+Hindi+Science
print("Sum of Math, English, Hindi, Science =",sum)

perc = (sum/400)*100

print(end="Percentage Mark = ")
print(perc)