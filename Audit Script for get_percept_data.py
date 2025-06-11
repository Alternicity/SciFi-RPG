import os
import ast

PROJECT_ROOT = r"C:\Users\Niki\Documents\scifiRPG"
percept_funcs = []

class PerceptVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        if node.name == "get_percept_data":
            class_name = None
            parent = getattr(node, 'parent', None)
            while parent:
                if isinstance(parent, ast.ClassDef):
                    class_name = parent.name
                    break
                parent = getattr(parent, 'parent', None)

            percept_funcs.append((class_name, node.name, node.lineno, node.col_offset))
        self.generic_visit(node)

def annotate_tree(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def find_get_percept_data():
    for dirpath, _, filenames in os.walk(PROJECT_ROOT):
        for fname in filenames:
            if fname.endswith(".py"):
                full_path = os.path.join(dirpath, fname)
                with open(full_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=full_path)
                        annotate_tree(tree)
                        visitor = PerceptVisitor()
                        visitor.visit(tree)
                    except SyntaxError:
                        print(f"[WARNING] Could not parse {full_path}")

    print("\n=== get_percept_data() Implementations Found ===")
    for class_name, func_name, lineno, col in percept_funcs:
        print(f"{class_name or '[Global]'} → {func_name} at line {lineno}")

if __name__ == "__main__":
    find_get_percept_data()
