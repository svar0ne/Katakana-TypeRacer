import tkinter as tk
import random
import time

class Game():
    def __init__(self):
        self.kana_list = [
        ("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")
        ]
        self.attempts = 0
        self.wrong = []

    def restart(self):
        for x in root.winfo_children():
            x.destroy()
        self.menu()

    def menu(self):
        self.kana_label = tk.Label(root, text="")
        self.kana_label.pack()
        
        self.feedback = tk.Label(root, text="")
        self.feedback.pack()

        self.start_button = tk.Button(root, text="start game", command=self.game_start)
        self.start_button.pack()

    def game_start(self, event=None):
        self.start_button.destroy()
        self.kana_list_copy = self.kana_list.copy()
        self.start = time.time()

        self.entry = tk.Entry(root)
        self.entry.pack()
        self.entry.focus()
        self.entry.bind("<Return>", self.check_answer)
        self.kana_get()

    def kana_get(self):
        if self.kana_list_copy != []:
            self.random_tuple = random.choice(self.kana_list_copy)
            self.kana, self.romaji = self.random_tuple
            self.kana_label.config(text=self.kana)
        else:
            self.feedback.config(text="DONE")
            self.end = time.time()
            total_time = round(self.end - self.start, 2)
            per_kana = round(total_time / len(self.kana_list), 2)
            wrong_count = len(self.wrong)

            stats = {
                "total_time":    f"Total time:    {total_time} sec",
                "per_kana":        f"Time per kana: {per_kana} sec",
                "wrong_count":   f"You got: {wrong_count} kana wrong",
            }
            stats_string = "\n".join(stats.values())

            self.end_stats = tk.Label(root, text=stats_string, font=("courier", 8))
            self.end_stats.pack()

            self.back_to_menu = tk.Button(root, text="start menu", command=self.restart)
            self.back_to_menu.pack()
        
    def check_answer(self, event=None):
        answer = self.entry.get()

        if answer == self.romaji:
            self.attempts = 0
            self.feedback.config(text="RIGHT")
            self.kana_list_copy.remove(self.random_tuple)
            self.entry.delete(0, tk.END)
            self.kana_get()
        elif answer == "":
            pass
        else:
            self.attempts +=1
            if self.romaji not in self.wrong:
                self.wrong.append(self.kana)
            if self.attempts == 3:
                self.feedback.config(text=f"WRONG\nanswer: {self.romaji}")
            else:
                self.feedback.config(text="WRONG")
            self.entry.delete(0, tk.END)
                



root = tk.Tk()
root.geometry("350x450")

game = Game()
game.menu()

root.mainloop()
