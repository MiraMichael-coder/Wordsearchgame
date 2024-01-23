import string
import random
import json
import os
def create_grid(r, c):  # empty grid
    grid = []
    for row_index in range(r):
        row = []  # Create a new row list for each iteration
        for col_index in range(c):
            row.append(" ")
        grid.append(row)
    return grid


def fill_with_random_letters(grid):# fill the free space with random letters
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == " ":
                grid[row][col] = random.choice(string.ascii_uppercase)

def display_grid(grid):
       #Prints a visual representation of a 2D grid.
    if not grid:  # Check for empty grid
        print("Empty grid!")
        return

    # Build and format header
    header = " | ".join(str(col).rstrip() for col in range(len(grid[0])))
    print(f"  | {header} | ")

    # Print separator
    print("-" * (4 * len(grid[0]) + 3))

    # Iterate through rows and print them
    for i, row in enumerate(grid):
            # take alist or tuple and
        row_str = " | ".join(row)
        print(f" {i}| {row_str} |")

def choose_direction(grid, word):#choose random direction for each word
    rows, cols = len(grid), len(grid[0])
    while True:
        direction = random.choice([(0, 1), (1, 0), (1, 1), (-1, -1)])#Down,left,diagonal,reverse diagonal
        x = random.randint(0, max(0, rows - len(word)))
        y = random.randint(0, cols - len(word))

        if can_place_word(word, x, y, direction, grid):#check if he can plac word in the grid or not
            place_word(word, x, y, direction, grid)#if yes go to place function
            break
    return grid

def can_place_word(word, x, y, direction, grid):
    for i in range(len(word)):
        x_new = x + i * direction[0]
        y_new = y + i * direction[1]
        if not valid_placement(x_new, y_new,grid):
            return False
    return True

def valid_placement(row, col, grid):#validate if the the sepecific index filled or not

     if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
         if grid[row][col] == " ":
            return True

     return False

def place_word(word, x, y, direction, grid):
    for i in range(len(word)):# loop over each letter and calculate its coordinates
        x_new = x + i * direction[0]
        y_new = y + i * direction[1]
        grid[x_new][y_new] = word[i]

def generate_words(grid,level):# choose category then choose random words
    """Loads words based on the chosen category and places them on the grid."""
    max_attempts = 3  # Set maximum number of attempts
    attempts = 0
    while attempts < max_attempts:

        category = input("Please choose the category\n"
                            "(a for animals, b for cars, c for cities): ").lower()
        words_=[]
        try:
            if category == "a":  # if choose animals open animal txt file
                file = open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\animal_words.txt")  # Open the file in read mode
                try:
                    for line in file:# loop over file and put each line in a list
                        word = line.strip()
                        words_.append(word)
                except FileNotFoundError:#handling error
                    print(f"Error: File for category '{category}' not found.")
                finally:
                    file.close()

            elif category == "b":#open car txt file
                file = open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\car_words.txt")  # Open the file in read mode
                try:
                    for line in file:
                        word = line.strip()
                        words_.append(word)
                except FileNotFoundError:
                    print(f"Error: File for category '{category}' not found.")
                finally:
                    file.close()
            elif category == "c":#open cities file
                file = open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\cities_words.txt")  # Open the file in read mode
                try:
                    for line in file:
                        word = line.strip()
                        words_.append(word)
                except FileNotFoundError:
                    print(f"Error: File for category '{category}' not found.")
                finally:
                    file.close()
            else:
                raise ValueError("Invalid list choice. Please enter 'a', 'b', or 'c'.")

            if level=="1":
                words = []
                random.shuffle(words_)
                for word in words_[1:6]:
                    if len(word) < 9:
                        words.append(word)
            elif level=="2":#choose 6
                random.shuffle(words_)
                words = words_[:6]
            elif level=="3":#choose 7
                random.shuffle(words_)
                words = words_[:7]

            for word in words: #then goto choose direction function to put words one by one
                grid = choose_direction(grid,word)
            return words, grid  # Return after successful word placement
        except ValueError as e:#handling wrong input
            print(e)
            attempts += 1  # Increment attempt counter
            if attempts == max_attempts:
                print("Maximum attempts to enter correct category reached. Exiting.")
                break  # Exit the loop if maximum attempts reached


def validate_grid_coordinates(grid, row_index, col_index):
    #Checks if the given coordinates are within the valid grid boundaries.
    if 0 <= row_index < len(grid) and 0 <= col_index < len(grid[0]):
        return True
    return False
def validation(word_positions, word_list, grid):#making sure guess word and coordinates are right
    while True:
        word_input = input("Please enter the word you want to guess: ").upper()

        if word_input in word_list:
            index_choice = []
            for i in range(len(word_input)):
                while True:
                    try:# it stores the user input in a list then compare it with the right placement
                        index_x = int(input(f"Please enter index of row for letter '{word_input[i]}': "))
                        index_y = int(input(f"Please enter index of column for letter '{word_input[i]}': "))
                        if validate_grid_coordinates(grid, index_x, index_y) and grid[index_x][index_y] == word_input[i]:
                            index_choice.append((index_x, index_y)) # Use a tuple for coordinates

                            break
                        else:
                            print("Invalid indices. Please enter values within the grid boundaries and matching the letter.")
                    except ValueError:# handling inputing a charcter as input
                        print("Invalid input. Please enter integer values for the indices.")

            return index_choice, word_input

        else:
            print("Oopsie, try another word from the list:")


def find_word_position_in_grid(word, grid):#This store the position of words in a list
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == word[0]:
                for direction in [(0, 1), (1, 0), (1, 1), (-1, -1)]:
                    if can_place_word(word, row, col, direction, grid):
                        positions = []
                        for i in range(len(word)):
                            x_new = row + i * direction[0]
                            y_new = col + i * direction[1]
                            positions.append((x_new, y_new, word[i]))
                        return positions

    return []

def check_guess(guess, word_positions, grid):
    correct_positions = {}
    # Find all correct positions for the guessed letters
    for (word_index, position_in_word), (row, col, char) in word_positions.items():
        if guess[position_in_word].upper() == char:
            correct_positions[(row, col)] =char

    # Check if the guessed letters match any of the correct positions
    for row, col in correct_positions:
        if grid[row][col] != guess[correct_positions] :
            return False

    return True

def save_game_data(words, word_positions, name, score, grid):
    filename = open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\saved_game.txt", "w")
    filename.write(f"words={words}\n")
    filename.write(f"word_positions={word_positions}\n")
    filename.write(f"name={name}\n")
    filename.write(f"score={score}\n")
    for row in grid:
        filename.write("".join(row) + "\n")  # Write each row of the grid



def load_data():
    filename = r"C:\Users\Lenovo\Desktop\final wordsearch\cr\saved_game.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Extract data from lines (assuming a consistent format)
            words = eval(lines[0].split("=")[1].strip())  # Handle grid data extraction
            word_positions = eval(lines[1].split("=")[1].strip())  # Handle grid data extraction
            name = lines[2].split("=")[1].strip()
            score = int(lines[3].split("=")[1].strip())
            grid = [list(line.strip()) for line in lines[4:]]  # Convert each line to a list of characters
            # Return the loaded data
            return {
                "words": words,
                "word_positions": word_positions,
                "name": name,
                "score": score,
                "grid": grid,
            }
    else:
        print("No saved data found for that name.")
    return None

def resume_logic(words, grid, name, word_positions):
    # Recalculate word positions (remove unnecessary dictionary creation):
    for index, word in enumerate(words):
        positions = find_word_position_in_grid(word, grid)

        word_positions = {}
        for i, pos in enumerate(positions):
            word_positions[(index, i)] = pos

    counter = 5
    saved_data = load_data()

    # Retrieve score cautiously, handle potential None value:
    score = saved_data.get("score", 0)  # Use 0 as default if score is not found
    print(f"Number of trials for {name} is {counter}")

    while counter > 0:
        guess, word_input = validation(word_positions, words, grid)

        if check_guess(guess, word_positions, grid):
            print("Hooray! Correct!")
            score += 1  # Increment score (already ensured it's an integer)
            words.remove(word_input)
            print(f"New list {words}")
            counter -= 1
            print(f'Score: {score}')
            quit_input = input("Enter 'e' to quit the game, or press Enter to continue: ")

            if score>=5 or score<8:
                print("Game over!""\n""Congratulations, you won!")
                break
            if quit_input.lower() == 'e':  # If user wants to quit
                save_game = input("Do you want to save the game for later? (y/n): ")
                if save_game.lower() == 'y':
                    try:
                        saved_data["score"] = score  # Update the score in the saved_data dictionary
                        save_game_data(words, word_positions, name, score, grid)
                        print("Game saved successfully!")
                        start=input("new game?(y/n)")
                        if start=="y":
                            main()
                        else:
                            print("BYE!")
                    except Exception as e:
                        print(f"Error saving game: {e}")
                break
        else:
            print("Boo! Incorrect. Try again.")
            counter -= 1
            print(f"Number of trials left for {name} is {counter}")
            if counter == 0:
                print("Game over!""\n""Sorry, you lose.")
                break


def check_oldusername(username):
    filename = open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\saved_game.txt", "r")
    lines = filename.readlines()  # Read all lines into a list
    if len(lines) >= 3:  # Ensure there are at least 3 lines to access line 2
        second_line = lines[1].strip()  # Get the second line (index 1) and remove extra whitespace
        try:
            name_from_file = second_line.split("=")[1].strip()  # Split at "=", take the second part, and strip whitespace
            if name_from_file == username:
                return True
                # Also return the loaded data
        except IndexError:
            print("Invalid format in line 2. Cannot extract name.")  # Handle cases where "=" is missing
    return False

def main():
    name = input("Please enter your name: ")
    saved_data = load_data()  # Load saved data first
    resume_game = input(f"Welcome back, {name}! Do you want to resume your last saved game? (y/n): ")
    if resume_game.lower() == 'y':
        try:
            if check_oldusername(name):
                words = saved_data["words"]
                word_positions = saved_data["word_positions"]
                name = saved_data["name"]
                score = saved_data["score"]
                grid = saved_data["grid"]
                print("Resuming the game...")
                print(f"Your previous score was: {score}")
                print(f'Remaining words: {words}')
                display_grid(grid)
                # Resume the game from where it was left off:
                resume_logic(words, grid, name, word_positions)

          # End the main function to prevent starting a new game
        except KeyError as e:
            print(f"Error loading saved game: Missing key '{e.args[0]}'.")
                # Handle missing key error appropriately
        else:
                # Handle the case where there's no saved game or score is 0
            print("No saved game found. Starting a new game...")

                # Start a new game with appropriate initialization

                # Start new game (no valid saved game)
            print(f"Welcome, {name}! Let's start, shall we? GOOD LUCK!")
            while True:
                try:
                    level = input("Please enter the level you want 1 for Easy, 2 for Medium, 3 for Hard: ")
                    if level in ["1", "2", "3"]:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter one of the three choices '1', '2', or '3':")

                # Assign row and column values based on the valid input
            if level == "1":
                rows, cols = 8, 8
            elif level == "2":
                rows, cols = 10, 10
            else:  # level == "3"
                rows, cols = 12, 12

            grid = create_grid(rows, cols)
            words, grid = generate_words(grid, level)

            fill_with_random_letters(grid)

            print(words)
            display_grid(grid)

            for index, word in enumerate(words):
                positions = find_word_position_in_grid(word, grid)
                word_positions = {(index, i): pos for i, pos in enumerate(positions)}

            counter = 7
            score = 0

            print(f"Number of trials for {name} is {counter}")

            while counter > 0:
                guess, word_input = validation(word_positions, words, grid)

                if check_guess(guess, word_positions, grid):
                    print("Hooray! Correct!")
                    score += 1
                    words.remove(word_input)
                    print(f"new list {words}")
                    counter -= 1
                    print(f"Score:{score} , counter:{counter}")
                    quit_input = input("Enter 'e' to quit the game, or press Enter to continue: ")

                    if score == len(words):
                        print("Game over!""\n""Congratulations, you won!")
                        break
                    if quit_input.lower() == 'e':  # If user wants to quit
                        save_game = input("Do you want to save the game for later? (y/n): ")
                        if save_game.lower() == 'y':
                            try:
                                save_game_data(words, word_positions, name, score, grid)
                                print("Game saved successfully!")
                            except Exception as e:
                                print(f"Error saving game: {e}")
                        break
                else:
                    print("Boo! Incorrect. Try again.")
                    counter -= 1
                    print(f"Number of trials left for {name} are {counter}")
                    if counter == 0:
                        print("Game over!""\n""Sorry, you lose.")
                        break

                # Store scores in the file (only for new players or updated scores)
            new_game = input("Do you want to play again? (y/n): ")
            if new_game.lower() == 'y':
                main()
            else:
                print("Thank you, have a nice day!")


main()


