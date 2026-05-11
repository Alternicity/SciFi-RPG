#list_display_functions.py
import ast
import os

INPUT_FILE = "display/display.py"
OUTPUT_FILE = "display_functions.txt"


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    source = f.read()

tree = ast.parse(source)

functions = []

for node in ast.walk(tree):

    if isinstance(node, ast.FunctionDef):

        functions.append(node.name)


functions.sort()


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for func in functions:
        f.write(func + "\n")


print(f"Found {len(functions)} functions.")
print(f"Saved to {OUTPUT_FILE}")