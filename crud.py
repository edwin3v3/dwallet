from models import Users, Wallets, Transactions, session
from sqlalchemy import func

BOLD = "\033[1m"
RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"

SYSTEM_TAG = "[SYSTEM]"

# add new user
def add_user(name, email, ibal): 
    new_user = Users(name= name, email=email) 
    session.add(new_user)
    session.commit()
    session.flush()  # ensure new_user.id is available
    
    # Create wallet for that user
    new_wallet = Wallets(user_id=new_user.id, balance=ibal)
    session.add(new_wallet)
    
    session.commit()
    print(f"{YELLOW}User {name} added with wallet balance {ibal}")

# view all users
def view_all_users():
    users = session.query(Users).all()  # Fetch all user records
    print(f"{GREEN}  ID  |   NAME    |  EMAIL {RESET}")
    for user in users:
        print(f"{YELLOW}   {user.id} | {user.name}  |  {user.email}{RESET}")

# view total balance
def view_total_balance():
    total = session.query(func.sum(Wallets.balance)).scalar()  # returns a single value
    if total is None:
        total = 0.0
    print(f"{YELLOW} Total balance in system: {total}")

# add money

def system_credit(session, receiver_wallet, amount):
    
    # assume system wallet is always ID = 1
    system_wallet = session.query(Wallets).get(1)
    amt = float(amount)
    # print("System wallet BEFORE:", system_wallet.balance)
    # print("Receiver wallet Id:", receiver_wallet)

    wallets = session.query(Wallets).filter_by(id=receiver_wallet).first()
    # print("Receiver user:", wallets.id, wallets.user_id)

    users = session.query(Users).filter_by(id=wallets.user_id).first()

    system_wallet.balance -= amt
    wallets.balance += amt
    description = f"{SYSTEM_TAG} Added {amt} to {users.name}"

    txn = Transactions(sender_wallet_id=system_wallet.id,
    receiver_wallet_id = wallets.id,
    amount = amount,
    description = description)

    session.add(txn)
    session.commit()
    #sesssion.flush()

def transfer_funds(session, sender_wallet_id, receiver_wallet_id, amount, description):

    t_amt = float(amount)
    sender_wallet = session.query(Wallets).filter_by(id=sender_wallet_id).first()
    receiver_wallet = session.query(Wallets).filter_by(id=receiver_wallet_id).first()

    if sender_wallet.balance < t_amt:
        raise ValueError("Insufficient funds")

    sender_wallet.balance -= t_amt
    receiver_wallet.balance += t_amt

    txn = Transactions(sender_wallet_id = sender_wallet_id, 
    receiver_wallet_id = receiver_wallet_id,  amount = t_amt, description = description )
    session.add(txn)
    session.commit()

def view_transactions(session, user_id):
    wallet = session.query(Wallets).filter_by(user_id = user_id).first()

    if wallet is None:
        print(f"{RED} No wallet found for user_id={user_id}{RESET}")
        return

    sent_transactions = session.query(Transactions).filter_by(sender_wallet_id = wallet.id).all()
    print(f"{BOLD}{YELLOW}Sent Transactions for {wallet.users.name}{RESET}")
    print(f"{GREEN}  ID  |   TIME    |  AMOUNT | DESCRIPTION {RESET}")
    for transaction in sent_transactions:
        print(f"{YELLOW}   {transaction.id} | {transaction.timestamp}  |  {transaction.amount}  |   {transaction.description}{RESET}")

    received_transactions = session.query(Transactions).filter_by(receiver_wallet_id = wallet.id).all()
    print(f"{BOLD}{YELLOW}Received Transactions for {wallet.users.name}{RESET}")
    print(f"{GREEN}  ID  |   TIME    |  AMOUNT | DESCRIPTION {RESET}")
    for r_transaction in received_transactions:
        print(f"{YELLOW}   {r_transaction.id} | {r_transaction.timestamp}  |  {r_transaction.amount}  |   {r_transaction.description}{RESET}")


def view_user_balance(user_id):
    wallets = session.query(Wallets).filter_by(user_id = user_id).first()

    if wallets is None:
        print(f"{RED} No wallet found for user_id={user_id}{RESET}")
        return

    print(f"{YELLOW} Total balance for {wallets.users.name} is: {wallets.balance}")


    

    