import random
from random import randint
from time import time


class User:
    def __init__(self, name, code, password, phone_number, email):
        self.name = name
        self.code = code
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.accounts = set()
        self.useful_accounts = dict()

    def __eq__(self, other):
        return self.code == other.code and self.password == other.password

    def __hash__(self):
        return hash((self.code, self.password))

    def add_account(self, account):
        self.accounts.add(account)

    def get_accounts(self):
        return self.accounts

    def set_useful_accounts(self, alias, lst):
        self.useful_accounts.update({alias: lst})


class Account(User):
    def __init__(self, user, alias, acc_password):
        super().__init__(user.name, user.code, user.password, user.phone_number, user.email)
        self.alias = alias
        self.acc_password = acc_password
        self.opening = True
        self.money = 0
        self.card_number = "".join([str(randint(0, 9)) for _ in range(16)])
        self.transactions = list()
        self.welsh = (0, 0, 0)  # monthly_cost, remain_duration, start_time

    def __eq__(self, other):
        return self.card_number == other.card_number

    def __hash__(self):
        return hash(self.card_number)

    def close(self):
        self.opening = False

    def open(self):
        self.opening = True

    def get_info(self):
        return f"""
    alias: {self.alias},
    open: {self.opening},
    money: {self.money},
    transactions: {' ### '.join(self.transactions)}
        """

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number

    def change_money(self, money):
        self.money += money

    def get_money(self):
        return self.money

    def check_password(self, password):
        return True if self.password == password else False

    def set_welsh(self, welsh):
        self.welsh = welsh

    def get_welsh(self):
        return self.welsh


def welsh_wrapper(func):
    def wrap(*args, **kwargs):
        now = int(time())
        for account in args[0].accounts:
            welsh = account.get_welsh()
            if welsh[0]:
                time_diff = int((now - welsh[2]) / 20)
                print(time_diff)
                if time_diff >= welsh[1]:
                    time_diff = welsh[1]
                    account.set_welsh((0, 0, 0))
                else:
                    account.set_welsh((welsh[0], welsh[1] - time_diff, welsh[2]))
                account.change_money(-welsh[0] * time_diff)
        return func(*args, **kwargs)

    return wrap


class Controller:
    def __init__(self):
        self.users = set()
        self.accounts = set()
        self.online = None

    @welsh_wrapper
    def signup(self, name, code, password, phone_number, email):
        user = User(name, code, password, phone_number, email)
        if user in self.users:
            print('This user already exists! :(')
        else:
            self.users.add(user)
            print('successful! :)')

    @welsh_wrapper
    def login(self, code, password):
        user = User(name=None, code=code, password=password, phone_number=None, email=None)
        if user in self.users:
            for user_ in self.users:
                if user == user_:
                    self.online = user_
                    print(f'login successful! welcome {user_.name} :)')
                    return
        else:
            print('code or password is wrong!')

    @welsh_wrapper
    def logout(self):
        if self.online:
            print(f'Goodbye {self.online.name} :(')
            self.online = None
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def create_account(self, alias, acc_password):
        if self.online:
            account = Account(self.online, alias, acc_password)
            self.accounts.add(account)
            self.online.add_account(account)
            print(f'Account created with card number: {account.get_card_number()}')
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def show_accounts_info(self):
        if self.online:
            for acc in self.online.get_accounts():
                print(acc.get_info())
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def create_useful_list(self, alias, lst):
        if self.online:
            self.online.set_useful_accounts(alias, lst)
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def send_money(self, money, source, destination, password):
        if self.online:
            user = User(name=None, code=None, password=None, phone_number=None, email=None)
            source_account = Account(user=user, alias=None, acc_password=None)
            source_account.set_card_number(source)
            destination_account = Account(user=user, alias=None, acc_password=None)
            destination_account.set_card_number(destination)
            if source_account in self.accounts:
                for sacc in self.accounts:
                    if sacc == source_account:
                        if sacc.check_password(password):
                            if destination_account in self.accounts:
                                for dacc in self.accounts:
                                    if dacc == destination_account:
                                        sacc.change_money(-int(money))
                                        dacc.change_money(int(money))
                                        print('money has been sent :)')
                                        return True
                            else:
                                print(f'There is no account with card_number={destination}')
                        else:
                            print('Password is wrong!')
            else:
                print(f'There is no account with card_number={source}')
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def paying_bill(self, bill_key=0, pay_key=0):
        if self.online:
            if len(self.online.get_accounts()) == 0:
                print('This user has no account!')
            else:
                self.online.get_accounts()[0].change_money(-random.randint(1, 1000))
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def welsh(self, money, duration):
        if self.online:
            if len(self.online.get_accounts()) == 0:
                print('This user has no account!')
            else:
                list(self.online.get_accounts())[0].set_welsh((int(money) / int(duration), int(duration), int(time())))
                print('set welsh successful! :D')
        else:
            print(f'nobody online :)')

    @welsh_wrapper
    def close_account(self, password):
        if self.online:
            if len(self.online.get_accounts()) == 0:
                print('This user has no account!')
            else:
                for acc in self.online.get_accounts():
                    if acc.check_password(password):
                        if acc.get_money() != 0:
                            destination = input('Please Enter destination for you remaining money!')
                            if self.send_money(acc.get_money(), acc.get_card_number(), destination, password):
                                acc.close()
                                return
                print('Password is wrong!')
        else:
            print(f'nobody online :)')

    def run_shell(self):
        while True:
            s = input()
            if s == '':
                continue
            s = s.split()
            if s[0] == "signup":
                self.signup(*s[1:])
            elif s[0] == "login":
                self.login(*s[1:])
            elif s[0] == "logout":
                self.logout()
            elif s[0] == "create_account":
                self.create_account(*s[1:])
            elif s[0] == "show_accounts_info":
                self.show_accounts_info()
            elif s[0] == "create_useful_list":
                self.create_useful_list(s[1], s[2:])
            elif s[0] == "send_money":
                self.send_money(*s[1:])
            elif s[0] == "paying_bill":
                self.paying_bill(*s[1:])
            elif s[0] == "welsh":
                self.welsh(*s[1:])
            elif s[0] == "close_account":
                self.close_account(*s[1:])
            elif s[0] == "exit":
                return 'GOOD LUCK!'


if __name__ == '__main__':
    controller = Controller()
    controller.run_shell()

