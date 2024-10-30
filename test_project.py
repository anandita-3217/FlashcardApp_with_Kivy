from pytest_mock import mocker
from project import FlashcardDeck
import pytest

@pytest.fixture()
def deck():
    return FlashcardDeck()

# tests add_flashcard

def test_add_flashcard(deck):
    result_valid = deck.add_flashcard("What is 2 + 2?", "4")
    assert result_valid == "Flashcard What is 2 + 2? added"
    assert deck.card_count == 1

    result_noflashcards = deck.add_flashcard("","")
    assert result_noflashcards == "No question or answer entered"
    
    result_invalid_flashcards = deck.add_flashcard(" "," ")
    assert result_invalid_flashcards == "Invalid question and answer pairing"
    

# tests update_flashcard
def test_update_flashcard(deck):
    deck.add_flashcard("What is the capital of France?", "Paris") 
    result_valid = deck.update_flashcard("What is the capital of France?", "Lyon")
    assert result_valid == "Flashcard 'What is the capital of France?' updated!"
    assert deck.deck["What is the capital of France?"] == "Lyon"

    result_noexist = deck.update_flashcard("What is the capital of Spain?", "Madrid")
    assert result_noexist == "Flashcard 'What is the capital of Spain?' does not exist"


def test_delete_flashcard(deck):
    deck.add_flashcard("What is the capital of France?", "Paris") 
    result_valid = deck.delete_card("What is the capital of France?")
    assert result_valid == "Flashcard 'What is the capital of France?' deleted"
    assert deck.card_count == 0

    result_noexist = deck.delete_card("What is the capital of India?")
    assert result_noexist == "Flashcard 'What is the capital of India?' not found in deck"

    result_invalid0 = deck.delete_card("")
    assert result_invalid0 == "Invalid question format"

    result_invalid1 = deck.delete_card(" ")
    assert result_invalid1 == "Invalid question format"

def test_delete_deck(deck):
    deck.add_flashcard("What is the capital of France?", "Paris") 
    deck.add_flashcard("What is 2+2?", "4")

    result = deck.delete_deck()
    assert result == "Deck deleted!"
    assert deck.card_count == 0

def test_delete_deck_invalid(deck):
    result = deck.delete_deck()
    assert result == "Deck empty!"

def test_deck_size(deck):
    assert deck.deck_size() == 0
    deck.add_flashcard("What is the capital of France?", "Paris") 
    deck.add_flashcard("What is 2+2?", "4")
    assert deck.deck_size() == 2

def test_view_deck(deck):

    result = deck.view_deck()
    assert result == "No cards to show"

    deck.add_flashcard("What is the capital of France?", "Paris") 
    result_valid = deck.view_deck()
    assert result_valid == "Q: What is the capital of France? - A: Paris"

def test_quiz_beginner(deck):
    
    result_invalid = deck.quiz('beginner')
    assert result_invalid == "error: Not enough flashcards for beginner level quiz."

    deck.add_flashcard("What is 2+2?", "4")
    deck.add_flashcard("What is the capital of France?", "Paris")
    deck.add_flashcard("What is the square root of 16?", "4")
    deck.add_flashcard("Who wrote '1984'?", "George Orwell")
    deck.add_flashcard("What is the capital of Spain?", "Madrid")
    
    quiz = deck.quiz('beginner', shuffle=False)
    assert len(quiz['questions']) == 5

def test_quiz_pro_level(deck):
    
    for i in range(1, 16):
        deck.add_flashcard(f"Question {i}", f"Answer {i}")
        
    quiz = deck.quiz('pro', shuffle=False)
    assert len(quiz['questions']) == 15

def test_check_answer(deck):
    
    questions = [
        ("What is 2+2?", "4"),
        ("What is the capital of France?", "Paris")
    ]
    
    result_correct = deck.check_answer(0, "4", questions)
    assert result_correct is True

    result_incorrect = deck.check_answer(1, "London", questions)
    assert result_incorrect is False

def test_upload_deck(deck,mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data='{"Q1": "A1", "Q2": "A2"}'))
    mock_json_load = mocker.patch("json.load", return_value={"Q1": "A1", "Q2": "A2"})
    
    
    result = deck.upload_deck("mocked_file.json")
    
    assert result == "Deck added!"
    assert deck.card_count == 2
 
def test_add_deck_valid(deck):
    new_flashcards ={    "What is 2 + 2?": "4",
    "What is the capital of France?": "Paris",
    "What is the largest planet?": "Jupiter"
    }
    result_valid = deck.add_deck(new_flashcards)
    assert result_valid ==  "Deck added!"
    assert deck.card_count == 3


