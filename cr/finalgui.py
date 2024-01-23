import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage


class WordSearchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Game")
        self.root.geometry("600x600")
        bg = PhotoImage(file=r"C:\Users\Lenovo\Desktop\final wordsearch\cr\images\intro.gif")
        bg_label = tk.Label(self.root, image=bg)
        bg_label.place(x=0, y=0, relheight=1, relwidth=1)
        bg_label.image = bg
        self.name = ""
        self.words = []
        self.grid_size = (0, 0)
        self.grid = self.create_grid(*self.grid_size)
        self.word_positions = {}
        self.found_words = []
        self.trials_left = 0
        self.timer_seconds = 300  # Five-minute timer
        self.show_solution = tk.BooleanVar()
        self.pressedWord = ''
        self.pressedCoordinates = []
        self.buttons = []
        self.word_list_labels = []
        self.timer_label = None  # Added timer label
        self.difficulty_var = tk.StringVar(value="")  # Added difficulty variable with default value
        self.create_welcome_page()
        self.paused = False  # Flag to track if the timer is paused
        self.pause_button = None
        self.resume_button = None
    def create_welcome_page(self):
        welcome_frame = tk.Frame(root)
        welcome_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        welcome_label = tk.Label(welcome_frame, text="Welcome to Word Search Game!", fg="black",
                                 font=("Arial", 14))
        welcome_label.pack(padx=20, pady=60)

        name_label = tk.Label(welcome_frame, text="Enter your name:", font=("Arial", 13))
        name_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.name_entry = tk.Entry(welcome_frame)
        self.name_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        category_label = tk.Label(welcome_frame, text="Choose the category:", fg="black", font=("Arial", 12))
        category_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.category_var = tk.StringVar()
        categories = [("Animals"), ("Cars"), ("Cities")]
        category_dropdown = tk.OptionMenu(welcome_frame, self.category_var, *categories)
        category_dropdown.config(fg="black", font=("Arial", 12))
        category_dropdown.pack(pady=10)

        difficulty_label = tk.Label(self.root, text="Choose difficulty:", fg="black", font=("Arial", 12))
        difficulty_label.place(relx=0.5, rely=0.60, anchor=tk.S)
        difficulties = ["Easy", "Medium", "Hard"]
        difficulty_dropdown = tk.OptionMenu(self.root, self.difficulty_var, *difficulties)
        difficulty_dropdown.config(fg="black", font=("Arial", 12))
        difficulty_dropdown.place(relx=0.5, rely=0.65, anchor=tk.S)

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 12),
                                 bg="#c27ba0",
                                 fg="white")
        start_button.pack(pady=10)
        start_button.place(relx=0.5, rely=0.7, anchor=tk.S)

    def start_game(self):
        self.name = self.name_entry.get()
        list_choice = self.category_var.get()
        difficulty = self.difficulty_var.get()
        if self.name and list_choice and difficulty:
            rows, cols = self.get_grid_size(self.difficulty_var.get())  # Get grid size based on difficulty
            self.grid = self.create_grid(rows, cols)
            self.generate_background(list_choice)
            self.words, self.grid = self.generate_words(list_choice)
            self.trials_left = len(self.words)
            self.right_guesses = 0
            self.timer_seconds = 300  # Reset timer to 2 minutes
            self.generate_background(list_choice)
            self.create_game_page(list_choice)
            self.update_timer()


        else:
            messagebox.showinfo("Error", "Please enter your name and choose a category.")

    def get_grid_size(self, level):
        if level == "Easy":
            return 8, 8
        elif level == "Medium":
            return 10, 10  # Return both grid size and words
        else:  # level == "Hard"
            return 12, 12

    def create_game_page(self, list_choice):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.generate_background(list_choice)

        game_frame = tk.Frame(self.root, bg="#c27ba0")
        game_frame.pack(expand=True)
        grid_frame = tk.Frame(game_frame, bg="#c27ba0")
        grid_frame.grid(row=0, column=0, padx=20, pady=20)
        word_list_frame = tk.Frame(game_frame, bg="#c27ba0")
        word_list_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        score_frame = tk.Frame(game_frame)
        score_frame.grid(row=0, column=2, columnspan=1, pady=10)

        # Set transparent background for check button and message label
        check_button = tk.Button(word_list_frame, text="Check Word", height=1, width=15, anchor='c',
                                 command=self.check_word, bg="#c27ba0")
        check_button.grid(row=0, column=1)

        self.message_text = tk.StringVar()
        message_label = tk.Label(word_list_frame, textvariable=self.message_text, font=("Arial", 12),
                                 bg="#c27ba0", fg="#c27ba0")

        message_label.grid(row=0, column=0, padx=0, pady=0, sticky=tk.E)
        save_button = tk.Button(score_frame, text="Save", command=self.save_game, font=("Arial", 12),
                        bg="#c27ba0", fg="white")
        save_button.grid(row=2, column=1, padx=2, pady=2, sticky=tk.W)

        # Place the score label on the left side with minimum padding
        self.score_label = tk.Label(score_frame, text="Score: 0", font=('None %d' % 14))
        self.score_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.E)  # Set padding to 2

        # Place the timer label next to the score label on the right side with minimum padding
        self.timer_label = tk.Label(score_frame, text=f"Time: {self.format_timer(self.timer_seconds)}",
                                    font=('None %d' % 14))
        self.timer_label.grid(row=0, column=1, padx=0, pady=0, sticky=tk.W)  # Set padding to 2

        self.display_grid()
        self.display_word_list()
        self.display_score()
        self.pause_button = tk.Button(score_frame, text="Pause Timer", command=self.pause_timer, font=("Arial", 12),
                                      bg="#c27ba0", fg="white")
        self.pause_button.grid(row=1, column=0, padx=2, pady=2, sticky=tk.E)

        self.resume_button = tk.Button(score_frame, text="Resume Timer", command=self.resume_timer, font=("Arial", 12),
                                       bg="#c27ba0", fg="white")
        self.resume_button.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
        quit_button = tk.Button(score_frame, text="Quit", command=self.confirm_quit, font=("Arial", 12),
                                bg="#c27ba0", fg="white")
        quit_button.grid(row=2, column=0, padx=2, pady=2, sticky=tk.E)
    def save_game(self):
        save_data = {
            "words": self.words,
            "word_positions": self.word_positions,
            "name": self.name,
            "score": self.right_guesses,
            "grid": self.grid,
        }

        try:
            self.save_game_data(save_data)
            messagebox.showinfo("Game Saved", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving game: {e}")

    def save_game_data(self, save_data):
        filename = r"C:\Users\Lenovo\Desktop\final wordsearch\cr\saved_game.txt"
        with open(filename, "w") as file:
            file.write(f"words={save_data['words']}\n")
            file.write(f"word_positions={save_data['word_positions']}\n")
            file.write(f"name={save_data['name']}\n")
            file.write(f"score={save_data['score']}\n")
            for row in save_data['grid']:
                file.write("".join(row) + "\n")  # Write each row of the grid
    
    def pause_timer(self):
        self.paused = True
        self.pause_button.config(state=tk.DISABLED)  # Disable pause button when already paused
        self.resume_button.config(state=tk.NORMAL)
        self.disable_grid_buttons()
    def resume_timer(self):
        self.paused = False
        self.pause_button.config(state=tk.NORMAL)  # Enable pause button when resuming
        self.resume_button.config(state=tk.DISABLED)
        self.enable_grid_buttons()
        self.update_timer()
    def disable_grid_buttons(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state=tk.DISABLED)

    def enable_grid_buttons(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state=tk.NORMAL)    
    def generate_background(self, list_choice):
        image_path = None

        if list_choice == "Animals":
            image_path = tk.PhotoImage(file=r"C:\Users\Lenovo\Desktop\final wordsearch\cr\images\animals.gif")
        elif list_choice == "Cars":
            image_path = tk.PhotoImage(file=r"C:\Users\Lenovo\Desktop\final wordsearch\cr\images\cars.gif")
        elif list_choice == "Cities":
            image_path = tk.PhotoImage(file=r"C:\Users\Lenovo\Desktop\final wordsearch\cr\images\cities.gif")
        else:
            raise ValueError("Invalid choice. Please enter 'Animals', 'Cars', or 'Cities'.")

        frame1 = tk.Frame(self.root)
        frame1.place(x=0, y=0, relwidth=1, relheight=1)
        background_label = tk.Label(frame1, image=image_path)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.pack(expand=True, fill=tk.BOTH)
        # Keep a reference to the image to prevent it from being garbage-collected
        background_label.image = image_path

    def confirm_quit(self):
        response = messagebox.askyesno("Quit Game", "What to restart game?")
        if response:
            self.reset_game()
        else:
            messagebox.showinfo("Thank You", "Thank you for playing!")
            self.root.destroy()
    def generate_words(self, list_choice):
        file_path = None
        if list_choice == "Animals":
            file_path = r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\animal_words.txt"
        elif list_choice == "Cars":
            file_path = r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\car_words.txt"
        elif list_choice == "Cities":
            file_path = r"C:\Users\Lenovo\Desktop\final wordsearch\cr\words\cities_words.txt"
        else:
            raise ValueError("Invalid category. Please enter 'Animals', 'Cars', or 'Cities'.")

        try:
            with open(file_path, 'r') as file:
                words = [word.strip() for line in file for word in line.split()]

            random.shuffle(words)
            words = words[:6]
            for word in words:
                self.grid = self.choose_direction(word)
            self.fill_with_random_letters()
            return words, self.grid

        except FileNotFoundError:
            print("Error: File not found.")
            return None

    def create_grid(self, r, c):
        return [[" " for _ in range(c)] for _ in range(r)]

    def choose_direction(self, word):
        rows, cols = len(self.grid), len(self.grid[0])
        while True:
            direction = random.choice([(0, 1), (1, 0), (1, 1), (-1, -1)])
            x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if self.can_place_word(word, x, y, direction):
                self.place_word(word, x, y, direction)
                break
        return self.grid

    def can_place_word(self, word, x, y, direction):
        for i in range(len(word)):
            x_new = x + i * direction[0]
            y_new = y + i * direction[1]
            if not self.valid_placement(word[i], x_new, y_new):
                return False
        return True

    def valid_placement(self, char, row, col):
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]) and (
                    self.grid[row][col] == " " or self.grid[row][col] == char)

    def place_word(self, word, x, y, direction):
        positions = []
        for i in range(len(word)):
            x_new = x + i * direction[0]
            y_new = y + i * direction[1]
            self.grid[x_new][y_new] = word[i]
            positions.append((x_new, y_new))
        self.word_positions[word] = positions

    def fill_with_random_letters(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == " ":
                    row[i] = random.choice(string.ascii_uppercase)

    def display_grid(self):
        grid_frame = tk.Frame(self.root, bg="#c27ba0")
        grid_frame.pack(pady=10, side="left")
        for i in range(len(self.grid)):
            row_buttons = []
            for j in range(len(self.grid[i])):
                button = tk.Button(grid_frame, text=self.grid[i][j], font=("Arial", 14), width=4, height=1,
                                   command=lambda i=i, j=j: self.buttonPress(i, j))
                button.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def display_word_list(self):
        word_list_frame = tk.Frame(self.root, bg="#c27ba0")
        word_list_frame.pack(pady=5, side="left", padx=(10, 0))
        for word in self.words:
            label = tk.Label(word_list_frame, text=word, font=("Arial", 12), bg="#c27ba0", fg="white")
            label.pack()
            self.word_list_labels.append(label)

    def buttonPress(self, x, y):
        if not self.pressedWord or (self.pressedWord and (x, y) not in self.pressedCoordinates):
            self.pressedWord += self.grid[x][y]
            self.pressedCoordinates.append((x, y))
            self.buttons[x][y].config(bg='#F9FB46')


    def check_word(self):
        if not self.pressedWord:
            return

        if self.pressedWord in self.words and all(
                coord in self.word_positions[self.pressedWord] for coord in self.pressedCoordinates):
            for x, y in self.pressedCoordinates:
                self.buttons[x][y].config(bg='lime green')
            self.right_guesses += 1
            self.found_words.append(self.pressedWord)
            self.words.remove(self.pressedWord)
            self.update_word_list()
        else:
            for x, y in self.pressedCoordinates:
                self.buttons[x][y].config(bg='red')  # Highlight wrong selection in red
            self.trials_left -= 1
            self.display_score()  # Update the score display immediately after an incorrect selection
            self.root.after(1000, self.reset_wrong_selection)  # After 1 second, reset the wrong selection

        self.pressedWord = ''
        self.pressedCoordinates = []

        if not self.words or self.trials_left <= 0:
            result = messagebox.askquestion("Game Over",
                                        f"{'Congratulations, you win!'  if not  self.words  else  'Sorry, you lose!'} Play again?",
                                        icon='question')
            if result == 'yes':
                self.reset_game()
            else:
                self.root.destroy()

    def reset_wrong_selection(self):
        for x, y in self.pressedCoordinates:
            self.buttons[x][y].config(bg='SystemButtonFace')  # Reset the color to the default
        self.display_score()  # Update the score display after resetting the wrong selection


    def update_word_list(self):
        for label in self.word_list_labels:
            if label.cget("text") == self.pressedWord:
                label.config(bg="lime green", fg="black")
                break

    def display_score(self):
        self.score_label.config(
            text=f"  Trials Left - {self.trials_left}, Username - {self.name}")
        self.update_timer( )
    def update_timer(self):
        if not self.paused:
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.timer_label.config(text=f"Time: {self.format_timer(self.timer_seconds)}")
                self.root.after(1000, self.update_timer)
        #else:
            #messagebox.showinfo("Game Over", "Time's up! Play again?")
            #self.reset_game()

    def format_timer(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:01}:{seconds:01}"

    def score_saving(self):
        """Saves the current score to a file."""

        with open(r"C:\Users\Lenovo\Desktop\final wordsearch\cr\saved_game.txt", "a") as file:
            name = self.name_entry.get()  # Assuming name_entry is an entry widget
            score = self.right_guesses  # Assuming right_guesses holds the score

            score_data = f"{name};{score}\n"
            file.write(score_data)

    def reset_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.words = []
        bg = PhotoImage(file=r"C:\Users\Lenovo\Desktop\final wordsearch\cr\images\intro.gif")
        bg_label = tk.Label(self.root, image=bg)
        bg_label.place(x=0, y=0, relheight=1, relwidth=1)
        bg_label.image = bg
        self.grid_size = (0, 0)
        self.grid = self.create_grid(*self.grid_size)
        self.word_positions = {}
        self.buttons = []
        self.pressedWord = ''
        self.pressedCoordinates = []
        self.found_words = []
        self.trials_left = 0
        self.word_list_labels = []
        self.timer_label = None
        self.create_welcome_page()


if __name__ == "__main__":
    root = tk.Tk()
    game = WordSearchGame(root)
    root.mainloop()
