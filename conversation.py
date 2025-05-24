# conversation.py
from events import Event

class Conversation(Event):
    def __init__(self, speaker, listener, participants, topics):
        self.speaker = speaker
        self.listener = listener
        self.context = {}  # Store modifiers like reputation, memory stubs, etc.
        self.participants = []
        self.topics = []


    def start(self):
        print(f"{self.listener.name} begins talking to {self.speaker.name}.")

        # Stub options
        print("1. Greet")
        print("2. Ask about this place")
        print("3. End conversation")
        choice = input("Choose an option: ")

        if choice == "1":
            print(f"{self.speaker.name} says: 'Hello.'")
        elif choice == "2":
            print(f"{self.speaker.name} says: 'This place? It's seen better days.'")
        else:
            print("You end the conversation.")

class Gossip(Conversation):
    pass

class BoardRoomMeeting(Conversation):
    pass

class ChanceMeeting(Conversation):
    pass

class Meetup(Conversation):
    pass