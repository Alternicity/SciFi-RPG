import time
import sys
import os
import logging
# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generators.generate import generate_city_data  #Import the city generation function
import curses

print("Current Working Directory:", os.getcwd())
# Setup logging for debugging and tracking progress
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def display_menu(stdscr):
    stdscr.clear()  # Clear the screen
    stdscr.addstr("Welcome to the RPG Generator!\n")
    stdscr.addstr("1: Generate City\n")
    stdscr.addstr("2: Placeholder\n")
    stdscr.addstr("3: Exit\n")
    stdscr.refresh()

def main(stdscr):
    while True:
        display_menu(stdscr)  # Display the menu in curses window
        key = stdscr.getch()  # Get user input (single key press)

        # Handle user input using ord() to detect keys
        if key == ord('1'):
            stdscr.clear()
            stdscr.addstr("Starting city generation...\n")
            stdscr.refresh()
            try:
                # Call the city generator function
                generate_city_data()
                stdscr.addstr("City generation complete.\n")
            except Exception as e:
                stdscr.addstr(f"Error generating city: {e}\n")
            stdscr.refresh()
            time.sleep(1)  # Adding a short delay to simulate processing
        elif key == ord('2'):
            stdscr.clear()
            stdscr.addstr("Placeholder option selected.\n")
            stdscr.refresh()
            time.sleep(1)
        elif key == ord('3'):
            stdscr.clear()
            stdscr.addstr("Exiting...\n")
            stdscr.refresh()
            break
        else:
            stdscr.clear()
            stdscr.addstr("Invalid option. Please press 1, 2, or 3.\n")
            stdscr.refresh()
            time.sleep(1)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
