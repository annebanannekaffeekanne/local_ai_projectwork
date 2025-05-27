from LLM import ask_mistral_with_context

def main():
    print("ask local AI, type 'exit' to quit")
    while True:
        user_input = input("you: ")
        if user_input.lower() == "exit":
            break
        answer = ask_mistral_with_context(user_input)
        print("AI:", answer)

if __name__ == "__main__":
    main()