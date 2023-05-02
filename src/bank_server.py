import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = 1024

input_file = open('../data/bank.json')
f = input_file.read()
bank = json.loads(f)

s.bind((host, port))


inp, addr = s.recvfrom(1024)
inp = inp.decode('utf-8')

if (inp == 'y'):
    input_file = open('../data/bank.json')
    f = input_file.read()
    bank = json.loads(f)

    name, addr = s.recvfrom(1024)
    name = name.decode('utf-8')
    bank['investors'].append({"name": name, "amount": 0})
    data = json.dumps(bank)

    out = open('../data/bank.json', 'w')
    out.write(data)
    out.close()

    while True:
        input_file = open('../data/bank.json')
        f = input_file.read()
        bank = json.loads(f)

        option, addr = s.recvfrom(1024)
        option = option.decode('utf-8')

        if option == '1':
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')
            amt, addr = s.recvfrom(1024)
            amt = amt.decode('utf-8')

            for i in bank['investors']:
                if i['name'] == name:
                    i['amount'] = i['amount'] + int(amt)

            data = json.dumps(bank)
            out = open('../data/bank.json', 'w')
            out.write(data)
            out.close()

        elif option == '2':
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')
            amt, addr = s.recvfrom(1024)
            amt = amt.decode('utf-8')

            for i in bank['investors']:
                if i['name'] == name:
                    if i['amount'] > int(amt):
                        i['amount'] = i['amount'] - int(amt)
            print(i['amount'])
            data = json.dumps(bank)
            out = open('../data/bank.json', 'w')
            out.write(data)
            out.close()

        elif option == '3':
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')

            for i in bank['investors']:
                if i['name'] == name:
                    amt = i['amount']
            amt = str(amt)
            s.sendto(amt.encode(), addr)

        elif option == '4':
            amt, addr = s.recvfrom(1024)
            amt = amt.decode('utf-8')
            print(amt)
            stock, addr = s.recvfrom(1024)
            stock = stock.decode('utf-8')
            print(stock)
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')
            print(name)
            for i in bank['investors']:
                if i['name'] == name:
                    if i['amount'] > int(amt):
                        i['amount'] = i['amount'] - int(amt)

            for i in bank['investors']:
                if i['name'] == stock:
                    i['amount'] = i['amount'] + int(amt)

            data = json.dumps(bank)
            out = open('../data/bank.json', 'w')
            out.write(data)
            out.close()

        elif option == '5':
            sell_amt, addr = s.recvfrom(1024)
            amt = sell_amt.decode('utf-8')
            print(amt)
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')
            print(name)
            stock, addr = s.recvfrom(1024)
            stock = stock.decode('utf-8')
            print(stock)
            for i in bank['investors']:
                if i['name'] == name:
                    if i['amount'] > int(amt):
                        i['amount'] = i['amount'] + int(amt)

            for i in bank['investors']:
                if i['name'] == stock:
                    if i['amount'] > int(amt):
                        i['amount'] = i['amount'] - int(amt)

            data = json.dumps(bank)
            out = open('../data/bank.json', 'w')
            out.write(data)
            out.close()
