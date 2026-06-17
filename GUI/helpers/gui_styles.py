#GUI.helpers.gui_styles.py
from tkinter import ttk

TEXT_SELECTION = {
    "selectbackground": "#1f6aa5",
    "selectforeground": "white",
}



def configure_gui_styles():

    style = ttk.Style()

    style.configure(
        "EntityHeading.TLabel",
        font=("TkDefaultFont", 10, "bold")
    )