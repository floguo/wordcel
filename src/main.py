import tkinter as tk # Basic Tkinter
from tkinter import ttk # Themed Tkinter
import requests # HTTP library for API calls
import pygame # Audio playback
import os # File system operations
import tempfile # Temporary file operations (for audio files)
import typing

class DictionaryApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root # Main window
        self.root.title("Wordcel") # Window title
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/" # DictionaryAPI URL
        pygame.mixer.init() # Initialize audio mixer for pronunciation
        self.root.configure(bg="#f0f0f0") # Light gray background

        # Set minimum window size
        self.root.minsize(300,400)
        
        # Search frame
        search_frame = ttk.Frame(root, padding="24")
        search_frame.grid(row=1, column=0, sticky="ew") # Position at top, sticky east-west
        # Label for search field
        search_label = ttk.Label(search_frame, text="Look up a word")
        search_label.grid(row=0, column=0, sticky='w')
        # Word entry field
        self.word_entry = ttk.Entry(search_frame, width=32) 
        self.word_entry.grid(row=1, column=0) # Position at top, sticky east-west
        # Search button
        search_button = ttk.Button(search_frame, text="Define", command=self.search_word)
        search_button.grid(row=1, column=1, sticky='ns')

        # Configure columns and rows
        search_frame.columnconfigure(0, weight=0)
        search_frame.columnconfigure(1, weight=1)
        
        # Result frame
        result_frame = ttk.Frame(root, padding=(24, 0, 24, 24))
        result_frame.grid(row=2, column=0, sticky="nsew")
        # Result text field
        self.result_text = tk.Text(result_frame, height=24, width=55, wrap=tk.WORD) 
        self.result_text.grid(row=0, column=0) # Fill frame
        
        # Bind Enter key to search
        self.word_entry.bind('<Return>', lambda e: self.search_word()) # Lambda (anonymous function) takes an event e as argument

    def search_word(self):
        # Get word (string)from user entry, strip whitespace, convert to lowercase
        word = self.word_entry.get().strip().lower() 
        # If no word (emp) is entered, return to avoid unnecessary API call
        if not word:
            return
            
        try:
            # Make API call to DictionaryAPI
            response = requests.get(f"{self.api_url}{word}")
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Handle successful API call (status code 200)
            if response.status_code == 200:
                data = response.json()[0]
                # Debug API response in terminal
                print("API response:", data)
                self.display_definition(data)
            else:
                # Error: Word not found
                self.result_text.insert(tk.END, "Word not found. Try another word?")
                
        except Exception as e:
            # Error: API call failed
            self.result_text.insert(tk.END, "An error occurred. Please try again.")
    
    def _setup_acccessibility(self):
        # Bind keyboard shortcuts
        # self.root.bind('<Control-f>', lambda e: self_word_entry.focus()) # TODO: Focus on search field
        self.word_entry.bind('<Return>', lambda e: self.search_word()) # Search when Enter key is pressed

        # Set tab order
        self.word_entry.lift()

        # Add tooltips
        self._create_tooltip(self.word_entry, "Enter a word to search")

        # Set ARIA labels
        self.word_entry.configure(name="word_search_entry")
        self.result_text.configure(name="definition_results")

        # Make text widget read-only, allow text to be copied
        self.result_text.configure(state="disabled")

    def play_pronunciation(self, audio_url):
        # Initialize audio mixer if not already initialized
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Download audio file
            response = requests.get(audio_url)
            if response.status_code == 200:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                # Clean up temp file after delay
                self.root.after(2000, lambda: os.unlink(temp_path))
            else:
                print(f"Failed to download audio file: {response.status_code}")
        except Exception as e:
            print(f"Error playing pronunciation audio: {e}")

    def display_definition(self, data):
        # Add play pronunciation audio button
        # Frame to hold play audio button
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=3, column=0)

        # Add buttons for available audio sources
        for phonetic in data.get('phonetics', []):
            if phonetic.get('audio'):
                audio_url = phonetic['audio']
                # Determine regional accent based on audio URL (UK or US)
                region = 'UK' if 'uk' in audio_url else 'AU' if 'au' in audio_url else 'US'
                # If audio URL is found, create a button to play pronunciation
                ttk.Button(
                    button_frame, 
                    text=f"Play {region} pronunciation",
                    command=lambda url=audio_url: self.play_pronunciation(url)
                ).pack(side='left', pady=(0, 24))

        # Display word and definitions
        word = data['word'] # Get word from API response
        phonetic = data.get('phonetic', '') # Get phonetic symbol from API response
        self.result_text.insert(tk.END, f"{word.capitalize()} {phonetic}\n\n")

        # Display etymology if available
        if 'origin' in data:
            self.result_text.insert(tk.END, f"Etymology: {data['origin']}\n\n") 
                               
        # Display meanings and definitions  
        # Create numbered list of meanings and definitions                           
        for i, meaning in enumerate(data['meanings'], 1):
            pos = meaning['partOfSpeech']
            definition = meaning['definitions'][0]['definition']
            
            # Insert numbered list of meanings and definitions
            self.result_text.insert(tk.END, f"{i}. {pos}\n")
            self.result_text.insert(tk.END, f"Definition: {definition}\n")
            
            # Show example if available
            example = meaning['definitions'][0].get('example', '')
            if example:
                self.result_text.insert(tk.END, f"Example: {example}\n")
            
            self.result_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()