import os
import click

from crud import add_user, view_all_users, view_total_balance, system_credit, transfer_funds, view_transactions, view_user_balance
from models import session, Users, Wallets, Transactions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  
    # 'cls' for Windows, 'clear' for Linux/Mac

@click.command()
def main_menu():

    while True:
        clear_screen() # clear screen before showing home
        click.secho("#--------------------#", fg="blue")
        click.secho("#                    #", fg="blue")
        click.secho("#     D-WALLET       #", fg="blue")
        click.secho("# Transact Anywhere  #", fg="blue")
        click.secho("#                    #", fg="blue")
        click.secho("#--------------------#", fg="blue")
        click.secho(" ", fg = 'blue')
        click.secho("Select Option to Proceed", fg='yellow')
        click.secho("1. Send/ Add Money", fg='green')
        click.secho("2. Personal Report", fg='green')
        click.secho("3. Admin Section", fg='green')
        click.secho("4. Exit", fg='green')

        menu_input = click.prompt("Select Option", type = int)

        if menu_input == 1:
            transactions_menu()
        
        elif menu_input == 2:
            wallets_menu()
        
        elif menu_input == 3:
            admin_menu()
        
        elif menu_input == 4:
            click.echo(".")
            click.echo(".")
            click.secho("Bye, Another time!!", fg = "yellow")
            click.echo(".")
            click.echo(".")
            break

        else:
            click.secho(f"Invalid choice, try again!", fg = "red")

def admin_menu():
    
    while True:
        click.secho("")
        click.secho("Admin Section", fg = "green")
        click.secho("1. Register a new user", fg='blue')
        click.secho("2. View all User", fg='blue')
        click.secho("3. View total balance", fg='blue')
        click.secho("4. Return to Home", fg='blue')

        user_option = click.prompt("Select User Option", type = int)
        if user_option == 1:
            click.secho("Register a user", fg = "yellow")
            name = click.prompt("1. Enter name of user")
            email = click.prompt("2. Enter email of user")
            ibal = click.prompt("3. Assign initial balance")
            try: 
                add_user(name, email, ibal)
                click.secho(f"User {name} added successfully")
            except Exception as e:
                click.secho(f"Error adding user, {e}")
        
        elif user_option == 2:
            try:
                click.secho("Users in the System", fg = "yellow")
                view_all_users()
            except Exception as e:
                click.secho(f"Error viewing users, {e}")
        elif user_option == 3:
            try:
                view_total_balance()
            except Exception as e:
                click.secho(f"Error viewing balance, {e}")

        elif user_option == 4:
            return() # return to home 
            
        else:
            click.secho(f"Invalid choice, Try again", fg = "red")

def wallets_menu():
    
    while True:
        click.secho("Personal Report", fg = "yellow")
        click.secho("1. View Transactions", fg='blue')
        click.secho("2. View my balance", fg='blue')
        click.secho("3. Return to Home", fg='blue')

        wallet_options = click.prompt("Select wallet Option", type = int)
        if wallet_options == 1:
                      
            try: 
                user_id = click.prompt("1. Enter user id")
                view_transactions(session, user_id)
            except Exception as e:
                click.secho(f"Error adding wallet, {e}")
        
        elif wallet_options == 2:
            try:
                user_id = click.prompt("1. Enter user id")
                view_user_balance(user_id)
            except Exception as e:
                click.secho(f"Error viewing wallets, {e}")
        elif wallet_options == 3:
            return() # return to home 
            
        else:
            click.secho(f"Invalid choice, Try again", fg = "red")

def transactions_menu():
    
    while True:
        click.secho(" ")
        click.secho("Send/ Add Money", fg = "yellow")
        click.secho("1. Add Money to Wallet", fg='blue')
        click.secho("2. Send Money(Pay)", fg='blue')
        click.secho("3. Return to Home", fg='blue')

        transactions_options = click.prompt("Select transactions Option", type = int)
        if transactions_options == 1:
            click.secho("Add Money to Wallet", fg = "yellow")
            receiver_id = click.prompt("1. Enter wallet_id of receiver")
            amount = click.prompt("2. Enter Amount recieved")

            try: 
                system_credit(session, receiver_id, amount)
                wallets = session.query(Wallets).filter_by(id=receiver_id).first()
                users = session.query(Users).filter_by(id=wallets.user_id).first()
                click.secho(f"System credited {amount} for {users.name}", fg = "magenta", bold = True)
            except Exception as e:
                click.secho(f"Error adding transactions, {e}")
        
        elif transactions_options == 2:
            click.secho("Send Money", fg = "yellow")
            sender_wallet_id = click.prompt("1. Enter wallet_id of sender")
            receiver_wallet_id = click.prompt("2. Enter wallet_id of receiver")
            amount = click.prompt("3. Enter Amount Sent")
            try:
                sender_wallets = session.query(Wallets).filter_by(id=sender_wallet_id).first()
                receiver_wallets = session.query(Wallets).filter_by(id=receiver_wallet_id).first()

                #click.secho(f"Transaction successful {sender_wallets.users.name}", fg = "magenta", bold = True)

                description = f"{sender_wallets.users.name} paid {receiver_wallets.users.name}"

                transfer_funds(session, sender_wallet_id, receiver_wallet_id, amount, description)
                click.secho(f"Transaction successful: {description}", fg = "magenta", bold = True)
            except Exception as e:
                click.secho(f"Error viewing transactions, {e}")
        elif transactions_options == 3:
            return() # return to home 
            
        else:
            click.secho(f"Invalid choice, Try again", fg = "red")

if __name__ ==  '__main__':
    main_menu()