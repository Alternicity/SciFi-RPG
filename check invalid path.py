import os

path = "C:\\Users\\Stuart\\Python Scripts\\scifiRPG\\scifiRPG\\data\\Test City\\Regions\\North.json"
if os.path.exists(path):
    print("Path is valid!")
else:
    print("Path is invalid!")
