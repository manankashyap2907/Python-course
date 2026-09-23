import random
playing = True
number = str(random.randint(0, 9))
print("Hello!, I will generate a random number between 0 and 9, and you have to guess it.")
print("If you get the correct number then you win!")
while playing:
    guess = input("Enter your guess: ")
    if guess == number:
        print("Congratulations! You guessed the correct number!")
        playing = False
    else:
        print("Sorry, that's not the correct number. Try again!")