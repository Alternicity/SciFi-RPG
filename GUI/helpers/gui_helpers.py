#GUI.helpers.gui_helpers.py

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

