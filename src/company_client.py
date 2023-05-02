import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bank_host = socket.gethostname()
bank_port = 5050
market_host = socket.gethostname()
market_port = 5055

inp = input("Do you want to launch a IPO")

if (inp == 'y'):
    s.sendto(inp.encode(), (market_host, market_port))
    name = input("What is the name of your company?")
    s.sendto(name.encode(), (market_host, market_port))
    quantity = input("What is the number of shares?")
    s.sendto(quantity.encode(), (market_host, market_port))
    price = input("What is the base price per share?")
    s.sendto(price.encode(), (market_host, market_port))
    s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if (inp == 'y'):

    s.sendto(inp.encode(), (bank_host, bank_port))
    s.sendto(name.encode(), (bank_host, bank_port))

    while True:
        print("Select from options")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")

        option = input("Choose Option: ")
        option = str(option)

        if option == '1':
            s.sendto(option.encode(), (bank_host, bank_port))
            amt = input("How much money do you want to deposit?")
            s.sendto(name.encode(), (bank_host, bank_port))
            s.sendto(amt.encode(), (bank_host, bank_port))

        elif option == '2':
            s.sendto(option.encode(), (bank_host, bank_port))
            amt = input("How much money do you want to withdraw?")
            s.sendto(name.encode(), (bank_host, bank_port))
            s.sendto(amt.encode(), (bank_host, bank_port))

        elif option == '3':
            s.sendto(option.encode(), (bank_host, bank_port))
            s.sendto(name.encode(), (bank_host, bank_port))
            amt, addr = s.recvfrom(1024)
            amt = amt.decode('utf')
            print("You have " + amt + "in yout account")
