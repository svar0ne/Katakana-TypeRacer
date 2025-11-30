import tkinter as tk
import random

class Game():
    def __init__(self):
        self.kk_list = [
        ("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")
        ]

    def menu(self, event=None):
        self.kk_label = tk.Label(root, text="")
        self.kk_label.pack()

        self.feedback = tk.Label(root, text="")
        self.feedback.pack()

        self.start_button = tk.Button(root, text="start game", command=self.game_start)
        self.start_button.pack()

    def game_start(self, event=None):
        self.kk_list_copy = self.kk_list.copy()
        self.start_button.destroy()
        
        self.entry = tk.Entry(root)
        self.entry.pack()
        self.entry.focus()
        self.entry.bind("<Return>", self.check_answer)
        self.kana_get()

    def kana_get(self):
        if self.kk_list_copy != []:
            self.random_tuple = random.choice(self.kk_list_copy)
            self.kk, self.romaji = self.random_tuple
            self.kk_label.config(text=self.kk)
        else:
            self.feedback.config(text="over")
        
    def check_answer(self, event=None):
        answer = self.entry.get()
        if answer == self.romaji:
            self.feedback.config(text="RIGHT")
            self.kk_list_copy.remove(self.random_tuple)
            self.entry.delete(0, tk.END)
            self.kana_get()
        else:
            self.feedback.config(text="WRONG")
            self.entry.delete(0, tk.END)



root = tk.Tk()
root.geometry("350x450")

game = Game()
game.menu()

root.mainloop()
