import customtkinter as ctk
import random
import ctypes

import settings

# Load the shared library
lib = ctypes.CDLL('./game.dll')  # Replace with the correct path
lib.evaluate_guess.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# Function to evaluate the guess using the shared library
def evaluate_guess(target, guess):
    feedback = ctypes.create_string_buffer(len(guess))
    lib.evaluate_guess(target.encode('utf-8'), guess.encode('utf-8'), feedback)
    return feedback.value.decode('utf-8')

# Main CustomTkinter App
class WordleGame(ctk.CTk):
    def __init__(self, main_menu, word_list, target_word, attempt_limit, word_length):
        super().__init__()
        self.main_menu = main_menu
        self.title("Wordle Game")
        self.geometry("400x600")
        self.word_list = word_list
        self.target_word = target_word
        self.max_attempts = attempt_limit
        self.word_length = word_length
        self.current_attempt = 0

        # UI Elements
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

        # Create grid for guesses
        self.guess_labels = []
        self.active_row = []
        for i in range(self.max_attempts):
            row = []
            for j in range(self.word_length):
                label = ctk.CTkLabel(
                    self.grid_frame,
                    text="",
                    font=("Helvetica", 20),
                    width=50,
                    height=50,
                    corner_radius=5,
                    fg_color="gray",
                )
                label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row.append(label)
            self.guess_labels.append(row)

        # Create active row entries for the first attempt
        self.create_active_row()

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_guess)
        self.submit_button.pack(pady=10)

        # Bind Enter key to submit guess
        self.bind("<Return>", lambda event: self.submit_guess())

        # Enable main menu buttons when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_active_row(self):
        """Create entry boxes in the active row for the current attempt."""
        self.active_row = []
        for j in range(self.word_length):
            entry = ctk.CTkEntry(
                self.grid_frame,
                font=("Helvetica", 20),
                justify="center",
                width=50,
            )
            entry.grid(row=self.current_attempt, column=j, padx=5, pady=5, sticky="nsew")
            entry.bind("<KeyRelease>", self.handle_keypress(j))  # Bind key event
            self.active_row.append(entry)

        # Use `after` to ensure the focus is set after the window is fully initialized
        self.after(100, lambda: self.active_row[0].focus())

    def handle_keypress(self, index):
        """Handle key presses in the active row entries."""

        def handler(event):
            entry = self.active_row[index]
            # Handle backspace
            if event.keysym == "BackSpace":
                if entry.get():  # If the current box is not empty
                    entry.delete(0, ctk.END)  # Clear the content
                elif index > 0:  # If the current box is empty, move to the previous box
                    self.active_row[index - 1].focus()
                    self.active_row[index - 1].delete(0, ctk.END)
            # Handle typing a letter
            elif event.keysym.isalpha() and len(entry.get()) == 1:
                if index < self.word_length - 1:
                    self.active_row[index + 1].focus()

        return handler

    def submit_guess(self):
        # Collect the guess from the active row
        guess = "".join(entry.get().lower() for entry in self.active_row)
        if len(guess) != self.word_length or guess not in self.word_list:
            self.result_label.configure(text=f"Invalid guess! Enter a {self.word_length}-letter word.")
            return

        # Clear the result label if the guess is valid
        self.result_label.configure(text="")

        # Evaluate the guess
        feedback = evaluate_guess(self.target_word, guess)

        # Replace entries with labels and update colors
        for j, (letter, fb) in enumerate(zip(guess, feedback)):
            entry = self.active_row[j]
            entry.destroy()  # Remove the entry box
            label = ctk.CTkLabel(
                self.grid_frame,
                text=letter.upper(),
                font=("Helvetica", 20),
                width=50,
                height=50,
                corner_radius=5,
            )
            label.grid(row=self.current_attempt, column=j, padx=5, pady=5, sticky="nsew")
            self.guess_labels[self.current_attempt][j] = label  # Replace in the grid
            # Update color based on feedback
            if fb == "2":
                label.configure(fg_color="green", text_color="white")
            elif fb == "1":
                label.configure(fg_color="yellow", text_color="black")
            else:
                label.configure(fg_color="gray", text_color="white")

        # Check win/lose conditions
        if feedback == "2" * self.word_length:
            self.result_label.configure(text="🎉 Congratulations! You guessed the word!")
            self.submit_button.configure(state="disabled")
            self.unbind("<Return>")  # Unbind the Enter key
            return

        self.current_attempt += 1
        if self.current_attempt == self.max_attempts:
            self.result_label.configure(text=f"Game over! The word was: {self.target_word.upper()}")
            self.submit_button.configure(state="disabled")
            self.unbind("<Return>")  # Unbind the Enter key
            return

        # Create new active row for the next attempt
        self.create_active_row()

    def on_close(self):
        """Handle window close event."""
        self.main_menu.enable_buttons()
        self.destroy()


# Run the game
def play( main_menu):
    # Load word list and choose a target word
    game_settings = settings.load_settings()
    word_list_language = game_settings["language"]
    word_list = game_settings["word_list"]
    attempt_limit = game_settings["attempts"]
    word_length = game_settings["word_length"]
    target_word = random.choice(word_list)

    app = WordleGame(main_menu, word_list, target_word, attempt_limit, word_length)
    app.mainloop()

