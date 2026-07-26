a = 10
b = 15
c = 5

print(not(a == b))

print(not(b == c))

z = "hello"
y = "world"

if not (z == y):
    print(z, "and", y, "are different" )

    if not (z == y):
        print(z, "and", y, "are different")

m = 50
n = 70

if not((m == 50)) == ((n == 70)):
    print(m, "and", n, "are different")


a = int(input("Enter a number"))

if not (a % 2 == 0):
    print(a, "is an odd number.")