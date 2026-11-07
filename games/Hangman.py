#Hangman - A simple console game for 2 players

# How to start the game (in the terminal):
# 1. Player 1 tyupes in secret word
# 2. or game picks random word from list

import random

#own list if no word in beginning

WORDS = ["mountain", "ski resort", "snowboard", "chairlift", "avalanche","glacier","mountain hut","snowflake","gondola","summit"]



# 1. The pictures of the hangman
# The number of mistakes tells us which picture to show
# A backslash \ must be written twice \\ , otherwise Python
# thinks it is a special sign. On screen you will see only one \ .
PICTURES = [
    # 0 mistakes: nothing drawn yet
  """
 
 
                  O      Fun fact: I hate ropes.
                 /|\\    Please keep it that way!
                 / \\
    =========""",
    # 1 mistake: the post
    """
 
       |
       |
       |
       |
    =========""",
    # 2 mistakes: + top bar
    """
        _ _ _
       |
       |
       |
       |
    =========""",
    # 3 mistakes: + rope
    """
        _ _ _
       |     |
       |
       |
       |
    =========""",
    # 4 mistakes: + head
    """
        _ _ _
       |     |
       |     O
       |
       |
    =========""",
    # 5 mistakes: + back
    """
        _ _ _
       |     |
       |     O
       |     |
       |
    =========""",
    # 6 mistakes: + first arm
    """
        _ _ _
       |     |
       |     O
       |    /|
       |
    =========""",
    # 7 mistakes: + second arm
    """
        _ _ _
       |     |
       |     O
       |    /|\\
       |
    =========""",
    # 8 mistakes: + first leg
    """
        _ _ _
       |     |
       |     O
       |    /|\\
       |    /
    =========""",
    # 9 mistakes: + second leg -> game over
    """
        _ _ _
       |     |
       |     O
       |    /|\\
       |    / \\
    =========""",
]
 

# 2. Messages for the end of the game

 
# Picture for the winner

WIN_PICTURE = """
       \\O/    BYE BYE, ROPE!
        |     You saved him!
       / \\
"""
 
# Picture for the loser
LOSE_PICTURE = """
       .---.
      / o o \\     BOOO!
     |   O   |    He will haunt you
     |       |    until you win.
     '^v^v^v^'
"""
 
# Picture when the player leaves the game early (types "quit")
QUIT_PICTURE = """
        O      WAIT! WHERE ARE YOU GOING?!
       /|\\     You left me hanging...
       / \\     ...literally.
"""
 
# How many wrong guesses are allowed before the game is lost.

MAX_MISTAKES = 9
 
 
#3. Actions of the game 
# Return the word with _ for every letter that was not guessed yet.


def show_word(secret_word, guessed_letters):
    result = ""
 
    # Go through the secret word, one letter at a time.
    # First loop: letter = "c", then "a", then "t", then "s".
    for letter in secret_word:
        # Is it a space (like in "ski resort")? Then show a gap, no blank.
        # The player never has to guess a space.
        if letter == " ":
            result = result + "  "
        # Was this letter already guessed by the player?
        elif letter in guessed_letters:
            # Yes -> show the letter (plus a space, so it is easy to read)
            result = result + letter + " "
        else:
            # No -> show a blank instead
            result = result + "_ "
 
    # Give the finished text back to whoever called this function.
    return result
 


# Return True if every letter of the word was guessed, otherwise False.

def is_word_guessed(secret_word, guessed_letters):
    # Check every letter of the secret word.
    for letter in secret_word:
        # Spaces don't need to be guessed -> skip them.
        # "continue" jumps straight to the next letter.
        if letter == " ":
            continue
        # If even ONE letter is missing, the word is not guessed yet.
        if letter not in guessed_letters:
            # "return" stops the function right here.
            return False
 
    # The loop finished without finding a missing letter -> all guessed
    return True
 
 

# Print the picture, the word and the letters guessed so far.
# game state that the player sees after every guess.

def print_game_state(secret_word, guessed_letters, mistakes):
    # Pick the picture that matches the number of mistakes.
    print(PICTURES[mistakes])
    print()
 
    # The word with blanks,
    print("Word:     ", show_word(secret_word, guessed_letters))
 
    # All letters tried so far. " ".join(...) puts a space between them:
    # ["a", "x", "t"] becomes "a x t"
    print("Guessed:  ", " ".join(guessed_letters))
 
    # How many mistakes, e.g. "Mistakes: 3 of 9"
    print("Mistakes: ", mistakes, "of", MAX_MISTAKES)
    print()
 
 

# Ask until the player types one new letter.
# Wrong inputs (like "ab", "5", nothing, or a letter used before)
# are rejected and the player is asked again.


def ask_for_letter(guessed_letters):
    while True:
        # input() waits until the player types something and presses Enter.
        # .lower() turns "A" into "a", so big and small letters count the same.
        guess = input("Guess a letter: ").lower()
 
        # Does the player want to leave? Then give back "quit".
        # This check must come FIRST, because "quit" has more than 1 letter.
        if guess == "quit":
            return "quit"
 
        # len(guess) = how many characters were typed.
        elif len(guess) != 1:
            # Not exactly 1 sign -> "one letter!" message
            print("ONE letter! The hangman doesn't have time for essays.")
        # .isalpha() = True if it is a letter (not a number or a sign).
        elif not guess.isalpha():
            # 1 sign, but no letter -> "not a letter!" message
            print("That's not a letter! Did your cat walk over the keyboard?")
        # Was this letter already tried before?
        elif guess in guessed_letters:
            print("Deja vu! You already tried that letter.")
        # Everything is fine -> give the letter back. The loop ends.
        else:
            return guess
 
 

# Play one full game with the given secret word.
# main part- it repeats "ask - check - show" until
# the player wins or loses.

def play(secret_word):
    # Make the word lowercase, so "CATS" works the same as "cats".
    secret_word = secret_word.lower()
 
    # The game state: only these 3 things describe the whole game.
    #   secret_word     -> the word to guess (set above)
    #   guessed_letters -> list of all letters tried so far (empty at start)
    #   mistakes        -> how many wrong guesses (0 at start)
    guessed_letters = []
    mistakes = 0
 
    # Show the empty game once before the first guess
    print_game_state(secret_word, guessed_letters, mistakes)
 
    # Repeat until break out of the loop (win or lose)
    while True:
        # 1. Get one new letter from the player
        guess = ask_for_letter(guessed_letters)
 
        # Did the player type "quit"? Then say goodbye and end the game.
        if guess == "quit":
            print(QUIT_PICTURE)
            print("The secret word was:", secret_word, "- you'll never know if you would have made it!")
            break
 
        # 2. Remember this letter. .append() adds it to the end of the list
        guessed_letters.append(guess)
 
        # 3. Check if the letter is in the secret word.
        if guess in secret_word:
            print("'" + guess + "'", "is in the word! Nailed it. The hangman just gave you a high five.")
        else:
            print("'" + guess + "'", "is NOT in the word. Oops! The rope just got a bit tighter.")
            # Wrong guess -> one more mistake (one more part of the hangman).
            mistakes = mistakes + 1
 
        # 4. Show the new game state
        print_game_state(secret_word, guessed_letters, mistakes)
 
        # 5. Check if the game is over
        # Won: all letters of the word are guessed
        if is_word_guessed(secret_word, guessed_letters):
            print(WIN_PICTURE)
            print("The word was", secret_word, ". The hangman just added you to his will. You get the rope.")
            print()
            print("You needed", len(guessed_letters), "guesses and made", mistakes, "mistakes.")
 
            # comment that depends on how many mistakes were made
            if mistakes == 0:
                print("ZERO mistakes?! Are you a mind reader?")
            elif mistakes <= 3:
                print("Only", mistakes, "mistakes! The hangman barely noticed the danger.")
            elif mistakes <= 6:
                print(mistakes, "mistakes... not bad! The hangman only needs a little therapy.")
            else:
                print("PHEW!", mistakes, "mistakes! That was close. The hangman needs a nap now.")
            break  # leaves the while loop -> game ends
 
        # Lost: the hangman picture is complete.
        if mistakes == MAX_MISTAKES:
            print(LOSE_PICTURE)
            print("The word was", secret_word + ". The hangman removed you from his will.")
            break
 
 

# Start of the program - only runs when you start this file directly

if __name__ == "__main__":
    # Ask Player 1 for a secret word.
    # .strip() removes extra spaces at the start and the end.
    print()
    print("Welcome to HANGMAN! A life is in your hands. No pressure.")
    print()
    print("Want to give up? Type quit instead of a letter.")
    print()
    word = input("Player 1, whisper a secret word (or press ENTER and let fate decide): ").strip()

    # Did Player 1 type "quit"? Then leave before the game even starts.
    if word.lower() == "quit":
        print(QUIT_PICTURE)

    # Did Player 1 type nothing (just pressed Enter)?
    # Then the text is empty: "" -> pick a random word from my WORDS list.
    elif word == "":
        word = random.choice(WORDS)
        print("The computer rolled the dice. Good luck, you will need it!")
    else:
        # Print  empty lines so Player 2 cannot see the word anymore.
        print("\n" * 10)
        print("Player 1 chose a word. Player 2, the hangman's future depends on you!")
 
    # Start the game with this word (but not if Player 1 typed "quit").
    if word.lower() != "quit":
        play(word)