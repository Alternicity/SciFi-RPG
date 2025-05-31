import re
import shutil

filename = "location.py"
backup_filename = "location_backup.py"

# These are the default lines to add if missing
default_fields = {
    "security_level": "    security_level: int = 0\n",
    "is_open": "    is_open: bool = True\n",
    "has_security": "\n    def has_security(self):\n        return False\n"
}

# Backup the original
shutil.copyfile(filename, backup_filename)
print(f"📦 Backup created: {backup_filename}")

with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

output_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    output_lines.append(line)

    class_match = re.match(r"(?:@dataclass\s*\n)?class\s+(\w+)\((.*?)\):", line)
    if class_match:
        class_name = class_match.group(1)
        class_start_index = i
        indent = "    "

        # Collect class body until next class or end
        class_body_lines = []
        i += 1
        while i < len(lines) and not re.match(r"(?:@dataclass\s*\n)?class\s+(\w+)\((.*?)\):", lines[i]):
            class_body_lines.append(lines[i])
            i += 1

        class_body_str = "".join(class_body_lines)

        # Add missing fields
        inserted_any = False
        for field, default_line in default_fields.items():
            if field not in class_body_str:
                print(f"🔧 Injecting '{field}' into {class_name}")
                class_body_lines.insert(0, default_line)
                inserted_any = True

        output_lines.extend(class_body_lines)

        continue  # Skip the regular line incrementation

    i += 1

# Write the updated content back
with open(filename, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print("✅ Done! Missing attributes injected (if needed).")
print("🛡️  Original file backed up as:", backup_filename)
