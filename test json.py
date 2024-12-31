with open("test_city.json", "r") as f:
    data = json.load(f)
    print(type(data))  # This should output: <class 'dict'>
