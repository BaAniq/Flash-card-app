from tkinter import *
import pandas
from random import choice

card_words = {}

try:
    french_words = pandas.read_csv('data/left_to_learn.csv')
except FileNotFoundError:
    french_words = pandas.read_csv("data/french_words.csv")
french_english_dict = french_words.to_dict(orient='records')

def correct_word_in_french(card_words):
    global window_timer
    window.after_cancel(window_timer)
    canvas.itemconfig(card_image, image=photo_image_file_front)
    card_word_french = card_words['French']
    canvas.itemconfig(card_word, text=card_word_french)
    canvas.itemconfig(card_language, text='French')
    return card_word_french


def next_card():
    global window_timer, card_words
    window.after_cancel(window_timer)
    canvas.itemconfig(card_image, image=photo_image_file_back)
    card_words = choice(french_english_dict)
    card_word_english = card_words['English']
    canvas.itemconfig(card_word, text=card_word_english)
    canvas.itemconfig(card_language, text='English')
    window_timer = window.after(3000, correct_word_in_french, card_words)
    

def correct_answer():
    french_english_dict.remove(card_words)
    data = pandas.DataFrame(french_english_dict)
    data.to_csv('data/left_to_learn.csv', index=False)
    next_card()


BACKGROUND_COLOR = "#B1DDC6"


window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)
window_timer = window.after(3000, next_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
photo_image_file_back = PhotoImage(file='images/card_back.png')
photo_image_file_front = PhotoImage(file='images/card_front.png')
card_image = canvas.create_image(400, 263, image=photo_image_file_back, )
card_language = canvas.create_text(400, 150, text='Language', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='Word', font=('Ariel', 60, 'bold'))
canvas.grid(row=1, column=1, columnspan=2)

wrong_button_image = PhotoImage(file='images/wrong.png',)
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=2, column=1)

right_button_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_button_image, highlightthickness=0, command=correct_answer)
right_button.grid(row=2, column=2)

window.mainloop()
