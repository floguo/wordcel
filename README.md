
# Wordcel - A GUI Dictionary Application

## Project Description
**Wordcel** is a Python-based graphical user interface (GUI) application designed to provide word definitions, pronunciations, and examples in an accessible and user-friendly manner. The app integrates with the [DictionaryAPI](https://dictionaryapi.dev/) to fetch real-time word data and uses the `pygame` library for audio playback of pronunciations.

This project demonstrates practical applications of Python's `tkinter` library for GUI design, alongside HTTP API integration and audio playback capabilities. The application includes features that enhance accessibility, making it inclusive for a diverse range of users.

---

## Running the Application

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wordcel
   ```
2. **Set up virtual environment:**
   ```bash
   python -m venv venv  # Create a new environment
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
   To ensure the virtual environment is activated, run `python` in the terminal. If it's activated, you should see `(venv)` in the prompt.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python src/main.py
   ```

---

## How to Use Wordcel

### Keybindings
- **Tab Navigation:** Use the `Tab` key to navigate across buttons and inputs.
- **Enter Key:** Press `Enter` on focused audio buttons to play pronunciations.
- **Alt + S:** Focus on the search input field for faster word lookup.

### Steps to Use
1. Type a word into the search bar.
2. Click **“Define word”** or press `Enter` to fetch the word’s data.
3. If audio pronunciations are available, click the appropriate button (e.g., **“Play US pronunciation”**) to listen.

---

## Recent Updates

### Accessibility Improvements
- Added keyboard navigation for all buttons.
- Enabled `Enter` key playback for focused audio buttons.
- Improved dynamic toggling for the **“Play Audio”** section, ensuring it’s only visible when applicable.

### Visual Enhancements
- Implemented indentation and Roman numeral sub-indexing for better organization.
- Simplified button hover and focus effects for a consistent experience.

---

## Example Output

### Input:
- User enters the word **“philosophy”** and clicks **“Define word.”**

### Output:
```plaintext
Philosophy /fəˈlɒsəfi/

1. Noun:
   i. The study of the fundamental nature of knowledge, reality, and existence, especially when considered as an academic discipline.
      Example: "He studied philosophy at university."

Play US Pronunciation | Play UK Pronunciation
```

Clicking a pronunciation button plays the corresponding audio.

---

## Future Enhancements

- **Synonyms & Antonyms:** Add related words for a richer vocabulary experience.
- **Word Etymology:** Provide historical origins of words.
- **Offline Mode:** Cache frequently searched words for use without an internet connection.

---

## Notes on Development

- The `requirements.txt` file ensures all dependencies are tracked for smooth setup.
- For development, ensure to update `requirements.txt` if new libraries are added:
  ```bash
  pip freeze > requirements.txt
  ```