from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
list_of_words = []

try:
    learn_data = pd.read_csv("./data/word_to_learn.csv")
except FileNotFoundError:
    # when file not found error will happen this block will execute
    # reading data from csv
    data = pd.read_csv("./data/french_words.csv")
    # converting a dataframe as a list of records
    list_of_words = data.to_dict(orient='records')


else:
    # if file found than load the data from word_to_learn csv
    list_of_words = learn_data.to_dict(orient='records')


def next_card():
    """this func will show the next card"""
    global current_card, flip_timer
    # cancel the time when showing the next card
    window.after_cancel(flip_timer)

    # will choose a random word from list of words and save it as a current card
    current_card = choice(list_of_words)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_words, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_image)

    # calling flip_card func after 3 sec
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """this func will flip the current card after 3 sec"""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_words, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_img)


def is_known():
    # remove the card from the list of cards after clicking right button
    list_of_words.remove(current_card)
    # will make a csv from the updated list
    df_words = pd.DataFrame(list_of_words)
    df_words.to_csv('./data/word_to_learn.csv', index=False)
    next_card()


# ------------UI-----------#
window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# canvas creation
canvas = Canvas(width=800, height=526, highlightthickness=0)

# setting background image of canvas
front_image = PhotoImage(file="./images/card_front.png")
# next background image
back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)

# changing background color of canvas
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

# text over canvas
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_words = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# check button
right_img = PhotoImage(file="./images/right.png")
correct_btn = Button(image=right_img, highlightthickness=0, command=is_known)
correct_btn.grid(column=1, row=1)

# cross button
wrong_img = PhotoImage(file="./images/wrong.png")
cross_btn = Button(image=wrong_img, highlightthickness=0, command=next_card)
cross_btn.grid(column=0, row=1)

flip_timer = window.after(3000, flip_card)

next_card()

window.mainloop()
