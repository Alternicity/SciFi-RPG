#GUI.gui.py
import tkinter as tk
from tkinter import ttk
from GUI.helpers.gui_logging import gui_log
from GUI.inspectors.npc.npc_overview_panel import build_overview_panel, refresh_overview_panel
from GUI.inspectors.npc.memories.npc_memories_panel import build_memories_panel, refresh_memories_panel
from GUI.inspectors.npc.motivations.npc_motivations_panel import build_motivations_panel, refresh_motivations_panel
from GUI.inspectors.npc.percepts.npc_percepts_panel import build_percepts_panel, refresh_percepts_panel
from GUI.inspectors.npc.thoughts.npc_thoughts_panel import build_thoughts_panel, refresh_thoughts_panel
from GUI.inspectors.faction.faction_hq_panel import refresh_faction_hq_panel

from GUI.inspectors.city.city_region_panel import (
    refresh_region_panel,
)
from GUI.tabs.city.city_map_tab import create_city_map_tab

from faction import Gang
from faction import Corporation
from faction import State

class TC2GUI:

    def __init__(self, root, game_state):

        self.root = root
        self.game_state = game_state
        self.root.title("World/Sim Inspector")
        self.root.geometry("1400x900")

        self.npc_lookup = {}
        self.current_mode = "npc"
        self.sim_running = False

        self.mode_var = tk.StringVar(
            value=self.current_mode
        )

        self.build_top_bar()
        self.update_loop()
        
        self.main_notebook = ttk.Notebook(root)
        self.main_notebook.pack(fill="both", expand=True)
        
        self.selected_npc = None
        self.selected_region = None
        self.selected_faction = None
        self.selected_location = None

        # Future generalized selection
        self.selected_entity = None

        self.load_mode(self.current_mode)#line 44

    def build_top_bar(self):

        self.top_bar = ttk.Frame(self.root)
        self.top_bar.pack(fill="x")

        #Mode Selector
        ttk.Label(
            self.top_bar,
            text="Mode:"
        ).pack(side="left", padx=(5, 2), pady=5)

        mode_dropdown = ttk.Combobox(
            self.top_bar,
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
        mode_dropdown.pack(side="left", padx=(0, 10))
        mode_dropdown.bind(
            "<<ComboboxSelected>>",
            self.on_mode_change
        )

        #Button
        self.advance_tick_button = ttk.Button(
            self.top_bar,
            text="Advance 1 Tick",
            command=self.advance_one_tick
        )
        self.advance_tick_button.pack(side="left")

        #Day/Time
        self.time_label = ttk.Label(self.top_bar, text="")
        self.time_label.pack(side="right", padx=10)
        self.refresh_time_display()
        #add various refresh calls here, perhaps call a refresh_all() ? 

    def advance_one_tick(self):
        from simulate_day import simulate_hours
        simulate_hours(
            self.game_state.all_characters,
            num_ticks=1
        )

        #self.refresh_npc_view()
        self.refresh_time_display()

        if self.current_mode == "npc":
            self.refresh_npc_view()

        elif self.current_mode == "city":
            self.refresh_city_view()

        elif self.current_mode == "faction":
            self.refresh_faction_view()

        self.root.update_idletasks()



    def on_npc_select(self, event):

        selection = self.npc_listbox.curselection()

        if not selection:
            return

        display_name = self.npc_listbox.get(selection[0])

        self.selected_npc = self.npc_lookup.get(display_name)

        #self.refresh_npc_view()

        if self.selected_npc.location:
            region = getattr(
                self.selected_npc.location,
                "region",
                None
            )

        self.selected_npc.observe(
                location=self.selected_npc.location,
                region=self.selected_npc.location.region
            )

        self.refresh_npc_view()

        self.root.update_idletasks()

    def on_mode_change(self, event):

        selected_mode = self.mode_var.get()

        self.current_mode = selected_mode

        self.load_mode(selected_mode)

    def load_mode(self, mode_name):

        self.current_mode = mode_name

        gui_log(f"Loading mode: {mode_name}")

        self.clear_tabs()

        if mode_name == "npc":
            self.load_npc_mode()

        elif mode_name == "city":
            self.load_city_mode()

        elif mode_name == "faction":
            self.load_faction_mode()

    def refresh_npc_view(self):

        if not self.selected_npc:
            return
        
        self.npc_name_label.config(
            text=self.selected_npc.name
        )
        self.refresh_time_display()#or call from the sim loop

        try:
            refresh_overview_panel(self)
        except Exception as e:
            print(f"Overview refresh failed: {e}")

        try:
            refresh_thoughts_panel(self)
        except Exception as e:
            print(f"Thoughts refresh failed: {e}")

        try:
            refresh_motivations_panel(self)
        except Exception as e:
            print(f"Motivations refresh failed: {e}")

        try:
            refresh_memories_panel(self)
        except Exception as e:
            print(f"Memories refresh failed: {e}")

        try:
            refresh_percepts_panel(self)
        except Exception as e:
            print(f"Percepts refresh failed: {e}")

    def clear_tabs(self):

        for tab_id in self.main_notebook.tabs():
            self.main_notebook.forget(tab_id)

        # Clear mode-specific references

        self.npc_lookup = {}

        self.selected_npc = None

        self.overview_labels = {}
        self.stat_vars = {}
        self.stat_labels = {}
        """ Later this can evolve into:
        self.clear_npc_state()
        self.clear_city_state()
        self.clear_faction_state() """


    def load_npc_mode(self):

        npc_frame = ttk.Frame(self.main_notebook)

        self.main_notebook.add(
            npc_frame,
            text="NPC Observer"
        )
        #shall we put an outline here as well?
        left_panel = ttk.Frame(npc_frame)
        left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        right_panel = ttk.Frame(npc_frame)

        right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.npc_name_label = ttk.Label(
            right_panel,
            text="No NPC Selected"
        )

        self.npc_name_label.pack(pady=10)

        npc_notebook = ttk.Notebook(right_panel)
        npc_notebook.pack(fill="both", expand=True)

        overview_tab = ttk.Frame(npc_notebook)

        npc_notebook.add(overview_tab, text="Overview")

        thoughts_tab = ttk.Frame(npc_notebook)
        npc_notebook.add(thoughts_tab, text="Thoughts")

        motivations_tab = ttk.Frame(npc_notebook)
        npc_notebook.add(motivations_tab, text="Motivations")

        memories_tab = ttk.Frame(npc_notebook)
        npc_notebook.add(memories_tab, text="Memories")

        percepts_tab = ttk.Frame(npc_notebook)
        npc_notebook.add(percepts_tab, text="Percepts")

        build_overview_panel(self, overview_tab)
        build_thoughts_panel(self, thoughts_tab)
        build_motivations_panel(self, motivations_tab)
        build_memories_panel(self, memories_tab)
        build_percepts_panel(self, percepts_tab)

        self.stat_vars = {}
        self.stat_labels = {}

        #self.npc_name_label.pack(pady=10)

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

            display_name = (
                f"{key}: "
                f"{npc.name}"
            )

            self.npc_listbox.insert(
                tk.END,
                display_name
            )

            self.npc_lookup[display_name] = npc

        self.npc_listbox.bind(
            "<<ListboxSelect>>",
            self.on_npc_select
        )

    def load_city_mode(self):

        self.create_city_tab()

        #not yet
        #self.create_debug_tab()


    def load_faction_mode(self):

        self.create_faction_tab()
        self.create_debug_tab()

    def load_debug_mode(self):

        self.create_debug_tab()


        self.npc_name_label.pack()

    def create_city_tab(self):

        city_tab = ttk.Frame(self.main_notebook)

        self.main_notebook.add(
            city_tab,
            text="City"
        )

        create_city_map_tab(self, city_tab)

    def on_region_select(self, region):

        self.selected_region = region

        for rect_id in self.region_rectangles.values():

            self.map_canvas.itemconfig(
                rect_id,
                fill="gray20",
                outline="white",
                width=2
            )

        selected_rect = self.region_rectangles.get(
            region.id
        )

        if selected_rect:

            self.map_canvas.itemconfig(
                selected_rect,
                fill="steelblue",
                outline="yellow",
                width=4
            )

        refresh_region_panel(self)

        self.refresh_region_view()#is this stil necessary as well as the above?

    def refresh_region_view(self):

        refresh_region_panel(self)

    def on_faction_type_change(self,event):

        from GUI.inspectors.faction.faction_overview_panel import (
            refresh_faction_list
        )

        refresh_faction_list(self)


    def on_faction_select(self,event):

        selection=(
            self.faction_listbox.curselection()
        )

        if not selection:
            return

        name=(
            self.faction_listbox.get(
                selection[0]
            )
        )

        self.selected_faction=(
            self.faction_lookup[name]
        )

        self.selected_entity=(
            self.selected_faction
        )

        self.refresh_faction_view()
        
        
    def create_faction_tab(self):

        from GUI.tabs.faction.faction_tab import (
            create_faction_tab
        )

        tab = ttk.Frame(
            self.main_notebook
        )

        self.main_notebook.add(
            tab,
            text="Faction"
        )

        create_faction_tab(
            self,
            tab
        )
    def refresh_faction_view(self):
        from GUI.inspectors.faction.faction_characters_panel import (
            build_faction_characters_panel,
            refresh_faction_characters)
        
        from GUI.inspectors.faction.faction_overview_panel import refresh_faction_overview

        faction = self.selected_faction


        if not self.selected_faction:
            return

        refresh_faction_overview(self)
        refresh_faction_characters(self)
        refresh_faction_hq_panel(self)


        overview = [

            f"Name: {getattr(faction,'name','Unknown')}",
            f"Type: {getattr(faction,'type','Unknown')}",
            f"Members: {len(getattr(faction,'members',[]))}"

        ]

        if getattr(faction, "HQ", None):

            overview.append(
                f"HQ: {faction.HQ.name}"
            )

        else:

            overview.append(
                "HQ: None"
            )

        

        # Gang-specific

        if isinstance(faction, Gang):

            overview.extend([

                f"Violence: {faction.violence_disposition}",
                f"Race: {faction.race}",
                f"Boss: {faction.boss.name if faction.boss else 'None'}",
                f"Street Gang: {'Yes' if faction.is_street_gang else 'No'}",
                f"Captains: {len(faction.captains)}"

            ])


        # Corporation-specific

        elif isinstance(faction, Corporation):

            overview.extend([

                f"Violence: {faction.violence_disposition}",
                f"CEO: {faction.CEO.name if faction.CEO else 'None'}",
                f"Managers: {len(faction.managers)}",
                f"Security: {len(faction.security)}",
                f"Employees: {len(faction.employees)}"

            ])

        # State-specific

        elif isinstance(faction, State):

            overview.extend([

                f"Resources: {len(faction.resources)}",
                f"Laws: {len(faction.laws)}",
                f"Staff: {len(faction.state_staff)}"

            ])


        self.faction_overview_text.config(

            text="\n".join(overview)

        )

    def refresh_time_display(self):

        gs = self.game_state

        self.time_label.config(
            text=(
                f"Day {gs.day} | "
                f"Hour {gs.hour} | "
                f"{gs.get_day_phase()}"
            )
        )
    def update_loop(self):
        from simulate_day import simulate_hours
        if self.sim_running:

            simulate_hours(#not yet defined here
                self.game_state.all_characters,
                num_ticks=1
            )

            self.refresh_npc_view()
            self.refresh_time_display()

        self.root.after(250, self.update_loop)
        


#utility function


def launch_gui(game_state):

    root = tk.Tk()

    app = TC2GUI(root, game_state)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()