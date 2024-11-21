import tkinter as tk
from tkinter import ttk
import requests
import pygame
import os
import tempfile

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordcel")
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        pygame.mixer.init() # Initialize audio mixer for pronunciation
        
        # Search frame
        search_frame = ttk.Frame(root, padding="10")
        search_frame.grid(row=0, column=0, sticky="ew")
        
        self.word_entry = ttk.Entry(search_frame, width=30)
        self.word_entry.grid(row=0, column=0, padx=5)
        
        search_button = ttk.Button(search_frame, text="Search", command=self.search_word)
        search_button.grid(row=0, column=1, padx=5)
        
        # Result frame
        result_frame = ttk.Frame(root, padding="10")
        result_frame.grid(row=1, column=0, sticky="nsew")
        
        self.result_text = tk.Text(result_frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0)
        
        # Bind Enter key to search
        self.word_entry.bind('<Return>', lambda e: self.search_word())

    def search_word(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            return
            
        try:
            response = requests.get(f"{self.api_url}{word}")
            
            self.result_text.delete(1.0, tk.END)
            
            if response.status_code == 200:
                data = response.json()[0]
                # Debug print
                print("API response:", data)
                self.display_definition(data)
            else:
                self.result_text.insert(tk.END, "Word not found. Try another word?")
                
        except Exception as e:
            self.result_text.insert(tk.END, "An error occurred. Please try again.")

    def play_pronunciation(self, audio_url):
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
        # Frame to hold buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, pady=5)

        # Add buttons for available audio sources
        for phonetic in data.get('phonetics', []):
            if phonetic.get('audio'):
                audio_url = phonetic['audio']
                # Determine regional accent based on audio URL (UK or US)
                region = 'UK' if 'uk.mp3' in audio_url else 'US'
                # If audio URL is found, create a button to play pronunciation
                ttk.Button(
                    button_frame, 
                    text=f"Play {region} pronunciation",
                    command=lambda url=audio_url: self.play_pronunciation(url)
                ).pack(side='left', padx=5)

        # Display word and definitions
        word = data['word'] # Get word from API response
        phonetic = data.get('phonetic', '') # Get phonetic symbol from API response
        self.result_text.insert(tk.END, f"{word.capitalize()} {phonetic}\n\n")

        # Display etymology if available
        if 'origin' in data:
            self.result_text.insert(tk.END, f"Etymology: {data['origin']}\n\n") 
                               
        # Display meanings and definitions                             
        for i, meaning in enumerate(data['meanings'], 1):
            pos = meaning['partOfSpeech']
            definition = meaning['definitions'][0]['definition']
            
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