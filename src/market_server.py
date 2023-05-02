import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname()
port = 5055
input_file = open('../data/market.json')
f = input_file.read()
market = json.loads(f)

s.bind((host, port))

while True:
    inp, addr = s.recvfrom(1024)
    inp = inp.decode('utf-8')

    if (inp == 'y'):
        name, addr = s.recvfrom(1024)
        name = name.decode('utf-8')
        quantity, addr = s.recvfrom(1024)
        quantity = quantity.decode('utf-8')
        price, addr = s.recvfrom(1024)
        price = price.decode('utf-8')
        print(name, quantity, price)

        market['companies'].append(
            {"name": name, "quantity": int(quantity), "price": int(price)})
        data = json.dumps(market)

        out = open('../data/market.json', 'w')
        out.write(data)
        out.close()

    if inp == '4':
        stock, addr = s.recvfrom(1024)
        stock = stock.decode('utf-8')
        print(stock)
        price = 0
        quantity = 0

        input_file = open('../data/market.json')
        f = input_file.read()
        market = json.loads(f)

        for i in market['companies']:
            if i['name'] == stock:
                price = i['price']
                quantity = i['quantity']

        price = str(price)
        quantity = str(quantity)

        s.sendto(price.encode(), addr)
        s.sendto(quantity.encode(), addr)

        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print(data)
        if data == 'OK':
            name, addr = s.recvfrom(1024)
            name = name.decode('utf-8')
            print(name)
            quantity, addr = s.recvfrom(1024)
            quantity = quantity.decode('utf-8')
            print(quantity)

            price = int(price)
            quantity = int(quantity)
            print(price, quantity)

            for i in market['companies']:
                if i['name'] == stock:
                    i['quantity'] -= quantity
                    i['price'] = i['price'] + 1

            data = json.dumps(market)
            print(data)
            out = open('../data/market.json', 'w')
            out.write(data)
            out.close()

            input = open('../data/personal_stock.json')
            fq = input.read()
            market = json.loads(fq)
            print(market['people'])

            stock_flag = 1
            name_flag = 1

            for i in market['people']:
                if name == i['name']:
                    name_flag = 0
                    for j in range(0, len(i['stocks'])):
                        if stock == i['stocks'][j]:
                            i['quantity'][j] += quantity
                            stock_flag = 0

                    if stock_flag == 1:
                        i['stocks'].append(stock)
                        i['quantity'].append(quantity)

            if name_flag == 1:
                market['people'].append(
                    {"name": name, "stocks": [stock], "quantity": [quantity]})

            data = json.dumps(market)
            print(data)
            out = open('../data/personal_stock.json', 'w')
            out.write(data)
            out.close()

        else:
            continue

    if inp == '5':
        stock, addr = s.recvfrom(1024)
        stock = stock.decode('utf-8')

        input_file = open('../data/market.json')
        f = input_file.read()
        market = json.loads(f)

        for i in market['companies']:
            if i['name'] == stock:
                price = i['price']

        price = str(price)
        price = price.encode()
        print(price)
        s.sendto(price, addr)

        input = open('../data/personal_stock.json')
        f1 = input.read()
        market1 = json.loads(f1)

        name, addr = s.recvfrom(1024)
        name = name.decode('utf-8')
        print(name)
        avaliable_quantity = 0

        for i in market1['people']:
            if i['name'] == name:
                for j in range(0, len(i['stocks'])):
                    if i['stocks'][j] == stock:
                        avaliable_quantity = i['quantity'][j]

        avaliable_quantity = str(avaliable_quantity)
        avaliable_quantity = avaliable_quantity.encode()
        s.sendto(avaliable_quantity, addr)
        print(avaliable_quantity)

        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print(data)
        if data == 'OK':
            input_file2 = open('../data/personal_stock.json')
            f2 = input_file2.read()
            market2 = json.loads(f2)

            quantity, addr = s.recvfrom(1024)
            quantity = int(quantity.decode('utf-8'))

            for i in market2['people']:
                if i['name'] == name:
                    for j in range(0, len(i['stocks'])):
                        if i['stocks'][j] == stock:
                            i['quantity'][j] -= quantity

            data = json.dumps(market2)
            out = open('../data/personal_stock.json', 'w')
            out.write(data)
            out.close()

            input_file5 = open('../data/market.json')
            f5 = input_file5.read()
            market5 = json.loads(f5)

            for i in market5['companies']:
                if i['name'] == stock:
                    i['price'] = i['price'] - 1
                    i['quantity'] = i['quantity'] + quantity

            data = json.dumps(market5)
            out = open('../data/market.json', 'w')
            out.write(data)
            out.close()
