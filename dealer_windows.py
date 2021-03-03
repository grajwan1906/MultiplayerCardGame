# אליהו אטין 205868771
#גיא רג'ואן 322985409

import socket
import sys
import traceback
from random import randrange
from threading import Thread
import time


def main():
    start_server()


def start_server():
    host = "172.18.22.72"
    port = 8888  # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                   1)  # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(2)  # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            Thread(target=client_thread, args=(soc, connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    soc.close()


def client_thread(soc, connection, ip, port):
    isPlaying = False
    firstMessage = receive(connection)
    if firstMessage == "can I connect?":
        isPlaying = True

    cards = ["Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks", "Ac", "Ad", "Ah", "As"]
    i = 2
    while i < 11:
        cards.append(str(i) + "c")
        cards.append(str(i) + "d")
        cards.append(str(i) + "h")
        cards.append(str(i) + "s")
        i += 1

    numberOfRound = 1
    total = 0

    while isPlaying:

        if len(cards) < 2:
            send(connection, "endGame")
            time.sleep(1)
            send(connection, str(total))
            respond = receive(connection)
            if respond == "no":
                isPlaying = False
            else:
                isPlaying = True
                numberOfRound = 1
                total = 0
                cards = ["Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks", "Ac", "Ad", "Ah", "As"]
                i = 2
                while i < 11:
                    cards.append(str(i) + "c")
                    cards.append(str(i) + "d")
                    cards.append(str(i) + "h")
                    cards.append(str(i) + "s")
                    i += 1
        else:
            playerCardIndex = randrange(len(cards))
            playerCard = cards[playerCardIndex]
            send(connection, playerCard)
            action = receive(connection)
            if action == "status":
                send(connection, str(numberOfRound))
                time.sleep(1)
                send(connection, str(total))
            elif action == "end game":
                send(connection, str(numberOfRound))
                time.sleep(1)
                send(connection, str(total))
                isPlaying = False
            else:
                cards.remove(playerCard)

                dealerCardIndex = randrange(len(cards))
                dealerCard = cards[dealerCardIndex]
                cards.remove(dealerCard)

                winner = checkWhoIsTheWinner(dealerCard, playerCard)

                send(connection, dealerCard)
                time.sleep(1)
                send(connection, str(winner))
                time.sleep(1)
                send(connection, str(numberOfRound))
                if winner == -1:
                    total += int(action)
                elif winner == 1:
                    total -= int(action)
                else:
                    respond = receive(connection)
                    if respond == "s":
                        total += int(int(action)/2)
                    else:
                        if len(cards) > 5:
                            send(connection, "ok")
                            cardIndex = randrange(len(cards))
                            cards.remove(cards[cardIndex])
                            cardIndex = randrange(len(cards))
                            cards.remove(cards[cardIndex])
                            cardIndex = randrange(len(cards))
                            cards.remove(cards[cardIndex])

                            playerCardIndex = randrange(len(cards))
                            playerCard = cards[playerCardIndex]
                            cards.remove(playerCard)

                            dealerCardIndex = randrange(len(cards))
                            dealerCard = cards[dealerCardIndex]
                            cards.remove(dealerCard)

                            send(connection, playerCard)
                            time.sleep(1)
                            send(connection, dealerCard)

                            winner = checkWhoIsTheWinner(dealerCard, playerCard)

                            time.sleep(1)
                            send(connection, str(winner))
                            time.sleep(1)
                            send(connection, str(numberOfRound))
                            if winner == -1:
                                total += (int(action)*2)
                            elif winner == 1:
                                total -= int(action)
                            else:
                                total -= (int(action) * 2)
                        else:
                            send(connection, "not ok")



                numberOfRound += 1



        # print("Client is requesting to quit")
        # connection.close()
        # print("Connection " + ip + ":" + port + " closed")
        # is_active = False


def receive(connection):
    client_input = connection.recv(1024)
    return str(client_input.decode("utf8").rstrip())


def send(connection, message):
    connection.send(message.encode("utf8"))


def checkWhoIsTheWinner(dealerCard, playerCard):
    # if -1 the dealer is the winner
    # if 0 is a tie
    # if 1 the player is the winner

    playerScore = 0
    dealerScore = 0

    if dealerCard[0] == "1":
        dealerScore = 10
    elif dealerCard[0] == "J":
        dealerScore = 11
    elif dealerCard[0] == "Q":
        dealerScore = 12
    elif dealerCard[0] == "K":
        dealerScore = 13
    elif dealerCard[0] == "A":
        dealerScore = 14
    else:
        dealerScore = int(dealerCard[0])

    if playerCard[0] == "1":
        playerScore = 10
    elif playerCard[0] == "J":
        playerScore = 11
    elif playerCard[0] == "Q":
        playerScore = 12
    elif playerCard[0] == "K":
        playerScore = 13
    elif playerCard[0] == "A":
        playerScore = 14
    else:
        playerScore = int(playerCard[0])

    if dealerScore > playerScore:
        return -1
    if dealerScore < playerScore:
        return 1
    return 0


if __name__ == "__main__":
    main()
