# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0 )')


def menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice = input()

    if choice == '1':
        create_account()
        menu()
    elif choice == '2':
        log_in()
        menu()
    elif choice == '0':
        exit()
    else:
        print('Select from options 0,1,2')
        menu()


def create_account():
    print('Your card has been created')
    card_one = random.randint(400000000000000, 400000999999999)
    card = csalg(card_one)
    pin = create_pin()
    print('Your card number:')
    print(card)
    print('Your card PIN:')
    print(pin)
    cur.execute('INSERT INTO card(number, pin) VALUES(?, ?)', (card, pin))
    conn.commit()


def create_pin():
    pin = str(random.randint(0, 9))
    for i in range(3):
        pin = pin + str(random.randint(0, 9))
    return pin


def log_in():
    print('Enter your card number:')
    cardin = int(input())
    print('Enter your PIN:')
    pinin = input()
    cur.execute('SELECT number, pin FROM card WHERE number =:number', {"number": cardin})
    result = cur.fetchone()
    if type(result) != tuple:
        print('Wrong card number or PIN!')
        menu()
    elif result[1] != pinin:
        print('Wrong card number or PIN!')
        menu()
    else:
        if result[1] == pinin:
            print('You have successfully logged in!')
            logged_in(result[0])


def logged_in(cardno):
    cur.execute('SELECT number, pin, balance FROM card WHERE number =:number', {"number": cardno})
    card_details = cur.fetchone()
    balance = card_details[2]
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')
    choice = input()
    if choice == '1':
        print(f'Balance: {balance}')
        logged_in(cardno)
    elif choice == '2':
        print('Enter income:')
        income = int(input())
        cur.execute('UPDATE card SET balance = ? WHERE number = ?', (balance + income, cardno))
        conn.commit()
        print('Income was added!')
        logged_in(cardno)
    elif choice == '3':
        do_transfer(card_details)
        logged_in(cardno)
    elif choice == '4':
        cur.execute('DELETE FROM card WHERE number =:number', {"number": cardno})
        conn.commit()
        print('The account has been closed!')
    elif choice == '0':
        print('Bye!')
        exit()
    elif choice == '5':
        print('You have successfully logged out!')
        menu()
    else:
        logged_in(cardno)


def do_transfer(card_details):
    balance = card_details[2]

    print('Transfer')
    print('Enter card number:')
    dest_card = input()
    if dest_card == card_details[0]:
        print("You can't transfer money to the same account!")
    else:
        if not luhn_check(dest_card):
            print('Probably you made a mistake in the card number. Please try again!')
        else:
            cur.execute('SELECT number, balance FROM card WHERE number = :number', {"number": dest_card})
            recipient = cur.fetchone()
            if type(recipient) != tuple:
                print('Such a card does not exist.')
            else:
                print('Enter how much money you want to transfer:')
                transfer_amount = int(input())
                if balance < transfer_amount:
                    print('Not enough money!')
                else:
                    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (recipient[1] + transfer_amount, recipient[0]))
                    conn.commit()
                    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (balance - transfer_amount, card_details[0]))
                    conn.commit()
                    print('Success!')



def csalg(cardin):
    cardlist = [int(x) for x in str(cardin)]
    algcheck = []
    count = 1
    for x in cardlist:
        if count % 2 != 0:
            if (x * 2) > 9:
                algcheck.append((x * 2) - 9)
            else:
                algcheck.append(x * 2)
        else:
            algcheck.append(x)
        count += 1
    lastdig = int(str(sum(algcheck))[-1])
    if lastdig == 0:
        algcheck.append(lastdig)
    else:
        algcheck.append((10 - lastdig))

    finalcard = ''
    cardlist.append(algcheck[-1])
    return int(finalcard.join(str(z) for z in cardlist))


def luhn_check(cardno):
    if len(cardno) != 16:
        return False
    cardlist = [int(x) for x in str(cardno)]
    algcheck = []
    count = 1
    for x in cardlist:
        if count % 2 != 0:
            if (x * 2) > 9:
                algcheck.append((x * 2) - 9)
            else:
                algcheck.append(x * 2)
        else:
            algcheck.append(x)
        count += 1
    if (sum(algcheck) % 10) == 0:
        return True
    else:
        return False


menu()