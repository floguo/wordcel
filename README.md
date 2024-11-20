# Wordcel

> Etymology made easy

Flora Guo  
Faculty of Information  
Bachelor of Information  
INF452: Information Design Studio V: Coding  
Fall 2024

## About
Wordcel is a desktop app that helps you explore word origins and etymology in a simple, clean interface. No more clicking through sketchy websites or trying to parse confusing dictionary entries - just type in a word and get its story.

### Features
- Quick etymology lookups
- Word origin tracing
- Historical word forms
- Clean, minimalist interface that's easy on the eyes
- Built-in pronunciation guide

### Built With
- Python 3.8+
- Tkinter for the UI
- Free Dictionary API for etymology data

## Getting Started

### Prerequisites
- Python 3.8 or newer
- Some basic command line knowledge
- Internet connection

### Installation
1. Install required packages:
```bash
pip install requests tkinter
```

2. Run the app:
```bash
python src/main.py
```

## Design Choices

### Accessibility First
- High contrast mode available
- Adjustable text size
- Keyboard navigation friendly
- Clear, readable fonts
- Simple, intuitive layout

### User Experience
- Clean, distraction-free interface
- Quick response times
- Helpful error messages when things go wrong
- No unnecessary clicks or menus to navigate

## Project Structure
```
wordcel/
├── src/
│   ├── api/
│   │   └── etymology_service.py
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── search_frame.py
│   │   ├── result_frame.py
│   │   └── styles.py
│   └── main.py
└── README.md
```

## Known Limitations
- English words only (for now)
- Needs internet to work
- Some really obscure words might not have data

## What's Next
- More languages
- Offline mode
- Pretty word evolution trees
- "Word of the day" feature
- Dark mode (because why not)

---

*Note: Example screenshots and detailed usage guide coming soon!*