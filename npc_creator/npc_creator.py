#npc_creator_npc_creator.py
import tkinter as tk
from tkinter import ttk
import json
import sys
import os
from tkinter import messagebox

# Fix imports - existing code, is this deprecated?
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(
    BASE_DIR,
    "saved_npcs"
)
os.makedirs(SAVE_DIR, exist_ok=True)


from base.character import Character
from create.create_character_names import create_name


class NPCCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("NPC Creator")
        self.core_stats = [
            "strength",
            "agility",
            "intelligence",
            "concentration",
            "luck",
            "psy",
            "charisma",
            "toughness",
            "observation"
        ]
        
        self.stat_vars = {}
        self.stat_labels = {}
        self.previous_stats = {}

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # --- Identity Tab ---
        identity_tab = ttk.Frame(notebook)
        notebook.add(identity_tab, text="Identity")

        ttk.Label(identity_tab, text="Name").pack()
        self.name_entry = ttk.Entry(identity_tab)
        self.name_entry.pack()

        generate_name_btn = ttk.Button(identity_tab, text="Generate Name", command=self.generate_name)
        generate_name_btn.pack()

        ttk.Label(identity_tab, text="Race").pack()
        self.race_combo = ttk.Combobox(identity_tab, values=Character.VALID_RACES)
        self.race_combo.pack()

        ttk.Label(identity_tab, text="Sex").pack()
        self.sex_combo = ttk.Combobox(identity_tab, values=["male", "female"])
        self.sex_combo.pack()

        # --- Stats Tab ---
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Stats")

        self.stat_vars = {}
        self.stat_labels = {}

        BASE_STAT = 10
        STAT_POOL = 25

        self.remaining_points = tk.IntVar(value=STAT_POOL)

        ttk.Label(stats_tab, text="Points Remaining:").grid(row=0, column=0, sticky="w")
        self.points_label = ttk.Label(stats_tab, textvariable=self.remaining_points)
        self.points_label.grid(row=0, column=1, sticky="w")

        for row, stat in enumerate(self.core_stats, start=1):

            ttk.Label(stats_tab, text=stat.capitalize()).grid(row=row, column=0, sticky="w")

            var = tk.IntVar(value=BASE_STAT)
            self.stat_vars[stat] = var

            slider = tk.Scale(
                stats_tab,
                from_=1,
                to=20,
                orient="horizontal",
                variable=var,
                command=lambda val, s=stat: self.update_stat_pool(s)
            )

            slider.grid(row=row, column=1, sticky="ew")

        stats_tab.columnconfigure(1, weight=1)
        self.stat_vars[stat] = var
        self.previous_stats[stat] = BASE_STAT

        # --- Fun Prefs Tab ---
        fun_tab = ttk.Frame(notebook)#notebook not defined here
        notebook.add(fun_tab, text="Fun Prefs")

        ttk.Label(fun_tab, text="Social").pack()
        self.social_slider = tk.Scale(fun_tab, from_=1, to=10, orient="horizontal")
        self.social_slider.pack()

        ttk.Label(fun_tab, text="Nature").pack()
        self.nature_slider = tk.Scale(fun_tab, from_=1, to=10, orient="horizontal")
        self.nature_slider.pack()

        ttk.Label(fun_tab, text="Learning").pack()
        self.learning_slider = tk.Scale(fun_tab, from_=1, to=10, orient="horizontal")
        self.learning_slider.pack()

        ttk.Label(fun_tab, text="Sport").pack()
        self.sport_slider = tk.Scale(fun_tab, from_=1, to=10, orient="horizontal")
        self.sport_slider.pack()

        # --- Personality Tab ---
        personality_tab = ttk.Frame(notebook)
        notebook.add(personality_tab, text="Personality")
        personality_frame = ttk.LabelFrame(#parent container,widgets go INSIDE it
            personality_tab,
            text="Personality Traits"
        )
        personality_frame.pack(fill="both", expand=True, padx=10, pady=10)


        self.personality_vars = {}
        self.personality_pool = 60
        self.updating = False

        #ttk.Label(personality_tab, text=f"Points Remaining: {self.personality_pool}").pack()
        self.pool_label = ttk.Label(
            personality_frame,
            text=f"Points Remaining: {self.personality_pool}"
        )

        self.pool_label.grid(
            row=0,
            column=0,
            columnspan=2,#Label/Slider  
            pady=(0, 10)
        )
        #The pool label should span both columns
        traits = [
            "extroversion",
            "curiosity",
            "discipline",
            "agreeableness",
            "neuroticism"
        ]

        for row, trait in enumerate(traits, start=1):

            var = tk.IntVar(value=10)
            self.personality_vars[trait] = var

            label = ttk.Label(
                personality_frame,
                text=trait.capitalize()
            )

            label.grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=5
            )

            slider = tk.Scale(
                personality_frame,
                from_=1,
                to=20,
                orient="horizontal",
                variable=var
            )

            slider.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=5,
                pady=5
            )

            var.trace_add(
                "write",
                lambda *args, t=trait: self.on_personality_change(t)
            )
            
        # Allow slider column expansion
        personality_frame.columnconfigure(1, weight=1)

        self.previous_personality = {#self not defined
            trait: var.get()
            for trait, var in self.personality_vars.items()
        }

            
        # --- Save Button ---
        save_button = ttk.Button(root, text="Save NPC", command=self.save_npc)#root not defined here
        save_button.pack(pady=10)



    def update_stat_pool(self, changed_stat):

        BASE_STAT = 10
        STAT_POOL = 25

        total_spent = sum(
            var.get() - BASE_STAT
            for var in self.stat_vars.values()
        )

        remaining = STAT_POOL - total_spent

        # ❌ invalid move → revert
        if remaining < 0:

            self.stat_vars[changed_stat].set(
                self.previous_stats[changed_stat]
            )

            total_spent = sum(
                var.get() - BASE_STAT
                for var in self.stat_vars.values()
            )

            remaining = STAT_POOL - total_spent

        # ✅ valid move → commit
        else:
            self.previous_stats[changed_stat] = \
                self.stat_vars[changed_stat].get()

        self.remaining_points.set(remaining)




    def update_personality_pool(self):
        total = sum(var.get() for var in self.personality_vars.values())
        remaining = self.personality_pool - total

        self.pool_label.config(text=f"Points Remaining: {remaining}")



        # Optional: enforce hard limit
        if remaining < 0:
            self.pool_label.config(foreground="red")
        else:
            self.pool_label.config(foreground="black")

    def generate_name(self):
        race = self.race_combo.get()
        sex = self.sex_combo.get()

        if not race or not sex:
            messagebox.showerror(
                "Select race and sex first"
            )

            return

        first, family, full = create_name(race, sex)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, full)

    def save_npc(self):
        
        
        
        prefs = [
            self.social_slider.get(),
            self.nature_slider.get(),
            self.learning_slider.get(),
            self.sport_slider.get()
        ]

        if len(set(prefs)) != len(prefs):
            """ print("Fun prefs must all differ")
            return """

            messagebox.showerror(#the exisitng code used messagebox
                "Invalid Preferences",
                "Fun preferences must vary."
            )
            return

        data = {
            "name": self.name_entry.get(),
            "race": self.race_combo.get(),
            "sex": self.sex_combo.get(),
            
            "stats": {
                stat: var.get()
                for stat, var in self.stat_vars.items()
            },

            "personality": {
                trait: var.get()
                for trait, var in self.personality_vars.items()
            },

            "fun_prefs": {
                "social": prefs[0],
                "nature": prefs[1],
                "learning": prefs[2],
                "sport": prefs[3],
            }
        }
        
        if not data["name"]:
            messagebox.showerror(
                "Missing Name",
                "NPC must have a name."
            )
            return
        
        filepath = os.path.join(SAVE_DIR, f"{data['name']}.json")

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        messagebox.showinfo(
            "Success",
            f"Saved {data['name']}.json"
        )

    def on_personality_change(self, changed_trait):#added inside class NPCCreator

        if self.updating:
            return

        self.updating = True

        total = sum(var.get() for var in self.personality_vars.values())

        if total > self.personality_pool:
            # ❌ invalid → revert ONLY the changed one
            self.personality_vars[changed_trait].set(
                self.previous_personality[changed_trait]
            )
        # ✅ valid → commit new value
        self.previous_personality[changed_trait] = \
        self.personality_vars[changed_trait].get()
        self.update_personality_pool()
        self.updating = False

#utility functions

def launch_creator_ui():
    root = tk.Tk()
    app = NPCCreator(root)
    root.mainloop()




if __name__ == "__main__":
    launch_creator_ui()