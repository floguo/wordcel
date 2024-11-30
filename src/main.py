import tkinter as tk
from tkinter import ttk
from tkmacosx import Button  # Import tkmacosx.Button
import requests
import pygame
import os
import tempfile


class DictionaryApp:
    def __init__(self, root):
        """Initialize the dictionary application."""
        self.root = root
        self.root.title("Wordcel")
        self.root.geometry("500x700")
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        pygame.mixer.init()

        # Define colors for tkmacosx.Button
        self.button_styles = {
            'bg': '#3498db',  # Background color
            'fg': '#FFFFFF',  # Foreground color
            'hover': '#5dade2',  # Hover background
        }

        # Apply consistent styling and build the UI
        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self):
        """Configure custom styles for the application."""
        # Define a color palette
        self.COLORS = {
            'bg': '#2E2E2E',        # Dark background
            'fg': '#FFFFFF',        # Light foreground (text)
            'text_bg': '#2E2E2E',   # Background for text widgets
            'error': '#FF4444',     # Error text color
        }

        # Set root window background color
        self.root.configure(background=self.COLORS['bg'])

    def _create_custom_button(self, parent, text, command, **kwargs):
        """
        Helper to create tkmacosx.Button with consistent styles.
        """
        return Button(
            parent,
            text=text,
            bg=self.button_styles['bg'],
            fg=self.button_styles['fg'],
            activebackground=self.button_styles['hover'],
            activeforeground=self.button_styles['fg'],
            borderless=1,
            command=command,
            **kwargs
        )

    def _setup_ui(self):
        """Build the user interface."""
        # Frame for the search bar
        search_frame = ttk.Frame(self.root, padding=20)
        search_frame.pack(fill="x", pady=(20, 10))

        # Label for the search input
        search_label = ttk.Label(
            search_frame, text="Look up a word:",
            background=self.COLORS['bg'], foreground=self.COLORS['fg']
        )
        search_label.pack(anchor="w")

        # Input field for entering the word
        self.word_entry = ttk.Entry(search_frame, width=40)
        self.word_entry.pack(fill="x", pady=5)

        # Button to trigger the search
        search_button = self._create_custom_button(
            search_frame, "Define", self.search_word
        )
        search_button.pack(pady=10)

        # Frame for displaying results
        result_frame = ttk.Frame(self.root, padding=20)
        result_frame.pack(fill="both", expand=True, pady=(10, 20))

        # Add a scrollbar to the result frame
        self.scrollbar = ttk.Scrollbar(result_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Non-editable text widget to display definitions
        self.result_text = tk.Text(
            result_frame,
            height=20,
            wrap="word",
            font=("Helvetica", 12),
            relief="flat",
            borderwidth=0,
            background=self.COLORS['text_bg'],
            foreground=self.COLORS['fg'],
            yscrollcommand=self.scrollbar.set,
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        self.result_text.configure(state="disabled")  # Make the text widget read-only
        self.scrollbar.config(command=self.result_text.yview)  # Attach scrollbar to text widget

        # Frame for audio buttons
        self.audio_section_frame = ttk.Frame(self.root, padding=(20, 10))
        self.audio_section_frame.pack(fill="x")

        # Title for the audio section
        self.audio_title = ttk.Label(
            self.audio_section_frame, text="Play Audio", font=("Helvetica", 14, "bold"),
            background=self.COLORS['bg'], foreground=self.COLORS['fg']
        )
        self.audio_title.pack(anchor="center", pady=(5, 10))

        # Frame to hold the pronunciation buttons
        self.pronunciation_frame = ttk.Frame(self.audio_section_frame, padding=(0, 10))
        self.pronunciation_frame.pack(anchor="center", pady=10)

    def search_word(self):
        """Search for a word and display the results."""
        word = self.word_entry.get().strip().lower()
        if not word:
            self._update_result_text("Please enter a word.", is_error=True)
            return

        # Clear previous pronunciation buttons
        for widget in self.pronunciation_frame.winfo_children():
            widget.destroy()

        try:
            response = requests.get(f"{self.api_url}{word}")
            if response.status_code == 200:
                data = response.json()[0]
                self.display_definition(data)
            else:
                self._update_result_text("Word not found. Try another word.", is_error=True)
        except Exception as e:
            self._update_result_text(f"An error occurred: {e}", is_error=True)

    def display_definition(self, data):
        """Display the definition and pronunciation buttons."""
        # Clear previous content
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)

        # Display the word and phonetics
        word = data['word'].capitalize()
        phonetic = data.get('phonetic', '')
        self.result_text.insert(tk.END, f"{word} {phonetic}\n\n", "title")

        # Display meanings and definitions
        for meaning in data.get('meanings', []):
            part_of_speech = meaning['partOfSpeech'].capitalize()
            self.result_text.insert(tk.END, f"{part_of_speech}:\n", "pos")
            for definition in meaning['definitions']:
                self.result_text.insert(tk.END, f" - {definition['definition']}\n", "definition")
                if example := definition.get('example'):
                    self.result_text.insert(tk.END, f"   Example: {example}\n", "example")
            self.result_text.insert(tk.END, "\n")

        # Add pronunciation buttons for available audio
        self._add_pronunciation_buttons(data.get('phonetics', []))

        # Configure text widget styles
        self.result_text.tag_configure("title", font=("Helvetica", 16, "bold"))
        self.result_text.tag_configure("pos", font=("Helvetica", 14, "italic"), foreground="#d1d1d1")
        self.result_text.tag_configure("definition", font=("Helvetica", 12))
        self.result_text.tag_configure("example", font=("Helvetica", 12, "italic"), foreground="#b0c4de")

        # Disable editing in the result text widget
        self.result_text.configure(state="disabled")

    def _add_pronunciation_buttons(self, phonetics):
        """Add buttons to play pronunciation audio."""
        for phonetic in phonetics:
            if audio_url := phonetic.get('audio'):
                # Determine accent if specified
                accent = 'UK' if 'uk' in audio_url else 'US'
                button = self._create_custom_button(
                    self.pronunciation_frame,
                    f"{accent} Pronunciation",
                    lambda url=audio_url: self.play_pronunciation(url)
                )
                button.pack(side="left", padx=10)

    def play_pronunciation(self, audio_url):
        """Download and play the pronunciation audio."""
        try:
            response = requests.get(audio_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name

                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                self.root.after(5000, lambda: os.unlink(temp_path))  # Clean up after playback
            else:
                self._update_result_text("Failed to load pronunciation audio.", is_error=True)
        except Exception as e:
            self._update_result_text(f"Error playing audio: {e}", is_error=True)

    def _update_result_text(self, text, is_error=False):
        """Update the result text widget."""
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()