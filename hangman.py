from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

root = Tk()
root.title('Hangman')
root.minsize(600,400)

root.resizable(0,0)

photos = ["./hangman_png/0.jpg","./hangman_png/1.jpg","./hangman_png/2.jpg","./hangman_png/3.jpg","./hangman_png/4.jpg","./hangman_png/5.jpg","./hangman_png/6.jpg"]

def taking_words_from_db():
    f = open("database.txt","r")
    dictionary = f.readlines()
    dictionary = [element.strip() for element in dictionary]
    f.close()
    return dictionary

def image_resize_and_deploy(num):
    image_open = Image.open(photos[num])
    resized_image = image_open.resize((300,200))
    img = ImageTk.PhotoImage(resized_image)
    hangman_image.config(image=img)
    hangman_image.image=img
    hangman_image.pack()


def correct_guess(letter):
    displayed_word = lblWord.get().split(" ")

    for i in range(len(displayed_word)):
        if displayed_word[i] == '' and displayed_word[i+1] == '':
            displayed_word[i] = ' '
    displayed_word=list(''.join(displayed_word))

    for i in enumerate(word):
        if i[1] == letter: 
            displayed_word[i[0]] = letter

    joined_word = " ".join(displayed_word)
    lblWord.set(joined_word)
    
    if "".join(displayed_word) == word:
        messagebox.showinfo("Win", "You won!\nStrat new game.")
        game_start()

def game_start():
    global number_of_mistakes
    global word
    global tried_letter

    tried_letter = []
    number_of_mistakes = 0
    
    dictionary = taking_words_from_db()
    number_of_words = len(dictionary)
    words = dictionary[random.randint(1,number_of_words-1)].upper().split(", ")
    
    help, word = words
    category_display.config(text=["Category:", help])
    wrong_letters.config(text="Wrong letters:")
    image_resize_and_deploy(number_of_mistakes)

    initial_word = list("_" * len(word))
    for i in enumerate(word):
        if i[1] == ' ':
            initial_word[i[0]] = ' '
    lblWord.set(" ".join(initial_word))

def user_inputs_check(event):
    global number_of_mistakes
    global tried_letter
    letter = user_typing.get().upper()
    
    if (letter <= 'Z' and letter >= 'A') and len(letter) == 1  and  letter not in tried_letter:
        if letter in word:
            correct_guess(letter)
        else:
            number_of_mistakes += 1
            tried_letter.append(letter)
            wrong_letters.config(text= " ".join(["Wrong letters:"," ".join(tried_letter)]))
            image_resize_and_deploy(number_of_mistakes)

        if number_of_mistakes == 6:
            messagebox.showwarning("You lose", "Game over")
            game_start()
    
    user_typing.delete(0,END)


category_display = Label(root, font=('Arial',20))
category_display.pack()

lblWord = StringVar()
word_display_underscores = Label(root,textvariable=lblWord, font=('Arial',20))
word_display_underscores.pack()

wrong_letters = Label(root, font=('Arial',20))
wrong_letters.pack()

user_typing = Entry(root,font=('Arial',18))
user_typing.bind('<KeyRelease>',user_inputs_check)
user_typing.pack()

hangman_image = Label(root)
hangman_image.pack()

new_game_button = Button(root, command = lambda : game_start(), text="New Game")
new_game_button.pack()

game_start()

root.mainloop() 