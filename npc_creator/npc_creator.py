#npc_creator_npc_creator.py
import tkinter as tk
from tkinter import ttk
import json
import sys
import os
from tkinter import messagebox

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from base.character import Character
from create.create_character_names import create_name


class NPCCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("NPC Creator")

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

        ttk.Label(stats_tab, text="Strength").pack()
        self.strength_slider = tk.Scale(stats_tab, from_=1, to=20, orient="horizontal")
        self.strength_slider.set(10)
        self.strength_slider.pack()

        # --- Fun Prefs Tab ---
        fun_tab = ttk.Frame(notebook)
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


        self.personality_vars = {
            "extroversion": tk.IntVar(value=10),
            "curiosity": tk.IntVar(value=10),
            "discipline": tk.IntVar(value=10),
            "agreeableness": tk.IntVar(value=10),
            "neuroticism": tk.IntVar(value=10),
        }

        # --- Personality Tab ---
        personality_tab = ttk.Frame(notebook)
        notebook.add(personality_tab, text="Personality")

        self.personality_vars = {}
        self.personality_pool = 60

        ttk.Label(personality_tab, text=f"Points Remaining: {self.personality_pool}").pack()
        self.pool_label = ttk.Label(personality_tab)
        self.pool_label.pack()

        for trait in ["extroversion", "curiosity", "discipline", "agreeableness", "neuroticism"]:
            ttk.Label(personality_tab, text=trait.capitalize()).pack()

            var = tk.IntVar(value=10)
            self.personality_vars[trait] = var

            slider = tk.Scale(
                personality_tab,
                from_=1,
                to=20,
                orient="horizontal",
                variable=var,
                var.trace_add("write", lambda *args, t=trait: self.on_personality_change(t))#this isnt right, it is marked
            )
            slider.pack()

        # --- Save Button ---
        save_button = ttk.Button(root, text="Save NPC", command=self.save_npc)
        save_button.pack(pady=10)

    def update_personality_pool(self):
        total = sum(var.get() for var in self.personality_vars.values())
        remaining = self.personality_pool - total

        self.pool_label.config(text=f"Points Remaining: {remaining}")

        self.previous_personality = {#is this the right placefor this block?
            trait: 10 for trait in self.personality_vars
        }


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

        if len(set(prefs)) == 1:
            messagebox.showerror(
                "Invalid Preferences",
                "Fun preferences must vary."
            )
            return

        data = {
            "name": self.name_entry.get(),
            "race": self.race_combo.get(),
            "sex": self.sex_combo.get(),
            "strength": self.strength_slider.get(),
            "fun_prefs": {
                "social": prefs[0],
                "nature": prefs[1],
                "learning": prefs[2],
                "sport": prefs[3],
            "personality": {
                trait: var.get()
                for trait, var in self.personality_vars.items()
            }
            }
            
        }


        with open("npc.json", "w") as f:
            json.dump(data, f, indent=2)

        messagebox.showerror("Saved npc.json")#not reaally an error, is this ok?

    def on_personality_change(self, changed_trait):#added inside class NPCCreator

        if self.updating:
            return

        self.updating = True

        total = sum(var.get() for var in self.personality_vars.values())

        if total > self.personality_pool:
            # revert
            self.personality_vars[changed_trait].set(
                self.previous_personality[changed_trait]
            )
        else:
            # accept change
            self.previous_personality[changed_trait] = self.personality_vars[changed_trait].get()

        self.update_personality_pool()

def launch_creator_ui():
    root = tk.Tk()
    app = NPCCreator(root)
    root.mainloop()




if __name__ == "__main__":
    launch_creator_ui()