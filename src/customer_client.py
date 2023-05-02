import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bank_host = '192.168.1.4'
bank_port = 1024

market_host = '192.168.1.4'
market_port = 5055

inp = input("Do you want to create Bank Account")

if (inp == 'y'):
    s.sendto(inp.encode(), (bank_host, bank_port))
    name = input("What is your name?")
    s.sendto(name.encode(), (bank_host, bank_port))

    while True:
        print("Select from options")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Buy Stock")
        print("5. Sell Stock")

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

        elif option == '4':
            s2.sendto(option.encode(), (market_host, market_port))
            stock = input("What stock do you want to buy?")
            quantity = input("What is the quantity?")
            s2.sendto(stock.encode(), (market_host, market_port))
            price, addr = s2.recvfrom(1024)
            avaliable_quantity, addr = s2.recvfrom(1024)
            avaliable_quantity = avaliable_quantity.decode('utf-8')
            print(avaliable_quantity)
            if int(quantity) > int(avaliable_quantity):
                print("Not enough quantity")
                continue
            price = float(price.decode('utf-8'))
            buy_amt = price * int(quantity)
            inp = '3'
            inp = inp.encode()
            s.sendto(inp, (bank_host, bank_port))
            s.sendto(name.encode(), (bank_host, bank_port))
            bank_balance, addr = s.recvfrom(1024)
            if int(bank_balance) < buy_amt:
                print("Not enough money")
                continue

            data = "OK"
            data = data.encode()

            s2.sendto(data, (market_host, market_port))
            s2.sendto(name.encode(), (market_host, market_port))
            s2.sendto(quantity.encode(), (market_host, market_port))

            option = '4'
            option = option.encode()
            s.sendto(option, (bank_host, bank_port))
            s.sendto(str(buy_amt).encode(), (bank_host, bank_port))
            s.sendto(stock.encode(), (bank_host, bank_port))
            s.sendto(name.encode(), (bank_host, bank_port))

        elif option == '5':
            s2.sendto(option.encode(), (market_host, market_port))
            stock = input("What stock do you want to sell?")
            quantity = input("What is the quantity?")
            s2.sendto(stock.encode(), (market_host, market_port))
            price, addr = s2.recvfrom(1024)
            avaliable_quantity, addr = s2.recvfrom(1024)
            s2.sendto(name.encode(), (market_host, market_port))

            avaliable_quantity, addr = s2.recvfrom(1024)

            if int(quantity) > int(avaliable_quantity):
                data = "NO"
                data = data.encode()
                s2.sendto(data, (market_host, market_port))
                print("No enough quantity")
                continue

            data = "OK"
            data = data.encode()

            s2.sendto(data, (market_host, market_port))
            s2.sendto(quantity, (market_host, market_port))

            option = '5'
            s.sendto(option.encode(), (bank_host, bank_port))
            sell_amt = quantity * price
            sell_amt = str(sell_amt).encode()
            s.sendto(sell_amt, (bank_host, bank_port))
            s.sendto(name.encode(), (bank_host, bank_port))
