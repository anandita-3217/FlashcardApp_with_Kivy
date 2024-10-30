import random
import time
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

    # Class for flashcards and their managemanet
class FlashcardDeck:

    MAX_DECK_SIZE = 150

   # initalize flashcard deck as a dictionary - flash cards thhemselves as key,value pairs
    def __init__(self):
        self.deck = {}

     # will be called when viewing the cards.   
    def __str__(self):
        if not self.deck:
            return "No cards to show"
        return "\n".join([f"Q: {question} - A: {answer}" for question, answer in self.deck.items()])
    

    @property
    def card_count(self):
        return len(self.deck)

    # Helper functions

    def _is_deck_full(self):
        return len(self.deck) > FlashcardDeck.MAX_DECK_SIZE
    

    def _flashcard_exists(self,question):
        return question in self.deck
    

    def _handle_existing_flashcard(self,question):
        return f"Flashcard with question '{question}' already exists."
        
    

    # Main functions 

    def update_flashcard(self,question,new_answer):
        if self._flashcard_exists(question):
            if (question.isspace() or new_answer.isspace()): 
                return "Invalid question and answer pairing"
            self.deck[question] = new_answer
            return f"Flashcard '{question}' updated!"
        else:
            return f"Flashcard '{question}' does not exist"
                

    # will add a single card
    def add_flashcard(self,question,answer):
        if self._flashcard_exists(question):
            return self._handle_existing_flashcard(question)
        if self._is_deck_full():
            return "Deck size reached"
        if (question.isspace() or answer.isspace()): 
            return "Invalid question and answer pairing"
        if  (question == "" or answer == ""): 
            return "No question or answer entered"
        self.deck[question] = answer
        return f"Flashcard {question} added"
    

    # will add an entire deck
    def add_deck(self,new_flashcards):
        
        for question, answer in new_flashcards.items():
            if self._flashcard_exists(question):
                self._handle_existing_flashcard(question)
            else:
                if self._is_deck_full():
                    return f"Deck size cannot exceed {FlashcardDeck.MAX_DECK_SIZE} flashcards."
                self.deck[question] = answer
        return "Deck added!"
    
   

    


    # upload a .json file containing the cards
    def upload_deck(self, filepath):
        try:
            with open(filepath, 'r') as file:
                new_flashcards = json.load(file)
                return self.add_deck(new_flashcards)
        except FileNotFoundError:
            return "File not found. Please check the file path and try again."
        except json.JSONDecodeError:
            return "Invalid JSON format. Please check the file content."

    # deletes card by question
    def delete_card(self,question):
        if question in self.deck:
            del self.deck[question]
            return f"Flashcard '{question}' deleted"
        if question.isspace() or question == "":
            return "Invalid question format"
        else:
            return f"Flashcard '{question}' not found in deck"
    
    
    # delete an entire deck
    def delete_deck(self):
        if self.card_count == 0:
            return "Deck empty!"
        self.deck.clear()
        return "Deck deleted!"
    
    # Size of deck
    def deck_size(self):
        return len(self.deck) 


    # Prints all flashcards in the deck
    def view_deck(self):
        return str(self)
    
    
    # returns the quiz details as a dictionary on what questions to display

    def quiz(self, level, shuffle=True):
        time_limit = 60
        
        if level == 'beginner' and self.card_count < 5:
            return f"error: Not enough flashcards for {level} level quiz."
        elif level == 'mid' and self.card_count < 10:
            return f"error: Not enough flashcards for {level} level quiz."
        elif level == 'pro' and self.card_count < 15:
            return f"error: Not enough flashcards for {level} level quiz."

        
        num_questions = 5 if level == 'beginner' else 10 if level == 'mid' else 15
        questions = list(self.deck.items())  # Get all flashcards

        # Shuffle the questions for user  and dont for the tests 
        if shuffle:
            questions = random.sample(questions, num_questions)
        else:
            questions = questions[:num_questions] 

        return {
            "questions": questions,
            "time_limit": time_limit
        }
    
    # Returns a boolean value if true if the user_answer is correct else false
    def check_answer(self, current_question_index, user_answer, questions):
        _, correct_answer = questions[current_question_index]
        is_correct = user_answer.lower() == correct_answer.lower()
        return is_correct




 
#  GUI part

class FlashcardApp(App):
    def build(self):
        self.deck = FlashcardDeck()
        self.main_layout = BoxLayout(orientation="vertical", padding=10)

        # define buttons 
        self.add_button = Button(text="Add Flashcard", on_press=self.show_add_flashcard)
        self.update_button = Button(text="Update Flashcard", on_press=self.show_update_flashcard)
        self.delete_button = Button(text="Delete Flashcard", on_press=self.show_delete_flashcard)
        self.delete_deck_button = Button(text="Delete Deck", on_press=self.delete_deck)
        self.view_button = Button(text="View Deck", on_press=self.view_deck)
        self.add_deck_button = Button(text="Add Deck", on_press=self.show_add_deck)
        self.upload_button = Button(text="Upload Deck (from JSON)", on_press=self.show_upload_deck)
        self.quiz_button = Button(text="Take Quiz", on_press=self.quiz)
        self.deck_size_button = Button(text="View Deck Size", on_press=self.view_deck_size)
        self.exit_button = Button(text="Exit", on_press=self.exit_app)

        # add buttons 
        self.main_layout.add_widget(self.add_button)
        self.main_layout.add_widget(self.add_deck_button)
        self.main_layout.add_widget(self.upload_button)
        self.main_layout.add_widget(self.view_button)
        self.main_layout.add_widget(self.deck_size_button)
        self.main_layout.add_widget(self.update_button)
        self.main_layout.add_widget(self.delete_button)
        self.main_layout.add_widget(self.delete_deck_button)
        self.main_layout.add_widget(self.quiz_button)
        self.main_layout.add_widget(self.exit_button)

        return self.main_layout

    # helper funtions
    def clear_layout(self):
        self.main_layout.clear_widgets()

    def reset_layout(self, *args):
        self.clear_layout()
        self.main_layout.add_widget(self.add_button)
        self.main_layout.add_widget(self.add_deck_button)
        self.main_layout.add_widget(self.upload_button)
        self.main_layout.add_widget(self.view_button)
        self.main_layout.add_widget(self.deck_size_button)
        self.main_layout.add_widget(self.update_button)
        self.main_layout.add_widget(self.delete_button)
        self.main_layout.add_widget(self.delete_deck_button)
        self.main_layout.add_widget(self.quiz_button)
        self.main_layout.add_widget(self.exit_button)






    # Show functions
    def show_add_flashcard(self, instance):
        self.clear_layout()

        self.question_input = TextInput(hint_text="Enter the question", multiline=False)
        self.answer_input = TextInput(hint_text="Enter the answer", multiline=False)
        self.main_layout.add_widget(self.question_input)
        self.main_layout.add_widget(self.answer_input)

        add_button = Button(text="Submit Flashcard", on_press=self.add_flashcard)
        self.main_layout.add_widget(add_button)

        back_button = Button(text="Back", on_press=self.reset_layout)
        self.main_layout.add_widget(back_button)

    def show_update_flashcard(self, instance):
        self.clear_layout()

        self.question_input = TextInput(hint_text="Enter the question to update", multiline=False)
        self.answer_input = TextInput(hint_text="Enter the new answer", multiline=False)
        self.main_layout.add_widget(self.question_input)
        self.main_layout.add_widget(self.answer_input)

        update_button = Button(text="Update Flashcard", on_press=self.update_flashcard)
        self.main_layout.add_widget(update_button)

        back_button = Button(text="Back", on_press=self.reset_layout)
        self.main_layout.add_widget(back_button)

    def show_delete_flashcard(self, instance):
        self.clear_layout()

        self.question_input = TextInput(hint_text="Enter the question to delete", multiline=False)
        self.main_layout.add_widget(self.question_input)

        delete_button = Button(text="Delete Flashcard", on_press=self.delete_flashcard)
        self.main_layout.add_widget(delete_button)

        back_button = Button(text="Back", on_press=self.reset_layout)
        self.main_layout.add_widget(back_button)

    def show_add_deck(self, instance):
        self.clear_layout()

        self.add_deck_input = TextInput(hint_text="Enter flashcards in format Q: A (each flashcard on a new line)", multiline=True)
        self.main_layout.add_widget(self.add_deck_input)

        add_deck_button = Button(text="Submit Deck", on_press=self.add_deck)
        self.main_layout.add_widget(add_deck_button)

        back_button = Button(text="Back", on_press=self.reset_layout)
        self.main_layout.add_widget(back_button)

    def show_upload_deck(self, instance):
        self.clear_layout()  # Clear the layout to show the new UI components

        self.filepath_input = TextInput(hint_text="Enter the JSON file path", multiline=False)
        self.main_layout.add_widget(self.filepath_input)

        upload_button = Button(text="Upload Deck", on_press=self.upload_deck)
        self.main_layout.add_widget(upload_button)

        back_button = Button(text="Back", on_press=self.reset_layout)
        self.main_layout.add_widget(back_button)
    
    def show_popup(self, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        message_label = Label(text=message)
        dismiss_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(message_label)
        popup_layout.add_widget(dismiss_button)

        popup = Popup(title="Message", content=popup_layout, size_hint=(0.75, 0.5))
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()




   

    # Do funtions
    def add_flashcard(self, instance):
        question = self.question_input.text
        answer = self.answer_input.text
        if question and answer:
            result = self.deck.add_flashcard(question, answer)
            self.show_popup(result)
            self.question_input.text = ""
            self.answer_input.text = ""
        else:
            result = self.deck.add_flashcard(question,answer)
            self.show_popup(result)
            return

        # add_deck GUI
    def add_deck(self, instance):
        deck_data = self.add_deck_input.text.strip()
        if not deck_data:
            self.show_popup("No flashcards entered.")
            return


       
        new_flashcards = {}
        for line in deck_data.split("\n"):
            try:
                question, answer = line.split(":")
                new_flashcards[question.strip()] = answer.strip()
                if question == "":
                    self.show_popup("Invalid")
                    return
            except ValueError:
                self.show_popup("Invalid format. Use 'question: answer' on each line.")
                return

        
        result = self.deck.add_deck(new_flashcards)
        self.show_popup(result)

        
        self.add_deck_input.text = ""


        # update_flashcard gui 
    def update_flashcard(self, instance):
        question = self.question_input.text
        new_answer = self.answer_input.text
        if question and new_answer:
            result = self.deck.update_flashcard(question, new_answer)
            self.show_popup(result)
            self.question_input.text = ""
            self.answer_input.text = ""
        
        else:
            result = self.deck.update_flashcard(question,new_answer)
            self.show_popup(result)
            return
        # delete_flashcard GUI
    def delete_flashcard(self, instance):
        question = self.question_input.text
        if question:
            result = self.deck.delete_card(question)
            self.show_popup(result)
            self.question_input.text = ""
                
        else:
            result = self.deck.delete_card(question)
            self.show_popup(result)
            return
        # delete_deck GUI
    def delete_deck(self, instance):
        result = self.deck.delete_deck()
        self.show_popup(result)

   # scroll enabled only if more than 25 cards to be displayed
    def view_deck(self,instance):
        deck_content = self.deck.view_deck()
        num_flashcards = self.deck.card_count
        

        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        
        if num_flashcards > 25:
            scroll_view = ScrollView(size_hint=(1, None), size=(Window.width * 0.9, Window.height * 0.6))

            
            deck_label = Label(text=deck_content, size_hint_y=None)
            deck_label.bind(texture_size=deck_label.setter('size'))
            scroll_view.add_widget(deck_label)  
            layout.add_widget(scroll_view)



        else:
         
            deck_label = Label(text=deck_content)
            layout.add_widget(deck_label)

        
        close_button = Button(text="Close")
        close_button.bind(on_press=lambda instance: popup.dismiss())  
        layout.add_widget(close_button)

        
        popup = Popup(title="View Deck", content=layout, size_hint=(0.9, 0.9))
        popup.open()



    def upload_deck(self, instance):
        filepath = self.filepath_input.text
        if filepath:
            result = self.deck.upload_deck(filepath)  
            if "Deck added!" in result:
                self.show_popup(f"Deck loaded successfully from {filepath}\n \n Added cards: {self.deck.card_count}")
            else:
                self.show_popup(f"Error: {result}")  
        else:
            self.show_popup("Error: No file path provided.")
        self.reset_layout(instance)  
    

    

    def view_deck_size(self, instance):
        size = self.deck.deck_size()
        self.show_popup(f"Deck size: {size}")

    def exit_app(self, instance):
        self.stop()
    def quiz(self, instance):
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        beginner_button = Button(text="Beginner", size_hint=(1, 0.2))
        mid_button = Button(text="Mid", size_hint=(1, 0.2))
        pro_button = Button(text="Pro", size_hint=(1, 0.2))

        layout.add_widget(beginner_button)
        layout.add_widget(mid_button)
        layout.add_widget(pro_button)

        quiz_popup = Popup(title="Choose Quiz Level", content=layout, size_hint=(0.75, 0.5))

        
        beginner_button.bind(on_press=lambda instance: self.start_quiz('beginner', quiz_popup))
        mid_button.bind(on_press=lambda instance: self.start_quiz('mid', quiz_popup))
        pro_button.bind(on_press=lambda instance: self.start_quiz('pro', quiz_popup))

        quiz_popup.open()

    def start_quiz(self, level, quiz_popup):
        quiz_popup.dismiss()

        result = self.deck.quiz(level)

       
        if isinstance(result, dict) and "error" in result:
            self.show_popup(result["error"])
        elif isinstance(result, str):
            self.show_popup(result)
        else:
           
            self.questions = result.get("questions", [])
            self.time_limit = result.get("time_limit", 0)
            self.num_questions = len(self.questions)

            self.score = 0
            self.current_question = 0
            self.start_time = time.time()

            self.show_quiz()


    def show_quiz(self):
        if self.current_question >= self.num_questions or (time.time() - self.start_time > self.time_limit):
            self.show_popup(f"Quiz completed! Your score: {self.score}/{self.num_questions}")
            return

        question, _ = self.questions[self.current_question]
        layout = BoxLayout(orientation='vertical')
        question_label = Label(text=f"Question {self.current_question + 1}: {question}")

        self.answer_input = TextInput(hint_text="Enter your answer", multiline=False)
        submit_button = Button(text="Submit Answer", size_hint=(1, 0.2))

        submit_button.bind(on_press=self.submit_answer)

        layout.add_widget(question_label)
        layout.add_widget(self.answer_input)
        layout.add_widget(submit_button)

        self.quiz_popup = Popup(title=f"Quiz - Question {self.current_question + 1}",
                                content=layout, size_hint=(0.75, 0.5))
        self.quiz_popup.open()

    def submit_answer(self, instance):
        user_answer = self.answer_input.text
        is_correct = self.deck.check_answer(self.current_question, user_answer, self.questions)

        if is_correct:
            self.score += 1

        self.current_question += 1
        self.quiz_popup.dismiss()
        self.show_quiz()
        
def main():
    FlashcardApp().run()


if __name__ == "__main__":
    main()

