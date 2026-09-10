#Docs_md.gui_output.md

#HAving just made a sublocation view update:

World object / Character
        ↓
get_percept_data(observer)
        ↓
observer.percepts
        ↓
get_sublocation_percepts()
        ↓
semantic percepts

                    ┌→ Character display transformation
                    │
percepts ───────────┤
                    │
                    └→ Object DisplayNode tree
                              ↓
                       display aggregation


        Tkinter
        ↓
Sublocation entity page





is_highlighted_percept()
    → decides WHICH tag a row gets

tag_configure()
    → decides HOW that tag looks

    