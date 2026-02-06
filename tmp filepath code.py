try:
        with open(filepath, "r", encoding="utf-8") as f:
            contents = f.readlines()
            print(f"DEBUG: File contents: {contents}")
    except Exception as e:
        print(f"ERROR: {e}")