
# Wordcel - A GUI Dictionary Application

## Project Description
**Wordcel** is a Python-based graphical user interface (GUI) application designed to provide word definitions, pronunciations, and examples in an accessible and user-friendly manner. The app integrates with the [DictionaryAPI](https://dictionaryapi.dev/) to fetch real-time word data and uses the `pygame` library for audio playback of pronunciations.

This project demonstrates practical applications of Python's `tkinter` library for GUI design, alongside HTTP API integration and audio playback capabilities. The application includes features that enhance accessibility, making it inclusive for a diverse range of users.

---

## Running the Program

### Requirements

Ensure the following dependencies are installed:

- Python 3.8+
- `requests` (for HTTP API calls)
- `pygame` (for audio playback)

Install the required libraries by running:

```bash
pip install requests pygame
```

### Execution Steps

1. **Download the file:**
   Save the Python file (`main.py`) on your local machine.

2. **Run the program:**
   Open a terminal or command prompt, navigate to the folder containing the file, and execute the following command:

   ```bash
   python main.py
   ```

3. **Use the application:**
   - Enter a word in the text box.
   - Click the "Define" button or press `Enter` to fetch the definition.
   - Play pronunciation audio by clicking the respective button (e.g., "Play US pronunciation").

---

## Features

1. **Search Functionality:**
   - Enter a word to fetch its definition, part of speech, and examples.
   - The program handles errors gracefully, showing a message if the word is not found.

2. **Pronunciation Audio:**
   - Pronunciation buttons allow users to hear the correct pronunciation in different accents (e.g., US, UK).

3. **Accessible User Interface:**
   - Simple, intuitive layout designed with `tkinter` for ease of use.
   - Clear typography and layout suitable for a broad audience.

---

## Socio-Cultural Considerations

### Accessibility
- The app uses `ttk` for a modern, visually accessible interface.
- Text fields and buttons are positioned for ease of navigation and interaction.

### Cultural Inclusivity
- Regional pronunciation (US, UK) provides linguistic flexibility for users from different backgrounds.

### Customization for Users with Disabilities
- The program’s layout supports keyboard navigation (e.g., pressing `Enter` triggers a search).
- Future iterations could include text-to-speech output for visually impaired users.

---

## Example of Running the Program

### Input
- User enters the word "philosophy" in the search bar and clicks "Define."

### Output
The application displays:
```
Philosophy /fəˈlɒsəfi/

1. noun
Definition: The study of the fundamental nature of knowledge, reality, and existence, especially when considered as an academic discipline.
Example: "He studied philosophy at university."

Play US pronunciation | Play UK pronunciation
```
Clicking the pronunciation button plays the audio.

---

## Future Improvements

The following features can be added to enhance the application:

- **Synonyms and Antonyms:** Provide related words to enrich vocabulary.
- **Etymology:** Display the origin and historical development of words.
- **Related Words:** Suggest similar or associated terms.

---

## Authors
**Flora (Flo) Guo**
