import os

def send_message(message):
    # Run OLLAMA command-line tool to generate a response from the model
    output = os.popen(f"OLLAMA {message}").read()
    return output.strip()

def main():
    while True:
        try:
            message = input("You: ")
            response = send_message(message)
            print("OLLAMA:", response)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()