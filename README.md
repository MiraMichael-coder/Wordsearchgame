# Word Search Game Documentation

## Overview
This Python program implements a word search puzzle game where players find hidden words in a grid of letters. The game features multiple difficulty levels, word categories, and the ability to save/resume games.

## Features

- **Customizable Grid Sizes**: Different grid dimensions based on difficulty level
- **Multiple Categories**: Choose from animals, cars, or cities word lists
- **Difficulty Levels**:
  - Easy (8x8 grid, shorter words)
  - Medium (10x10 grid)
  - Hard (12x12 grid, more words)
- **Game Persistence**: Save and resume games
- **Interactive Gameplay**: 
  - Guess words by entering letter coordinates
  - Limited attempts to increase challenge
  - Score tracking

## Installation

1. Ensure you have Python 3.x installed
2. Clone or download the repository
3. Create a directory structure:
   ```
   /words/
     animal_words.txt
     car_words.txt
     cities_words.txt
     saved_game.txt
   ```
4. Populate the word files with appropriate words (one per line)

## Usage

Run the program with:
```
python word_search.py
```

### Game Flow

1. Enter your name
2. Choose to resume a saved game (if available) or start new
3. Select difficulty level (1-3)
4. Choose a word category (a-c)
5. The game displays the word list and letter grid
6. Guess words by:
   - Entering the word
   - Providing coordinates for each letter
7. Continue until all words are found or attempts run out

### Controls

- During gameplay:
  - Enter 'e' to quit and optionally save
  - Enter 'y'/'n' when prompted to play again

## File Structure

- `word_search.py`: Main game script
- `/words/`: Directory containing:
  - `animal_words.txt`: Animal vocabulary
  - `car_words.txt`: Vehicle vocabulary
  - `cities_words.txt`: City names
  - `saved_game.txt`: Stores game state

## Functions

### Core Game Functions

- `create_grid(r, c)`: Creates empty grid of specified dimensions
- `fill_with_random_letters(grid)`: Fills empty spaces with random letters
- `display_grid(grid)`: Prints the current grid state
- `choose_direction(grid, word)`: Selects random placement for words
- `generate_words(grid, level)`: Loads words based on category and places them

### Game Logic

- `validation()`: Validates player guesses
- `check_guess()`: Verifies if guess matches hidden word
- `resume_logic()`: Handles game continuation
- `main()`: Primary game loop and setup

### File Operations

- `save_game_data()`: Saves current game state
- `load_data()`: Loads saved game
- `file_path()`: Returns base directory path (modify for your system)

## Customization

To adapt the game:

1. Modify `file_path()` to point to your working directory
2. Edit word list text files to change vocabulary
3. Adjust grid sizes in the level selection logic
4. Change attempt counter in `main()` for different challenge levels

## Requirements

- Python 3.x
- Standard libraries:
  - random
  - json
  - os

## Known Issues

- Absolute file path requirement (modify `file_path()` for your system)
- Limited error handling for file operations
- Coordinate input could be more user-friendly

## Future Improvements

- Graphical interface
- Additional word categories
- Multiplayer support
- Timer mode
- Score leaderboard

Enjoy the Word Search game!
