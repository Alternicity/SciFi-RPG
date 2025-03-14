from city_vars import GameState
game_state = None # Might be getting reset by an import


def get_game_state():
        """Ensures only one instance of GameState exists."""
        global game_state

        if game_state is None:
            game_state = GameState()
        else:
            pass

        #print(f"🚀 DEBUG: get_game_state() is now returning {game_state}")

        return game_state