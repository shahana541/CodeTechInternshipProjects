def display_menu():
    print("\n--- Codetech Interactive Chatbot ---")
    print("1 - Greet me")
    print("2 - What's your name?")
    print("3 - Tell me your favorite colors")
    print("4 - How's the weather?")
    print("5 - Help (show commands)")
    print("6 - Tell me a joke")
    print("7 - Exit")

def chatbot():
    knowledge = {
        "name": "My name is CodetechBot.",
        "colors": "I like blue and green.",
        "weather": "I don't have live weather info yet. Stay tuned!"
    }

    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]

    print("Welcome to your enhanced chatbot!\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            print("Chatbot: Hello! Hope you're having a great day!")
        elif choice == '2':
            print(f"Chatbot: {knowledge['name']}")
        elif choice == '3':
            print(f"Chatbot: {knowledge['colors']}")
        elif choice == '4':
            print(f"Chatbot: {knowledge['weather']}")
        elif choice == '5':
            print("Chatbot: Choose a command by typing the number (1-7).")
        elif choice == '6':
            import random
            joke = random.choice(jokes)
            print(f"Chatbot: Here's a joke for you: {joke}")
        elif choice == '7':
            print("Chatbot: Goodbye! Have a nice day ahead!")
            break
        else:
            print("Chatbot: Invalid choice, please select between 1 and 7.")

if __name__ == "__main__":
    chatbot()
