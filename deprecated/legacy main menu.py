print("Default city loaded")
    while True:
        print("\nOptions:")
        print("1. Simulate Turn")
        print("2. View City Status")
        print("3. Exit")

        choice = input("Choose an option: ")
        print(f"User selected: {choice}")

        if choice == "1":
            simulate_turn()
        elif choice == "2":
            display_status()
        elif choice == "3":
            print("Exiting the game...")
            break  # Exit the loop and end the program
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()