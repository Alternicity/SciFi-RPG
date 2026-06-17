#GUI.gui.py
import tkinter as tk
from tkinter import ttk
from collections import deque
from base.location import Sublocation
from base.character import Character
from GUI.inspectors.entity.npc_inspector import build_npc_inspector
from GUI.inspectors.npc.sublocation_inspector import build_sublocation_inspector

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

from faction import Gang
from faction import Corporation
from faction import State

""" NEW architecture:
mode frame
    -> internal notebook """
class TC2GUI:
    #Replace Listbox with clickable frames
    def __init__(self, root, game_state):

        self.root = root
        self.game_state = game_state

        # --- single source of truth for UI state ---
        self.active_context = {#Observer context
            "mode": "npc",#im not sure if this is legit, ir used, it could be a legacy
            "faction": None,
            "npc": None,
            "entity": None,
            "region": None,
            "location": None,
            "sublocation": None
        }
        
        #Current target of attention
        self.inspected_target = None

        self.current_page = None#line 51

        """active_context
            Who or what am I following?

        inspected_target
            What is highlighted in right sidebar?

        current_page
            What is occupying the main panel? """

        self.mode_var = tk.StringVar(value=self.active_context["mode"])
        self.recent_npcs = deque(maxlen=20)
        self.root.title("World/Sim Inspector")
        self.root.geometry("1400x900")

        self.npc_lookup = {}
        self.sim_running = False

        self.build_top_bar()
        
        #refactor
        self.mode_container = ttk.Frame(self.root)#parent for all modes.
        self.mode_container.pack(fill="both", expand=True)
        
        self.mode_frames = {}

        self.update_loop()

        #refactor
        """ mode switching = switching outer frames
        notebooks STILL EXIST INSIDE MODES """
        self.build_npc_mode()
        self.build_city_mode()
        self.build_faction_mode()

        self.switch_mode(#note there are other self.switch_mode( entries in this file
            self.active_context["mode"]
        )


        self.mode_var.set(#attempt to populate intial mode selector with text
            self.active_context["mode"]
        )

    #refactor
    def build_npc_mode(self):
        """
        Build NPC mode widgets once.

        Widgets created here persist for the lifetime of the GUI.

        Refresh functions update these widgets but never recreate them.
        Page navigation should hide/show containers rather than destroy
        notebook infrastructure.
        """

        frame = ttk.Frame(self.mode_container)

        left_panel = ttk.Frame(frame)
        self.npc_main_panel = ttk.Frame(frame)

        self.npc_inspector_panel = ttk.Frame(
            frame,
            width=250
        )

        left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )
        
        self.npc_main_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.npc_page_container = ttk.Frame(
            self.npc_main_panel
        )

        self.npc_page_container.pack(
            fill="both",
            expand=True
        )

        self.detail_page_container = ttk.Frame(
            self.npc_main_panel
        )#Notice: Do NOT pack it yet. Initially only the notebook page is visible.

        self.mode_frames["npc"] = frame

        self.npc_inspector_panel.pack(
            side="right",
            fill="y"
        )
        
        ttk.Label(
            self.npc_inspector_panel,
            text="Inspector"
        ).pack(
            padx=10,
            pady=10
        )

        self.npc_name_label = ttk.Label(
            self.npc_page_container,
        )

        self.npc_name_label.pack(pady=10)
        
        npc_notebook = ttk.Notebook(
            self.npc_page_container
        )

        npc_notebook.pack(fill="both", expand=True)
        self.npc_notebook = npc_notebook

        overview_tab = ttk.Frame(npc_notebook)

        #centre panel tabs
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

        self.npc_listbox = tk.Listbox(left_panel)
        self.npc_listbox.pack(fill="y", expand=True)

        ttk.Separator(
            left_panel,
            orient="horizontal"
        ).pack(fill="x", pady=10)

        recent_header = ttk.Label(
            left_panel,
            text="Recent NPCs"
        )

        recent_header.pack(pady=(5, 2))

        self.recent_npcs_frame = ttk.Frame(left_panel)

        self.recent_npcs_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 10)
        )
        self.refresh_recent_npcs()

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

        print(self.npc_name_label.winfo_parent())
        print(self.npc_notebook.winfo_parent())
        #print(self.page_container)

    def build_city_mode(self):

        frame = ttk.Frame(self.mode_container)

        self.mode_frames["city"] = frame

        from GUI.tabs.city.city_map_tab import (
            create_city_map_tab
        )

        create_city_map_tab(
            self,
            frame
        )

    def build_faction_mode(self):
        """ left | center | inspector
        which mirrors NPC mode. """

        frame = ttk.Frame(self.mode_container)

        self.mode_frames["faction"] = frame

        

        left_panel = ttk.Frame(frame)

        center_panel = ttk.Frame(frame)

        self.faction_inspector_panel = ttk.Frame(
            frame,
            width=250
        )

        left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        

        self.faction_inspector_panel.pack(
            side="right",
            fill="y"
        )

        ttk.Label(
            self.faction_inspector_panel,
            text="Inspector"
        ).pack(
            padx=10,
            pady=10
        )

        center_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        from GUI.inspectors.faction.faction_overview_panel import (
            build_faction_selector
        )

        from GUI.tabs.faction.build_faction_parts import (
            build_faction_center
        )

        build_faction_selector(
            self,
            left_panel
        )

        build_faction_center(
            self,
            center_panel
        )

    def refresh_all(self):
        #NEVER create widgets inside refresh functions. (refactor)
        mode = self.active_context.get("mode")

        self.refresh_time_display()

        if mode == "npc":
            self.refresh_npc_view()

        elif mode == "city":
            self.refresh_city_view()

        elif mode == "faction":
            self.refresh_faction_view()

    def open_npc(self, npc):
        self.current_page = "npc"
        self.show_npc_page()#recent approach, ensures returning to an NPC restores the notebook page

        if npc.location:
            npc.observe(
                location=npc.location,
                region=npc.location.region
            )

        self.active_context["npc"] = npc
        self.active_context["entity"] = npc
        self.active_context["faction"] = None
        self.active_context["location"] = None


        if npc in self.recent_npcs:
            self.recent_npcs.remove(npc)

        self.recent_npcs.appendleft(npc)

        self.switch_mode("npc")

        self.refresh_npc_view()   # TEST

        if hasattr(self, "recent_npcs_frame"):
            self.refresh_recent_npcs()

    def open_faction(self, faction):
        from GUI.inspectors.faction.faction_overview_panel import refresh_faction_list
        print(f"OPEN FACTION {faction}")
        self.active_context["faction"] = faction
        self.active_context["entity"] = faction
        self.active_context["npc"] = None
        
        if faction.type == "gang":
            faction_type = "Gangs"

        elif faction.type == "corporation":
            faction_type = "Corporations"

        elif faction.type == "state":
            faction_type = "State"

        else:
            faction_type = "Gangs"

        self.switch_mode("faction")
        self.faction_type_var.set(faction_type)
        refresh_faction_list(self)

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
                "faction"
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

        simulate_hours(self.game_state.all_characters, num_ticks=1)

        self.refresh_all()
        self.root.update_idletasks()

    def reset_city_navigation(self):
        #used by mode selector: city and the back button in locations view
        #resets state, calls rebuild_city_map()
        print("RESET CITY NAVIGATION")

        self.active_context["region"] = None
        self.active_context["location"] = None

        self.rebuild_city_map()

    def on_city_back(self):
        self.reset_city_navigation()
        """ you can completely skip introducing on_city_back() unless later you need:
        logging, breadcrumbs, stack popping, animations, transition effects, confirmation dialogs """

    def on_npc_select(self, event):
        
        #tmp
        print("NPC SELECT CLICK")
        print(self.active_context)


        
        selection = self.npc_listbox.curselection()
        if not selection:
            return
    
        display_name = self.npc_listbox.get(selection[0])

        npc = self.npc_lookup.get(display_name)

        if not npc:
            return

        self.open_npc(npc)

    def on_mode_change(self, event):

        mode = self.mode_var.get()

        if mode == "npc":
            self.active_context["faction"] = None

        elif mode == "faction":
            self.active_context["npc"] = None

        self.switch_mode(mode)
        
    def switch_mode(self, mode_name):
        self.clear_inspector()
        current_mode = self.active_context["mode"]

        # Re-selecting city mode resets navigation
        if mode_name == "city":
            self.reset_city_navigation()

        self.active_context["mode"] = mode_name
        self.mode_var.set(mode_name)

        for frame in self.mode_frames.values():
            frame.pack_forget()

        active_frame = self.mode_frames[mode_name]

        active_frame.pack(fill="both", expand=True)

        self.refresh_all()

    def refresh_npc_view(self):
        """
        Update existing NPC widgets.

        This function assumes the NPC notebook and its tabs already exist.
        It must never create or destroy widgets.
        """
        print("REFRESH NPC VIEW")
        print("current_page =", self.current_page)

        #suspect verbose print
        print(self.active_context)

        npc = self.active_context["npc"]

        if not npc:
            return

        if self.current_page != "npc":
            return
        
        if self.active_context["mode"] != "npc":
            return

        print("npc_name_label =", self.npc_name_label)
        print("exists =", self.npc_name_label.winfo_exists())

        self.npc_name_label.config(
            text=npc.name
        )
        print("REFRESH NPC VIEW")
        print(f"SELECTED NPC", {npc.name})
        
        #self.refresh_time_display()

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
        pass

        # Clear mode-specific references

        self.npc_lookup = {}

        self.overview_labels = {}
        self.stat_vars = {}
        self.stat_labels = {}
        """ Later this can evolve into:
        self.clear_npc_state()
        self.clear_city_state()
        self.clear_faction_state() """


    def load_npc_mode(self):
        pass

    def refresh_recent_npcs(self):#line 411

        for w in self.recent_npcs_frame.winfo_children():
            w.destroy()

        for npc in self.recent_npcs:

            btn = ttk.Button(
                self.recent_npcs_frame,
                text=f"{npc.__class__.__name__}: {npc.name}",
                command=lambda n=npc: self.open_npc(n)
            )

            btn.pack(fill="x", pady=1)


    def load_city_mode(self):

        self.create_city_tab()

        #not yet
        #self.create_debug_tab()


    def load_faction_mode(self):

        self.create_faction_tab()


    def load_debug_mode(self):

        self.create_debug_tab()


        self.npc_name_label.pack()


    def refresh_city_view(self):

        from GUI.inspectors.city.city_overview_panel import (
            refresh_city_overview
        )
        print("REFRESH CITY VIEW")
        refresh_city_overview(self)

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

        self.refresh_region_view()

    def open_region(self, region):

        self.active_context["region"] = region
        self.active_context["location"] = None

        self.show_region_locations(region)

    def refresh_region_view(self):

        refresh_region_panel(self)

    def show_region_locations(self, region):
        from GUI.inspectors.city.region_locations_panel import build_region_locations_view
        for widget in self.city_center_frame.winfo_children():
            widget.destroy()

        build_region_locations_view(
            self,
            self.city_center_frame,
            region
        )

    def open_location(self, location):

        self.active_context["location"] = location

        print(f"Open location: {location.name}")

        self.show_location_view(location)


    def open_sublocation(self, sublocation):

        self.active_context["sublocation"] = sublocation

        print(f"Open sublocation: {sublocation.name}")
        
        self.show_sublocation_view(sublocation)

    def show_location_view(self, location):

        from GUI.inspectors.city.location_panel import build_location_view

        for widget in self.city_center_frame.winfo_children():
            widget.destroy()

        build_location_view(
            self,
            self.city_center_frame,
            location
        )

    def rebuild_city_map(self):
        #redraws UI only
        for widget in self.city_center_frame.winfo_children():
            widget.destroy()

        from GUI.tabs.city.city_map_canvas import build_city_map_canvas

        build_city_map_canvas(
            self,
            self.city_center_frame
        )

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

        faction = self.faction_lookup[name]

        self.open_faction(faction)
        
        
    def create_faction_tab(self):

        from GUI.tabs.faction.faction_tab import (
            create_faction_tab
        )

        

        """ tab = ttk.Frame(
            self.main_notebook
        )

        self.main_notebook.add(
            tab,
            text="Faction"
        ) """

        """ create_faction_tab(
            self,
            tab
        ) """

    def refresh_faction_view(self):
        from GUI.inspectors.faction.faction_characters_panel import (
            refresh_faction_characters
        )
        from GUI.inspectors.faction.faction_economy_panel import refresh_faction_economy_panel
        from GUI.inspectors.faction.faction_overview_panel import refresh_faction_overview
        faction = self.active_context["faction"]
        mode = self.active_context["mode"]

        print(f"refresh_faction_view: {faction}")
        if mode != "faction":
            print(f"refresh_faction_view: oof {faction}")

            return

        if not faction:
            return

        refresh_faction_overview(self)
        refresh_faction_characters(self)
        refresh_faction_hq_panel(self)
        refresh_faction_economy_panel(self)#self to match the other calls above, gui was marked not defined here

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
        
    def show_sublocation_center_view(self, sublocation):
        self.current_page = "sublocation"
        
        from GUI.helpers.gui_helpers import clear_frame
        from GUI.inspectors.npc.sublocation_inspector import (
            build_sublocation_inspector
        )

        self.clear_main_panel()
        
        self.show_detail_page()

        build_sublocation_inspector(
            self,
            self.detail_page_container,
            sublocation
        )

        self.clear_inspector()
    
    def show_sublocation_view(self, sublocation):

        from GUI.inspectors.npc.sublocation_inspector import (
            build_sublocation_inspector
        )

        self.clear_main_panel()
        self.show_detail_page()

        build_sublocation_inspector(
            self,
            self.detail_page_container,#updated
            sublocation
        )
        #but there was no self.
        #show_detail_page()
        #here. Should there be?

    def refresh_inspector(self):
        
        parent = self.get_inspector_parent()

        target = self.inspected_target
        print("INSPECTOR TARGET:", target)
        
        if target is None:
            return

        if isinstance(target, Sublocation):

            build_sublocation_inspector(
                self,
                parent,
                target
            )
        elif isinstance(target, Character):
            build_npc_inspector(
                self,
                parent,
                target
            )

        print("INSPECTOR PANEL =", self.npc_inspector_panel)
        print("MODE =", self.active_context["mode"])
        
    def clear_main_panel(self):
        from GUI.helpers.gui_helpers import clear_frame
        """ We are no longer clearing notebook widgets.
        Only temporary pages. """
        clear_frame(self.detail_page_container)

    def show_npc_page(self):
        #latest approach,official page switcher
        self.detail_page_container.pack_forget()

        self.npc_page_container.pack(
            fill="both",
            expand=True
        )

    def show_detail_page(self):
        #latest approach, official page switcher
        self.npc_page_container.pack_forget()

        self.detail_page_container.pack(
            fill="both",
            expand=True
        )

    def show_npc_entity_view(self, observer, target):
        #not switching observer, viewing another npc, from slected npcs perspective
        from GUI.inspectors.entity.npc_entity_page import build_npc_entity_page
        from GUI.helpers.gui_helpers import clear_frame
        self.current_page = "entity"
        self.clear_inspector()
        self.clear_main_panel()
        #clear_frame(self.npc_main_panel)

        print("SHOW NPC ENTITY VIEW")#the commetn already existed
        print("observer =", observer.name)
        print("target =", target.name)

        self.show_detail_page()#new approach
        build_npc_entity_page(
            self,
            self.detail_page_container,#is this right?
            observer,
            target
        )

        if observer is target:
            self.open_npc(observer)
            return
    
    def inspect(self, thing):
        self.inspected_target = thing
        self.refresh_inspector()

    def clear_inspector(self):
        from GUI.helpers.gui_helpers import clear_frame
        self.inspected_target = None

        clear_frame(
            self.get_inspector_parent()
        )

    def get_inspector_parent(self):

        #maybe
        mode = self.active_context["mode"]

        if self.active_context["mode"] == "faction":
            return self.faction_inspector_panel

        return self.npc_inspector_panel

#utility function


def launch_gui(game_state):

    root = tk.Tk()

    app = TC2GUI(root, game_state)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()