secret_number = 7
count = 0
max_tries = 4

while count < max_tries:
    guess = int(input(f"Guess the number [{count+1}/{max_tries}]: "))
    count += 1
    
    if guess == secret_number:
        print(f"Correct! You guessed it in {count} tries 🎉")
        break
    elif guess < secret_number:
        print("Too low! Try again")
    else:
        print("Too high! Try again")
else:
    print(f"Game Over! The number was {secret_number}")