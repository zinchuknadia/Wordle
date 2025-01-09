import json
import customtkinter as ctk
from wordfreq import top_n_list

# Language mapping
LANGUAGE_MAP = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian"
}

# Reverse mapping for saving and loading
LANGUAGE_MAP_REVERSE = {v: k for k, v in LANGUAGE_MAP.items()}

# Language selection combobox values
LANGUAGE_NAMES = list(LANGUAGE_MAP.values())

# Default settings
DEFAULT_SETTINGS = {
    "attempts": 6,
    "word_length": 5,
    "language": "en",
    "word_list": []
}

SETTINGS_FILE = "wordle_settings.json"

# Function to generate word list based on word length
def generate_word_list(word_length, language):
    return [word for word in top_n_list(language, 100000) if len(word) == word_length]

# Load settings from file or use defaults
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            settings["word_list"] = generate_word_list(settings["word_length"], settings["language"])
            return settings
    except FileNotFoundError:
        settings = DEFAULT_SETTINGS.copy()
        settings["word_list"] = generate_word_list(settings["word_length"], settings["language"])
        save_settings(settings)
        return settings

# Save settings to file
def save_settings(settings):
    settings_to_save = settings.copy()
    settings_to_save["word_list"] = []
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_to_save, f, indent=4)

# GUI Application
class WordleSettingsApp(ctk.CTk):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu

        self.title("Wordle Settings")
        self.geometry("400x400")  # Increased height for the new language section

        self.settings = load_settings()

        # Center the entire layout
        self.grid_columnconfigure(0, weight=1)

        # Frame for settings with matching background
        settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        settings_frame.pack(pady=20)

        # Number of attempts
        attempts_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        attempts_frame.grid(row=0, column=0, pady=10)
        self.attempts_label = ctk.CTkLabel(attempts_frame, text="Number of Attempts:")
        self.attempts_label.grid(row=0, column=0, padx=10)
        self.attempts_entry = ctk.CTkEntry(attempts_frame, width=100)
        self.attempts_entry.insert(0, str(self.settings['attempts']))
        self.attempts_entry.grid(row=0, column=1, padx=10)

        # Word length
        word_length_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        word_length_frame.grid(row=1, column=0, pady=10)
        self.word_length_label = ctk.CTkLabel(word_length_frame, text="Word Length:")
        self.word_length_label.grid(row=0, column=0, padx=10)
        self.word_length_entry = ctk.CTkEntry(word_length_frame, width=100)
        self.word_length_entry.insert(0, str(self.settings['word_length']))
        self.word_length_entry.grid(row=0, column=1, padx=10)

        # Language selection
        language_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        language_frame.grid(row=2, column=0, pady=10)
        self.language_label = ctk.CTkLabel(language_frame, text="Select Language:")
        self.language_label.grid(row=0, column=0, padx=10)
        self.language_combobox = ctk.CTkComboBox(
            language_frame,
            values=LANGUAGE_NAMES,  # Use user-friendly names
            command=self.update_language,
        )
        # Set the initial language based on the loaded settings
        self.language_combobox.set(LANGUAGE_MAP[self.settings['language']])
        self.language_combobox.grid(row=0, column=1, padx=10)

        # Buttons
        self.reset_button = ctk.CTkButton(self, text="Reset to Default", command=self.reset_settings)
        self.reset_button.pack(pady=10)
        self.save_button = ctk.CTkButton(self, text="Save and Close", command=self.save_and_close)
        self.save_button.pack(pady=10)

        # Enable main menu buttons when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_attempts(self):
        value = self.attempts_entry.get()
        if value.isdigit() and 1 <= int(value) <= 10:
            self.settings['attempts'] = int(value)
            self.attempts_label.configure(text=f"Number of Attempts:")
        else:
            self.attempts_label.configure(text="Invalid Input! Enter a number (1-10).")

    def update_word_length(self):
        value = self.word_length_entry.get()
        if value.isdigit() and 3 <= int(value) <= 10:
            self.settings['word_length'] = int(value)
            self.word_length_label.configure(text=f"Word Length:")
            self.settings['word_list'] = generate_word_list(self.settings['word_length'], self.settings['language'])
        else:
            self.word_length_label.configure(text="Invalid Input! Enter a number (3-10).")

    def update_language(self, selected_language):
        # Update the settings with the selected language code
        self.settings['language'] = LANGUAGE_MAP_REVERSE[selected_language]
        self.settings['word_list'] = generate_word_list(self.settings['word_length'], self.settings['language'])

    def reset_settings(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.settings['word_list'] = generate_word_list(self.settings['word_length'], self.settings['language'])
        self.attempts_entry.delete(0, ctk.END)
        self.attempts_entry.insert(0, str(self.settings['attempts']))
        self.word_length_entry.delete(0, ctk.END)
        self.word_length_entry.insert(0, str(self.settings['word_length']))
        self.language_combobox.set(LANGUAGE_MAP[self.settings['language']])
        self.attempts_label.configure(text=f"Number of Attempts:")
        self.word_length_label.configure(text=f"Word Length:")

    def save_and_close(self):
        """Validate inputs and save settings only if all inputs are valid."""
        attempts_valid = self.validate_attempts()
        word_length_valid = self.validate_word_length()

        if attempts_valid and word_length_valid:
            save_settings(self.settings)
            self.after(100, self.on_close)  # Use after to ensure all tasks are processed before closing
            # Close the window only if all inputs are valid
        else:
            self.save_button.configure(state="normal")  # Keep the save button enabled

    def validate_attempts(self):
        """Validate the number of attempts input."""
        value = self.attempts_entry.get()
        if value.isdigit() and 1 <= int(value) <= 10:
            self.settings['attempts'] = int(value)
            self.attempts_label.configure(text="Number of Attempts:")
            return True
        else:
            self.attempts_label.configure(text="Invalid Input! Enter a number (1-10).")
            return False

    def validate_word_length(self):
        """Validate the word length input."""
        value = self.word_length_entry.get()
        if value.isdigit() and 3 <= int(value) <= 10:
            self.settings['word_length'] = int(value)
            self.word_length_label.configure(text="Word Length:")
            self.settings['word_list'] = generate_word_list(self.settings['word_length'], self.settings['language'])
            return True
        else:
            self.word_length_label.configure(text="Invalid Input! Enter a number (3-10).")
            return False

    def on_close(self):
        self.main_menu.enable_buttons()
        self.destroy()

# Run the application
def show_settings(main_menu):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = WordleSettingsApp(main_menu)
    app.mainloop()
