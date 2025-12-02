import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import os
from katakana_list import *

class Game():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("350x350")
        self.root.config(bg=bgc)

        self.menu()
        self.root.mainloop()

    def menu(self):
        for x in self.root.winfo_children():
            x.destroy()
    
        self.title = tk.Label(self.root, text="Katakana TypeRacer", bg=bgc, fg=txtc, font=("", 20, "bold"))
        self.title.pack(pady=(20, 0))

        self.shortcut = tk.Label(self.root, text="enter = start game", bg=bgc, fg=txtc, font=("", 10))
        self.shortcut.pack()
        self.shortcut.focus()
        self.shortcut.bind("<Return>", self.game_start)


        self.start_button = tk.Button(self.root, text="start game", command=self.game_start, font=("", 10, "bold"))
        self.start_button.pack(pady=(25, 12))

        self.stats_button = tk.Button(self.root, text="stats", command=self.stats_page, font=("", 10, "bold"))
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

        self.stats_title = tk.Label(self.root, text="time per katakana: ", bg=bgc, fg=txtc, font=("", 13, "bold"))
        self.stats_title.pack(pady=(20, 5))

        self.stat1 = tk.Label(self.root, text=f"average: {avg_tpk} sec", bg=bgc, fg=txtc, font=("courier", 9))
        self.stat1.pack()

        self.stat2 = tk.Label(self.root, text=f"best:    {best_tpk} sec", bg=bgc, fg=txtc, font=("courier", 9))
        self.stat2.pack()

        self.stat3 = tk.Label(self.root, text=f"latest:  {last_tpk} sec", bg=bgc, fg=txtc, font=("courier", 9))
        self.stat3.pack()

        def confirm():
            choice = messagebox.askyesno(title="warning", message="this will permanently erase your data\n\n\tare you sure?")
            if choice == True:
                if os.path.exists("stats.json"):
                    os.remove("stats.json")
                    self.stats_page()
                else:
                    pass
            else:
                pass
        self.reset = tk.Button(self.root, text="reset", command=confirm, font=("", 10, "bold"))
        self.reset.pack(pady=(13, 0), padx=(0, 70))

        self.back_button = tk.Button(self.root, text="back", command=self.menu, font=("", 10, "bold"))
        self.back_button.pack()
        self.back_button.place(y=126, x=190)

    def game_start(self, event=None):
        for x in self.root.winfo_children():
            x.destroy()

        self.kana_list_copy = katakana_list.copy()
        self.wrong = {}
        self.attempts = 0
        self.start = time.time()
        
        self.kana_label = tk.Label(self.root, text="", bg=bgc, fg=txtc, font=("", 30, "bold"))
        self.kana_label.pack(pady=(20, 0))
        
        self.feedback = tk.Label(self.root, text="", bg=bgc, fg=txtc, font=("", 15))
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
            per_kana = round(total_time / len(katakana_list), 2)
            wrong_count = len(self.wrong)

            stats = {
                "total_time":    f"Total time:    {total_time} sec",
                "per_kana":      f"Time per kana: {per_kana} sec",
                "wrong_count":   f"You got:  {wrong_count} kana wrong",
            }
            stats_str = "\n".join(stats.values())

            self.end_stats = tk.Label(self.root, text=stats_str, bg=bgc, fg=txtc, font=("courier", 9))
            self.end_stats.pack(pady=20)

            def more_info():
                wrong_str = ""
                for x, y in self.wrong.items():
                    wrong_str += f"{x}={y}    "
                messagebox.showinfo(f"wrong kana", f"you got the following katakana wrong:\n\n{wrong_str}")

            self.back_to_menu = tk.Button(self.root, text="start menu", command=self.menu)
            self.back_to_menu.pack()
            self.back_to_menu.place(y=211, x=190)

            if wrong_count >0:
                self.more = tk.Button(self.root, text="show more", command=more_info)
                self.more.pack(padx=(0, 75))
            else:
                self.back_to_menu.place_configure(y=211, x=142)           

            try:   
                with open("stats.json", "r") as s:
                    json_stats = json.load(s)
            except FileNotFoundError:
                json_stats = {"tpk": []}
            
            json_stats["tpk"].append(per_kana)
            with open("stats.json", "w") as s:
                json.dump(json_stats, s, indent=4)
        
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



