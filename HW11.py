def print_mirrored_triangle(n):
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        stars = "*" * i
        print(spaces + stars)

height = 5
print_mirrored_triangle(height)
    