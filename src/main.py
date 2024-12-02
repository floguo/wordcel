import tkinter as tk
from tkinter import ttk
import requests
import pygame
import os
import tempfile
from tkmacosx import Button
from colorsys import rgb_to_hls, hls_to_rgb

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

    def _darken_color(self, hex_color, factor=0.8):
        """
        Darkens a hex color by a given factor.
        Args:
            hex_color (str): The hex color code (e.g., "#3498db").
            factor (float): A multiplier (<1 to darken, >1 to lighten).
        Returns:
            str: The darkened hex color code.
        """
        # Convert hex to RGB
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Convert RGB to HLS
        h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        # Apply the darkening factor to lightness
        l = max(0, min(1, l * factor))
        # Convert back to RGB
        r, g, b = hls_to_rgb(h, l, s)
        # Return as hex
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
    
    def int_to_roman(self,num):
        """Convert an integer to lowercase Roman numerals."""
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]

        roman_numeral = ""
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_numeral += syms[i]
                num -= val[i]
            i += 1
        return roman_numeral
    
    def _apply_hover_effect(self, button, normal_color, hover_factor=0.8):
        """
        Apply hover effect to a button.
        Args:
            button: The button to which the hover effect is applied.
            normal_color: The default background color of the button.
            hover_factor: The factor by which to darken the color on hover.
        """
        button.bind(
            "<Enter>",
            lambda e: button.config(bg=self._darken_color(normal_color, factor=hover_factor)),
        )
        button.bind(
            "<Leave>",
            lambda e: button.config(bg=normal_color),
        )
        # Reset active state after mouse click
        button.bind(
            "<ButtonRelease-1>",
            lambda e: button.config(bg=normal_color),
        )

    def _setup_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()

        # Define a color palette
        self.COLORS = {
            'bg': '#2E2E2E',        # Dark background
            'fg': '#FFFFFF',        # Light foreground (text)
            'accent': '#3498db',    # Accent color (blue for buttons)
            'hover': '#5dade2',     # Hover state for buttons
            'text_bg': '#2E2E2E',   # Background for text widgets (matches root)
            'error': '#FF4444',     # Error text color
        }

        # Configure frame and label styles
        style.configure("TFrame")
        style.configure("TLabel", font=("Helvetica", 12))

        # Configure text entry styles
        style.configure("TEntry", font=("Helvetica", 12), padding=10)

    def _setup_ui(self):
        """Build the user interface."""
        # Frame for the search bar
        search_frame = ttk.Frame(self.root, padding=(20, 10))
        search_frame.pack(fill="x", pady=(20, 0))

        # Label for the search input
        search_label = ttk.Label(
            search_frame, text="Look up a word:",
        )
        search_label.pack(anchor="w")

        # Input field for entering the word
        self.word_entry = ttk.Entry(search_frame, width=40)
        self.word_entry.pack(fill="x", pady=5)

        # Button to trigger the search
        search_button = Button(
            search_frame, 
            text="Define word", 
            command=self.search_word, 
            bg=self.COLORS['accent'], 
            fg=self.COLORS['fg'], 
            activebackground=self.COLORS['hover'], 
            activeforeground=self.COLORS['fg'], 
            borderless=1, 
            font=("Helvetica", 12, "bold")
        )
        search_button.pack(pady=10)
        self._apply_hover_effect(search_button, self.COLORS['accent'])

        # Bind Return key to trigger search
        self.root.bind("<Return>", lambda e: self.search_word())
        # Bind Alt+S to focus search
        self.root.bind("<Alt-s>", lambda e: self.word_entry.focus_set())

        # Frame for pronunciation buttons
        self.audio_section_frame = ttk.Frame(self.root)
        self.audio_section_frame.pack(fill="x")

        # Title for the audio section
        self.audio_title = ttk.Label(
            self.audio_section_frame, text="Play Audio", font=("Helvetica", 14, "bold")
        )

        # Frame to hold the pronunciation buttons
        self.pronunciation_frame = ttk.Frame(self.audio_section_frame)

        # Frame for displaying the results with a scrollbar
        result_frame = ttk.Frame(self.root, padding=20)
        result_frame.pack(fill="both", expand=True, pady=(0,20))

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
            yscrollcommand=self.scrollbar.set,
            padx=20,
            pady=20
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        self.result_text.configure(state="disabled")  # Make the text widget read-only
        self.display_empty_state() # Show empty state initially
        self.scrollbar.config(command=self.result_text.yview)  # Attach scrollbar to text widget

        # Bind Enter key to trigger search
        self.word_entry.bind("<Return>", lambda e: self.search_word())

    def search_word(self):
        """Search for a word and display the results."""
        word = self.word_entry.get().strip().lower()
        if not word: # Show empty state if input is empty
            self.display_empty_state()
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
        self.result_text.insert(tk.END, f"{word} {phonetic}\n", "title")

        # Display meanings and definitions
        for index, meaning in enumerate(data.get('meanings', []), start=1):
            part_of_speech = meaning['partOfSpeech'].capitalize()
            self.result_text.insert(tk.END, f"{index}. {part_of_speech}:\n", "pos")

            for sub_index, definition in enumerate(meaning['definitions'], start=1):
                # Use Roman numerals for sub-index
                roman_index = self.int_to_roman(sub_index)
                formatted_roman_index = f"{roman_index:>4}. " if roman_index else ""
                self.result_text.insert(
                    tk.END,
                    formatted_roman_index,
                    "definition_number"
                )
                # Indent the definition content as a block
                self.result_text.insert(
                    tk.END,
                    f"{definition['definition']}\n",
                    "definition"
                )
                if example := definition.get('example'):
                    self.result_text.insert(
                        tk.END,
                        f"Example: {example}\n",
                        "example"
                    )
                self.result_text.insert(tk.END, "\n")  # Add space after each meaning
        
        # Add pronunciation buttons for available audio
        self._add_pronunciation_buttons(data.get('phonetics', [])) 

        # Configure text widget styles dynamically
        self.result_text.tag_configure(
            "title", 
            font=("Helvetica", 16, "bold"), 
            lmargin2=24
        )
        self.result_text.tag_configure(
            "pos", 
            font=("Helvetica", 14, "italic"), 
            spacing3=8, 
            lmargin2=24
        )
        self.result_text.tag_configure(
            "definition_number", 
            font=("Helvetica", 12, "bold"), 
            lmargin1=40,
            lmargin2=40,
            tabs=[60]
        )
        self.result_text.tag_configure(
            "definition", 
            font=("Helvetica", 12), 
            lmargin1=60,
            lmargin2=60, 
            spacing3=8
        )  # Left margin for blocks
        self.result_text.tag_configure(
            "example", 
            font=("Helvetica", 12, "italic"), 
            lmargin1=80,
            lmargin2=80, 
            spacing3=8
        )  # Further indentation
        self.result_text.configure(state="disabled")

    def display_empty_state(self):
        """Display the empty state."""
        self.result_text.configure(state="normal") # Enable editing
        self.result_text.delete("1.0", tk.END) # Clear previous content

        # Add empty state message
        self.result_text.insert(tk.END, "\n\n🔍 Welcome to Wordcel!\n\n", "empty_title")
        self.result_text.insert(
            tk.END,
            "Type a word in the search bar above and press 'Enter' or click 'Define Word' to see the definition.\n\n",
            "empty_text"
        )

         # Configure text widget styles for empty state
        self.result_text.tag_configure("empty_title", font=("Helvetica", 16, "bold"), foreground="#3498db", justify="center")
        self.result_text.tag_configure("empty_text", font=("Helvetica", 12), foreground="#666666", justify="center")
        self.result_text.tag_configure("empty_hint", font=("Helvetica", 12, "italic"), foreground="#888888", justify="center")

        # Disable editing
        self.result_text.configure(state="disabled")

    def _add_pronunciation_buttons(self, phonetics):
        """Add buttons to play pronunciation audio."""
        # Clear any existing buttons
        for widget in self.pronunciation_frame.winfo_children():
            widget.destroy()

        # Initalize `buttons_created` to False
        buttons_created = False

        # Check if there are any valid audio URLs
        audio_found = False
        for phonetic in phonetics:
            if audio_url := phonetic.get('audio'):
                audio_found = True
                # Determine accent if specified
                accent = 'UK' if 'uk' in audio_url else 'US' if 'us' in audio_url else 'AU' if 'au' in audio_url else 'Unknown'

                # Create tkmacosx.Button with custom styling
                button = Button(
                    self.pronunciation_frame,
                    text=f"{accent} Pronunciation",
                    bg=self.COLORS['accent'],        # Background color
                    fg=self.COLORS['fg'],            # Foreground (text) color
                    activebackground=self.COLORS['hover'],  # Hover background color
                    activeforeground=self.COLORS['fg'],     # Hover text color
                    borderless=1,                    # Removes the button border
                    font=("Helvetica", 12, "bold"),  # Font styling
                    command=lambda url=audio_url: self.play_pronunciation(url),
                )
                button.pack(side="top", pady=5)

                self._apply_hover_effect(button, self.COLORS['accent'])

                # Bind <Return> key to the same command as the button click
                button.bind(
                    "<Return>",
                    lambda e, url=audio_url: self.play_pronunciation(url),
                )

        # Show or hide the "Play Audio" heading and buttons
        if audio_found:
            self.audio_section_frame.pack(fill="x", pady=0)
            self.audio_title.pack(anchor="center", pady=(2, 5))  # Ensure the title is visible
            self.pronunciation_frame.pack(anchor="center", pady=0)
            buttons_created = True
        else:
            self.audio_section_frame.pack_forget()
            self.audio_title.pack_forget()  # Hide the title when no audio is found

        if not buttons_created:
            # No audio available - show a placeholder message
            no_audio_label = ttk.Label(
                self.pronunciation_frame, text="No pronunciation available.",
            )
            no_audio_label.pack(anchor="center")
            
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