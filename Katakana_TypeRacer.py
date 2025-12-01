import tkinter as tk
from tkinter import messagebox
import random
import time
import json
from katakana_list import *

class Game():
    def __init__(self):
        self.kana_list = katakana_list
        self.root = tk.Tk()
        self.root.geometry("350x450")
        self.menu()
        self.root.mainloop()

    def menu(self):
        for x in self.root.winfo_children():
            x.destroy()
    
        self.title = tk.Label(self.root, text="Katakana TypeRacer",)
        self.title.pack()

        self.start_button = tk.Button(self.root, text="start game", command=self.game_start)
        self.start_button.pack()

        self.stats_button = tk.Button(self.root, text="stats", command=self.stats_page)
        self.stats_button.pack()

    def stats_page(self):
        for x in self.root.winfo_children():
            x.destroy()

        try:
            with open("stats.json", "r") as s:
                json_stats = json.load(s)
        except FileNotFoundError:
            json_stats = {"tpk": [0.0, 0.0]}

        tpk_data = (json_stats["tpk"])
        best_tpk = min(tpk_data)
        avg_tpk = round(sum(tpk_data) / len(tpk_data), 2)
        last_tpk = tpk_data[-1]

        self.stats_title = tk.Label(self.root, text="time per katakana: ", font=("", 12))
        self.stats_title.pack()

        self.stat1 = tk.Label(self.root, text=f"average: {avg_tpk} sec", font=("courier", 9))
        self.stat1.pack()

        self.stat2 = tk.Label(self.root, text=f"best:    {best_tpk} sec", font=("courier", 9))
        self.stat2.pack()

        self.stat3 = tk.Label(self.root, text=f"last:    {last_tpk} sec", font=("courier", 9))
        self.stat3.pack()

        self.back_button = tk.Button(self.root, text="back", command=self.menu)
        self.back_button.pack()

    def game_start(self):
        for x in self.root.winfo_children():
            x.destroy()

        self.kana_list_copy = self.kana_list.copy()
        self.wrong = {}
        self.attempts = 0
        self.start = time.time()
        
        self.kana_label = tk.Label(self.root, text="")
        self.kana_label.pack()
        
        self.feedback = tk.Label(self.root, text="")
        self.feedback.pack()

        self.entry = tk.Entry(self.root)
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
            self.entry.config(state="disabled")
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
            stats_str = "\n".join(stats.values())

            self.end_stats = tk.Label(self.root, text=stats_str, font=("courier", 9))
            self.end_stats.pack()

            def more_info():
                wrong_str = ""
                for x, y in self.wrong.items():
                    wrong_str += f"{x}={y}    "
                messagebox.showinfo(f"wrong kana", f"you got the following katakana wrong:\n\n{wrong_str}")

            if wrong_count >0:
                self.more = tk.Button(self.root, text="show more", command=more_info)
                self.more.pack()           

            try:   
                with open("stats.json", "r") as s:
                    json_stats = json.load(s)
            except FileNotFoundError:
                json_stats = {"tpk": []}
            
            json_stats["tpk"].append(per_kana)
            with open("stats.json", "w") as s:
                json.dump(json_stats, s, indent=4)
   
            self.back_to_menu = tk.Button(self.root, text="start menu", command=self.menu)
            self.back_to_menu.pack()
        
    def check_answer(self, event=None):
        answer = self.entry.get().strip()

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
            if self.kana not in self.wrong.keys():
                self.wrong[self.kana] = self.romaji
            if self.attempts >= 3:
                self.feedback.config(text=f"WRONG\nanswer: {self.romaji}")
            else:
                self.feedback.config(text="WRONG")
            self.entry.delete(0, tk.END)
                
player = Game()



