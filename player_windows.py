# אליהו אטין 205868771
#גיא רג'ואן 322985409


import socket
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "192.168.56.1"
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    send(soc, "can I connect?")
    isPlaying = True

    while isPlaying:
        playerCard = receive(soc)
        if playerCard == "endGame":
            total = receive(soc)
            print("The game has ended!")
            if int(total) > 0:
                print("Player lose: " + str(abs(int(total))) + "$")
                print("Dealer is the winner!")
            elif int(total) < 0:
                print("Player win: " + str(abs(int(total))) + "$")
                print("Player is the winner!")
            else:
                print("is a tie")

            action = input("would you like to play again? (y/n)  -> ")
            while not(action == "y" or action == "n"):
                action = input("would you like to play again? (y/n)  -> ")
            if action == "y":
                send(soc, "yes")
                isPlaying = True
            else:
                send(soc, "no")
                isPlaying = False

        else:
            action = input("Enter bet: ")
            send(soc, action)

            if action == "status":
                numberOfRound = str(int(receive(soc))-1)
                total = receive(soc)
                print("Current round: " + numberOfRound)
                if int(total) > 0:
                    print("Dealer won: " + str(abs(int(total))) + "$")
                elif int(total) < 0:
                    print("Player won: " + str(abs(int(total))) + "$")
                else:
                    print("Tie")

            elif action == "end game":
                numberOfRound = str(int(receive(soc))-1)
                total = receive(soc)
                isPlaying = False
                print("The game has ended on round " + numberOfRound + "!")
                print("The player quit.")
                if int(total) > 0:
                    print("Player lost: " + str(abs(int(total))) + "$")
                elif int(total) < 0:
                    print("Player won: " + str(abs(int(total))) + "$")
                else:
                    print("Tie")
                print("Thanks for playing.")
            else:

                dealerCard = receive(soc)
                winner = receive(soc)
                numberOfRound = receive(soc)

                if winner == "-1":
                    print("The result of round " + numberOfRound + ":")
                    print("Dealer won: " + action + "$")
                    print("Dealer's card: " + dealerCard)
                    print("Player's card: " + playerCard)
                elif winner == "1":
                    print("The result of round " + numberOfRound + ":")
                    print("Player won: " + action + "$")
                    print("Dealer's card: " + dealerCard)
                    print("Player's card: " + playerCard)
                else:
                    print("The result of round " + numberOfRound + " is a tie")
                    print("Dealer's card: " + dealerCard)
                    print("Player's card: " + playerCard)
                    print("The bet: " + action + "$")
                    respond = input("Do you wish to surrender or go to war? (s/w) ->  ")
                    while not (respond == "s" or respond == "w"):
                        respond = input("Do you wish to surrender or go to war? (s/w) ->  ")
                    send(soc, respond)
                    if respond == "s":
                        print("Round " + numberOfRound + " tie breaker:")
                        print("Player surrendered!")
                        print("The bet: " + action + "$")
                        print("Player won: " + str(int(action) / 2) + "$")
                        print("Dealer won: " + str(int(action) / 2) + "$")
                    else:
                        enoughCards = receive(soc)
                        if enoughCards == "ok":
                            playerCard = receive(soc)
                            dealerCard = receive(soc)
                            winner = receive(soc)
                            numberOfRound = receive(soc)

                            if winner == "-1":
                                print("Round " + numberOfRound + " tie breaker:")
                                print("Going to war!")
                                print("3 cards were discarded")
                                print("Original bet:" + action + "$")
                                print("New bet: " + str(int(action)*2) + "$")
                                print("Dealer's card: " + dealerCard)
                                print("Player's card: " + playerCard)
                                print("Dealer won: " + str(int(action)*2) + "$")
                            elif winner == "1":
                                print("Round " + numberOfRound + " tie breaker:")
                                print("Going to war!")
                                print("3 cards were discarded")
                                print("Original bet:" + action + "$")
                                print("New bet: " + str(int(action) * 2) + "$")
                                print("Dealer's card: " + dealerCard)
                                print("Player's card: " + playerCard)
                                print("Player won: " + action + "$")
                            else:
                                print("Round " + numberOfRound + " tie breaker:")
                                print("Going to war!")
                                print("3 cards were discarded")
                                print("Original bet:" + action + "$")
                                print("New bet: " + str(int(action) * 2) + "$")
                                print("Dealer's card: " + dealerCard)
                                print("Player's card: " + playerCard)
                                print("Player won: " + str(int(action) * 2) + "$")











def receive(connection):
    client_input = connection.recv(1024)
    return str(client_input.decode("utf8").rstrip())


def send(connection, message):
    connection.send(message.encode("utf8"))

if __name__ == "__main__":
    main()