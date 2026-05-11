#GUI.gui.py
import tkinter as tk
from tkinter import ttk
from GUI.helpers.gui_logging import gui_log

class TC2GUI:

    def __init__(self, root, game_state):

        self.root = root
        self.game_state = game_state
        self.root.title("TC2 Observer")
        self.root.geometry("1400x900")
        self.npc_lookup = {}
        self.current_mode = "npc"
        # --- Top Bar ---

        top_bar = ttk.Frame(root)
        top_bar.pack(fill="x")

        ttk.Label(
            top_bar,
            text="Mode:"
        ).pack(side="left", padx=5, pady=5)

        self.main_notebook = ttk.Notebook(root)
        self.main_notebook.pack(fill="both", expand=True)

        self.mode_var = tk.StringVar(value="npc")

        mode_dropdown = ttk.Combobox(
            top_bar,
            textvariable=self.mode_var,
            values=[
                "npc",
                "city",
                "faction",
                "debug"
            ],
            state="readonly",
            width=15
        )

        mode_dropdown.pack(side="left", padx=5)
        mode_dropdown.bind(
            "<<ComboboxSelected>>",
            self.on_mode_change
        )
        
        self.selected_npc = None
        self.load_mode(self.current_mode)

    def on_npc_select(self, event):

        selection = self.npc_listbox.curselection()

        if not selection:
            return

        selected_text = self.npc_listbox.get(selection[0])

        npc = self.npc_lookup[selected_text]

        self.selected_npc = npc

        self.refresh_npc_view()

    def on_mode_change(self, event):

        selected_mode = self.mode_var.get()

        self.current_mode = selected_mode

        self.load_mode(selected_mode)

    def load_mode(self, mode_name):
        gui_log(f"Loading mode: {mode_name}")
        self.clear_tabs()

        if mode_name == "npc":
            self.load_npc_mode()#so this call?

        elif mode_name == "city":
            self.load_city_mode()

        elif mode_name == "faction":
            self.load_faction_mode()

    def refresh_npc_view(self):
        #TMP
        if not self.selected_npc:
            return

        self.npc_name_label.config(
            text=self.selected_npc.name
        )

        print(
            f"Selected NPC: "
            f"{self.selected_npc.name} "
            f"{self.selected_npc.debug_role}"
        )

    def clear_tabs(self):

        for tab_id in self.main_notebook.tabs():
            self.main_notebook.forget(tab_id)

    def load_npc_mode(self):

        npc_frame = ttk.Frame(self.main_notebook)

        self.main_notebook.add(
            npc_frame,
            text="NPC Observer"
        )

        left_panel = ttk.Frame(npc_frame)
        left_panel.pack(side="left", fill="y")

        right_panel = ttk.Frame(npc_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        self.npc_name_label = ttk.Label(
            right_panel,
            text="No NPC Selected"
        )
        #is game_state object even availabel at all here?
        print("DEBUG NPCS:")
        print(self.game_state.debug_npcs)

        self.npc_name_label.pack(pady=10)

        self.npc_listbox = tk.Listbox(left_panel)
        self.npc_listbox.pack(fill="y", expand=True)

        # Prefer debug NPCs if available
        if self.game_state.debug_npcs:

            npc_source = self.game_state.debug_npcs.items()

        else:

            npc_source = [
                (npc.name, npc)
                for npc in self.game_state.all_characters[:20]
            ]

        for key, npc in npc_source:

            debug_role = getattr(npc, "debug_role", "npc")

            display_name = f"{key}: {npc.name} ({debug_role})"

            self.npc_listbox.insert(
                tk.END,
                display_name
            )

            self.npc_lookup[display_name] = npc

        self.npc_listbox.bind(
            "<<ListboxSelect>>",
            self.on_npc_select
        )



        self.npc_listbox.bind(
            "<<ListboxSelect>>",
            self.on_npc_select
        )

    def load_city_mode(self):

        self.create_city_tab()
        self.create_debug_tab()


    def load_faction_mode(self):

        self.create_faction_tab()
        self.create_debug_tab()


    def load_debug_mode(self):

        self.create_debug_tab()


        self.npc_name_label.pack()

    def create_faction_tab(self):

        tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(tab, text="Faction")

        ttk.Label(
            tab,
            text="Faction Overview"
        ).pack(padx=20, pady=20)


 


def launch_gui(game_state):

    root = tk.Tk()

    app = TC2GUI(root, game_state)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()