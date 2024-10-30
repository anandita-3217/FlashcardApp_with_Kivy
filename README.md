# Flashcard Application
#### Video Demo: <https://youtu.be/TODGAKPxzUs>
#### Description:

The Flashcard Application is a comprehensive learning tool developed in Python using the Kivy framework. This application allows users to create, manage, and study with digital flashcards, offering an interactive and user-friendly interface for effective learning.

### Features

1. **Flashcard Management**
   - Create individual flashcards with questions and answers
   - Update existing flashcards
   - Delete specific flashcards or entire decks
   - View all flashcards in the deck
   - Track deck size with a maximum capacity of 150 cards

2. **Deck Operations**
   - Add multiple flashcards simultaneously
   - Upload flashcards from JSON files
   - View deck statistics
   - Clear entire deck with one click

3. **Quiz System**
   - Three difficulty levels:
     - Beginner (5 questions)
     - Mid (10 questions)
     - Pro (15 questions)
   - Time-limited quizzes (60 seconds)
   - Randomized question selection
   - Immediate feedback on answers
   - Score tracking

### Project Structure

The project consists of two main classes:

1. **FlashcardDeck Class**
   - Core functionality for flashcard management
   - Data structure: Dictionary (questions as keys, answers as values)
   - Methods for CRUD operations (Create, Read, Update, Delete)
   - Quiz logic implementation
   - JSON file handling for deck uploads

2. **FlashcardApp Class (GUI)**
   - Built with Kivy framework
   - User interface components:
     - Main menu with action buttons
     - Input forms for flashcard operations
     - Pop-up messages for user feedback
     - Scrollable view for large decks
     - Quiz interface with timer

### Technical Details

**Key Components:**
1. **Main Interface**
   - Vertical BoxLayout for organizing buttons
   - Clear navigation structure with back buttons
   - Consistent UI elements for user interaction

2. **Input Validation**
   - Checks for empty inputs
   - Validates question-answer pairs
   - Prevents duplicate questions
   - Enforces deck size limits

3. **Quiz Implementation**
   - Random sampling of questions
   - Answer comparison (case-insensitive)
   - Score calculation
   - Time limit enforcement

4. **File Operations**
   - JSON format support for deck uploads
   - Error handling for file operations
   - Format validation for imported data

### Design Choices

1. **Why Kivy?**
   - Cross-platform compatibility
   - Rich UI component library
   - Support for touch interfaces
   - Scalable application structure

2. **Dictionary Data Structure**
   - Fast lookup times for flashcard operations
   - Simple key-value mapping for questions and answers
   - Easy iteration for quiz implementation
   - Efficient memory usage

3. **Scrollable View Implementation**
   - Activated only for decks with more than 25 cards
   - Improves usability with large datasets
   - Maintains performance with growing deck size

4. **Quiz Difficulty Levels**
   - Accommodates different user skill levels
   - Progressive learning approach
   - Maintains engagement through varied challenge levels

### Future Improvements

Potential enhancements for future versions:
1. Data persistence across sessions
2. Multiple deck support
3. Custom quiz configurations
4. Statistics tracking
5. Export functionality
6. Study session scheduling

### How to Run

1. Ensure Python is installed on your system
2. Install required dependencies:
   ```
   pip install kivy
   ```
3. Run the application:
   ```
   python project.py
   ```

### Dependencies
- Python 3.x
- Kivy framework
- JSON (built-in)
- Random (built-in)
- Time (built-in)

This project was created as a final project for CS50's Introduction to Programming with Python. It demonstrates practical application of object-oriented programming, GUI development, file handling, and user interface design principles.

