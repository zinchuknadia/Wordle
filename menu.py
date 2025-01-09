import customtkinter as ctk
import game  # Import the Wordle game module
import settings  # Import the settings module (to be implemented)

class WordleMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wordle Menu")
        self.geometry("400x300")
        #self.configure(fg_color="gray")  # Set the background color

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Wordle", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Buttons for menu options
        self.start_button = ctk.CTkButton(self, text="Start Game", font=("Helvetica", 16), command=self.start_game)
        self.start_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self, text="Settings", font=("Helvetica", 16), command=self.open_settings)
        self.settings_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self, text="Exit", font=("Helvetica", 16), command=self.exit_game)
        self.exit_button.pack(pady=10)

    def start_game(self):
        """Launch the Wordle game."""
        #self.destroy()  # Close the menu window
        self.disable_buttons()
        game.play(self)  # Call the game module's play function
        #self.enable_buttons()

    def open_settings(self):
        """Open the settings menu."""
        self.disable_buttons()
        settings.show_settings(self)  # Call the settings module's show_settings function

    def exit_game(self):
        """Exit the application."""
        self.destroy()  # Close the menu window

    def disable_buttons(self):
        self.start_button.configure(state="disabled")
        self.settings_button.configure(state="disabled")
        self.exit_button.configure(state="disabled")

    def enable_buttons(self):
        self.start_button.configure(state="normal")
        self.settings_button.configure(state="normal")
        self.exit_button.configure(state="normal")

# Main function to launch the menu
def main():
    app = WordleMenu()
    app.mainloop()

if __name__ == "__main__":
    main()

