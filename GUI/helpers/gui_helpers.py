#GUI.helpers.gui_helpers.py

""" def register_display_node(tree, item_id, node):
    tree._display_node_map[item_id] = node """
    #We can revisit the idea later if we discover that the Inspector genuinely needs the display node rather than its origin.
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def insert_blank_row(tree, parent=""):
    return tree.insert(
        parent,
        "end",
        text="",
        values=("", "", "")
    )

